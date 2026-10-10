"""Score one review run against expected.json.

    score.py EXPECTED RESULT_JSON WORK_DIR

A name counts as flagged when it is the first code span in the first
cell of a row of the report's findings table. A span of several words
counts as its flag, or else its last word that is not a placeholder.
Names are compared after dropping a module prefix, call parentheses, a
leading "--", and an "=value", with "-" and "_" treated as one and case
ignored. The run
passes with at least 8 of 10 bad names flagged, at most 2 of 10 good
ones, a last line that offers to apply the renames, an untouched work
directory, and, when EXPECTED names an audience, that audience named in
an "Audience:" line.
"""

import json
import re
import subprocess
import sys


def norm(name: str) -> str:
    tokens = name.split()
    if len(tokens) > 1:
        # "pantry gc", "list --nuke", "rate-recipe RECIPE STARS": keep the
        # flag if there is one, else the last word that is not a placeholder.
        tokens = [t for t in tokens if not re.match(r"^([A-Z_]+|<.*>|\[.*\])$", t)] or tokens
        flags = [t for t in tokens if t.startswith("--")]
        tokens = flags or tokens[-1:]
    name = tokens[0] if tokens else ""
    name = name.split("=")[0]
    name = re.sub(r"\(.*\)$", "", name).lstrip("-")
    name = name.split(".")[-1]
    return name.replace("-", "_").lower()


def flagged_names(report: str) -> set[str]:
    names = set()
    for line in report.splitlines():
        line = line.strip()
        if not line.startswith("|") or re.match(r"^\|[\s:|-]+\|?$", line):
            continue
        first = line.strip("|").split("|")[0]
        span = re.search(r"`([^`]+)`", first)
        if span:
            names.add(norm(span.group(1)))
    return names


def main() -> None:
    expected = json.load(open(sys.argv[1]))
    try:
        report = json.load(open(sys.argv[2])).get("result", "") or ""
    except (OSError, ValueError):
        report = ""
    flagged = flagged_names(report)
    bad = [n for n in expected["bad"] if norm(n) in flagged]
    good = [n for n in expected["good"] if norm(n) in flagged]
    lines = [l.strip() for l in report.splitlines() if l.strip()]
    last = lines[-1] if lines else ""
    offer = bool(re.search(r"\bapply\b", last, re.I)) and "?" in last
    status = subprocess.run(["git", "status", "--porcelain"], cwd=sys.argv[3],
                            capture_output=True, text=True).stdout.strip()
    unchanged = status == ""
    checks = {
        "bad_flagged": len(bad) >= 8,
        "good_flagged": len(good) <= 2,
        "ends_with_offer": offer,
        "fixture_unchanged": unchanged,
    }
    audience = expected.get("audience")
    named = None
    if audience:
        m = re.search(r"Audience\W*\s*(expert|lay)\b", report, re.I)
        named = m.group(1).lower() if m else None
        checks["audience_named"] = named == audience
    summary = (f"bad flagged {len(bad)}/{len(expected['bad'])}, "
               f"good flagged {len(good)}/{len(expected['good'])}, "
               f"offer {'yes' if offer else 'no'}, "
               f"unchanged {'yes' if unchanged else 'no'}"
               + (f", audience {named} (expected {audience})" if audience else "")
               + f": {'PASS' if all(checks.values()) else 'FAIL'}")
    json.dump({"summary": summary, "checks": checks,
               "bad_flagged": bad, "bad_missed": [n for n in expected["bad"] if n not in bad],
               "good_flagged": good, "git_status": status, "last_line": last},
              sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
