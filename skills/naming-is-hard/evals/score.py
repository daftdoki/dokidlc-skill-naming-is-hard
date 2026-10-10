#!/usr/bin/env python3
"""Count exact matches between a rename report and the answer key.

    score.py REPORT [ANSWER_KEY]

REPORT is the agent's final message: a markdown table whose first column
is the item number 1 to 17 and whose third column is the new name.
ANSWER_KEY defaults to answer-key.md beside this script; only its rows
1 to 17 count. Both sides are normalized the same way before comparing:
backticks, surrounding spaces, and case drop; a leading "iirc " or
"/iirc " drops; only the first word stays, so arguments drop
("set-x NAME VALUE" becomes "set-x"). Nothing fuzzier counts.
Prints one line per item, then "score: N of 17". Exit 2 when the report
has no table rows.
"""
import re
import sys
from pathlib import Path

ITEMS = 17


def norm(name):
    s = name.replace("`", "").strip().lower()
    s = re.sub(r"^/?iirc\s+", "", s)
    return s.split()[0] if s.split() else ""


def rows(text, name_col):
    found = {}
    for line in text.splitlines():
        # A pipe inside backticks, as in `status-line [on|off]`, or escaped
        # as \|, is part of the cell, not a column break.
        cells = [c.strip() for c in re.split(r"(?<!\\)\|(?=(?:[^`]*`[^`]*`)*[^`]*$)",
                                             line.strip().strip("|"))]
        if len(cells) <= name_col or not cells[0].isdigit():
            continue
        n = int(cells[0])
        if 1 <= n <= ITEMS and n not in found:
            found[n] = cells[name_col]
    return found


def main():
    here = Path(__file__).resolve().parent
    report = Path(sys.argv[1]).read_text()
    key_path = Path(sys.argv[2]) if len(sys.argv) > 2 else here / "answer-key.md"
    key = rows(key_path.read_text(), 2)
    got = rows(report, 2)
    if not got:
        print("score: no table rows in the report", file=sys.stderr)
        sys.exit(2)
    hits = 0
    for n in range(1, ITEMS + 1):
        want, have = norm(key[n]), norm(got.get(n, ""))
        ok = want == have
        hits += ok
        print(f"{n:2} {'=' if ok else 'x'} {have or '(missing)':40} key: {want}")
    print(f"score: {hits} of {ITEMS}")


if __name__ == "__main__":
    main()
