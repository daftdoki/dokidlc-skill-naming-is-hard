#!/usr/bin/env python3
"""Grade a rename report: exact matches, and names a judge accepts.

    score.py REPORT [ANSWER_KEY]

REPORT is the agent's final message: a markdown table whose first column
is the item number 1 to 17 and whose third column is the new name.
ANSWER_KEY defaults to answer-key.md beside this script; only its rows
1 to 17 count.

Exact: the New cell is one code span whose text equals the key's.
Acceptable: an exact match, or a name the judge accepts. The judge is one
headless `claude -p` call (JUDGE_MODEL, default claude-fable-5-1) that
gets naming-rule.md, and for each item what it does (items.json), the
creator's name, and the proposed name. It never sees which run or arm
made the names. It answers per item whether the name passes the rule's
four Done when checks and whether a newcomer would read it the same way
as the creator's name; acceptable means yes to both.

Format: every New cell is one code span holding a bare name (no program
name, parent command, or argument).

Prints one line per item, then the exact, acceptable, and format lines.
Exit 2 when the report has no table rows; 1 when the format check fails
or fewer than BAR (14) items are acceptable.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "evals"))
from tables import SPAN, bare_name, table_rows  # noqa: E402

ITEMS = 17
BAR = 14
RULE = HERE.parent / "references" / "naming-rule.md"
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-fable-5-1")

JUDGE_PROMPT = """You grade proposed names for the commands, flags, and settings of a command-line tool. The naming rule they must follow is between the RULE markers.

RULE
{rule}
RULE

The proposal's full set of names, for the rule's checks across names: {all_names}

For each item below you get the item's current name, what it does when it runs, the reference name its maintainer chose, and the proposed name. Answer two questions about the proposed name:

- passes_rule: given what the item does, does the proposed name pass all four checks in the rule's Done when section?
- same_reading: would a newcomer who reads only the proposed name understand the item the way the reference name tells them? A different word with the same meaning is yes. A name that suggests a different action, object, or scope is no.

Items:
{items}

Reply with only a JSON array, one object per item, in this form:
[{{"n": 1, "passes_rule": true, "same_reading": true, "reason": "one line"}}]
"""


def new_names(text):
    found = {}
    for cells in table_rows(text):
        if len(cells) > 2 and cells[0].isdigit():
            n = int(cells[0])
            if 1 <= n <= ITEMS and n not in found:
                found[n] = cells[2]
    return found


def judge(asks, all_names):
    """Ask the judge about each (n, item, creator, proposed); return {n: (ok, reason)}."""
    if not asks:
        return {}
    items = "\n".join(json.dumps({"n": n, "current": it["old"], "does": it["does"],
                                  "reference": want, "proposed": have})
                      for n, it, want, have in asks)
    prompt = JUDGE_PROMPT.format(rule=RULE.read_text(), all_names=", ".join(all_names),
                                 items=items)
    with tempfile.TemporaryDirectory() as tmp:
        run = subprocess.run(
            ["claude", "-p", "--setting-sources", "", "--strict-mcp-config", "--tools", "",
             "--model", JUDGE_MODEL, "--output-format", "json", prompt],
            cwd=tmp, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    try:
        text = json.loads(run.stdout).get("result") or ""
        answers = json.loads(re.search(r"\[.*\]", text, re.S).group(0))
    except (ValueError, AttributeError) as err:
        print(f"judge: no JSON answer ({err}); stderr: {run.stderr[-300:]}", file=sys.stderr)
        sys.exit(3)
    out = {}
    for a in answers:
        ok = bool(a.get("passes_rule")) and bool(a.get("same_reading"))
        why = f"rule {'yes' if a.get('passes_rule') else 'no'}, reading {'yes' if a.get('same_reading') else 'no'}: {a.get('reason', '')}"
        out[int(a["n"])] = (ok, why)
    return out


def main():
    report = Path(sys.argv[1]).read_text()
    key_path = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "answer-key.md"
    key = {n: SPAN.match(c).group(1) for n, c in new_names(key_path.read_text()).items()}
    items = json.loads((HERE / "items.json").read_text())
    got = new_names(report)
    if not got:
        print("score: no table rows in the report", file=sys.stderr)
        sys.exit(2)

    names, not_bare = {}, []
    for n in range(1, ITEMS + 1):
        cell = got.get(n, "")
        name = bare_name(cell)
        if cell and name is None:
            not_bare.append(n)
            m = SPAN.match(cell.strip())
            name = m.group(1) if m else cell.strip()
        names[n] = name
    exact = {n for n in names if names[n] == key[n]}
    asks = [(n, items[n - 1], key[n], names[n]) for n in sorted(names)
            if names[n] and n not in exact]
    verdicts = judge(asks, [names[n] for n in sorted(names) if names[n]])

    acceptable = 0
    for n in range(1, ITEMS + 1):
        if n in exact:
            ok, why = True, "exact"
        elif not names[n]:
            ok, why = False, "missing"
        else:
            ok, why = verdicts.get(n, (False, "judge gave no answer"))
        acceptable += ok
        mark = "=" if n in exact else ("+" if ok else "x")
        print(f"{n:2} {mark} {names[n] or '(missing)':36} key: {key[n]:32} {why}")

    print(f"exact: {len(exact)} of {ITEMS}")
    print(f"acceptable: {acceptable} of {ITEMS} (run bar {BAR})")
    if not_bare:
        print(f"format: FAIL, New cell not one bare name in items {', '.join(map(str, not_bare))}")
    else:
        print("format: ok")
    sys.exit(1 if not_bare or acceptable < BAR else 0)


if __name__ == "__main__":
    main()
