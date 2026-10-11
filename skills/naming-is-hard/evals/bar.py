#!/usr/bin/env python3
"""Check the rename eval's bar over several runs.

    bar.py OUT_DIR...

Reads each run's score.txt and prints every run's acceptable and exact
counts, then the means. Exit 1 when the mean acceptable is under 14 of
17 or any run failed its format check.
"""
import re
import sys
from pathlib import Path

BAR = 14
acc, exact, fmt_ok = [], [], True
if not sys.argv[1:]:
    sys.exit("usage: bar.py OUT_DIR...")
for d in sys.argv[1:]:
    path = Path(d) / "score.txt"
    text = path.read_text() if path.is_file() else ""
    a = re.search(r"^acceptable: (\d+)", text, re.M)
    e = re.search(r"^exact: (\d+)", text, re.M)
    if not (a and e):
        sys.exit(f"{path}: no score; the run or its judge failed")
    a, e = int(a.group(1)), int(e.group(1))
    f = "format: ok" in text
    fmt_ok &= f
    acc.append(a)
    exact.append(e)
    print(f"{d}: acceptable {a}, exact {e}, format {'ok' if f else 'FAIL'}")
mean = sum(acc) / len(acc)
print(f"mean acceptable {mean:.1f} of 17 (bar {BAR}), mean exact {sum(exact) / len(exact):.1f}")
sys.exit(0 if mean >= BAR and fmt_ok else 1)
