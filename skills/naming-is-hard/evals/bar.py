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
for d in sys.argv[1:]:
    text = (Path(d) / "score.txt").read_text()
    a = int(re.search(r"^acceptable: (\d+)", text, re.M).group(1))
    e = int(re.search(r"^exact: (\d+)", text, re.M).group(1))
    f = "format: ok" in text
    fmt_ok &= f
    acc.append(a)
    exact.append(e)
    print(f"{d}: acceptable {a}, exact {e}, format {'ok' if f else 'FAIL'}")
mean = sum(acc) / len(acc)
print(f"mean acceptable {mean:.1f} of 17 (bar {BAR}), mean exact {sum(exact) / len(exact):.1f}")
sys.exit(0 if mean >= BAR and fmt_ok else 1)
