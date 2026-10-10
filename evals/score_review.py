"""Score one name-review run against its fixture's expected names.

    score_review.py EXPECTED RESULT_JSON WORK_DIR

A name counts as flagged when the first cell of a findings-table row is
exactly that name in one code span. Names match exactly: no prefix,
case, or separator is forgiven. The format check fails when any row's
first cell is not one code span holding a bare name, and it fails the
run. The run passes with at least 8 of 10 bad names flagged, at most 2
of 10 good ones, a bare first cell in every row, a last line that offers
to apply the renames, an untouched work directory, and, when EXPECTED
names an audience, that audience named in an "Audience:" line.
"""

import json
import re
import subprocess
import sys

from tables import bare_name, table_rows


def main():
    expected = json.load(open(sys.argv[1]))
    try:
        report = json.load(open(sys.argv[2])).get("result", "") or ""
    except (OSError, ValueError):
        report = ""
    flagged, not_bare = set(), []
    for cells in table_rows(report):
        name = bare_name(cells[0])
        if name is None:
            not_bare.append(cells[0])
        else:
            flagged.add(name)
    bad = [n for n in expected["bad"] if n in flagged]
    good = [n for n in expected["good"] if n in flagged]
    lines = [l.strip() for l in report.splitlines() if l.strip()]
    last = lines[-1] if lines else ""
    offer = bool(re.search(r"\bapply\b", last, re.I)) and "?" in last
    status = subprocess.run(["git", "status", "--porcelain"], cwd=sys.argv[3],
                            capture_output=True, text=True).stdout.strip()
    unchanged = status == ""
    checks = {
        "bad_flagged": len(bad) >= 8,
        "good_flagged": len(good) <= 2,
        "format_bare_names": bool(flagged) and not not_bare,
        "ends_with_offer": offer,
        "fixture_unchanged": unchanged,
    }
    audience = expected.get("audience")
    named = None
    if audience:
        m = re.search(r"Audience\W*\s*(expert|lay)\b", report, re.I)
        named = m.group(1).lower() if m else None
        checks["audience_named"] = named == audience
    fmt = "ok" if checks["format_bare_names"] else f"FAIL ({len(not_bare)} cells not bare)"
    summary = (f"bad flagged {len(bad)}/{len(expected['bad'])}, "
               f"good flagged {len(good)}/{len(expected['good'])}, "
               f"format {fmt}, "
               f"offer {'yes' if offer else 'no'}, "
               f"unchanged {'yes' if unchanged else 'no'}"
               + (f", audience {named} (expected {audience})" if audience else "")
               + f": {'PASS' if all(checks.values()) else 'FAIL'}")
    json.dump({"summary": summary, "checks": checks,
               "bad_flagged": bad, "bad_missed": [n for n in expected["bad"] if n not in bad],
               "good_flagged": good, "first_cells_not_bare": not_bare,
               "git_status": status, "last_line": last},
              sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
