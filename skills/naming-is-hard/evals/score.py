#!/usr/bin/env python3
"""Count exact matches between a rename report and the answer key.

    score.py REPORT [ANSWER_KEY]

REPORT is the agent's final message: a markdown table whose first column
is the item number 1 to 17 and whose third column is the new name.
ANSWER_KEY defaults to answer-key.md beside this script; only its rows
1 to 17 count. A new name matches when its cell is one code span whose
text equals the key's exactly. The format check fails when any New cell
is not one code span holding a bare name (no program name, parent
command, or argument), and it fails the run.
Prints one line per item, then the score line and the format line.
Exit 2 when the report has no table rows, 1 when the format check fails.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "evals"))
from tables import SPAN, bare_name, table_rows  # noqa: E402

ITEMS = 17


def new_names(text):
    found = {}
    for cells in table_rows(text):
        if len(cells) > 2 and cells[0].isdigit():
            n = int(cells[0])
            if 1 <= n <= ITEMS and n not in found:
                found[n] = cells[2]
    return found


def main():
    here = Path(__file__).resolve().parent
    report = Path(sys.argv[1]).read_text()
    key_path = Path(sys.argv[2]) if len(sys.argv) > 2 else here / "answer-key.md"
    key = {n: SPAN.match(c).group(1) for n, c in new_names(key_path.read_text()).items()}
    got = new_names(report)
    if not got:
        print("score: no table rows in the report", file=sys.stderr)
        sys.exit(2)
    hits, not_bare = 0, []
    for n in range(1, ITEMS + 1):
        cell = got.get(n, "")
        have = bare_name(cell)
        if cell and have is None:
            not_bare.append(n)
        ok = have == key[n]
        hits += ok
        print(f"{n:2} {'=' if ok else 'x'} {cell or '(missing)':40} key: {key[n]}")
    print(f"score: {hits} of {ITEMS}")
    if not_bare:
        print(f"format: FAIL, New cell not one bare name in items {', '.join(map(str, not_bare))}")
        sys.exit(1)
    print("format: ok")


if __name__ == "__main__":
    main()
