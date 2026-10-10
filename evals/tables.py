"""Read markdown tables out of a model's report. Shared by every scorer."""

import re

# A pipe inside backticks, as in `status-line [on|off]`, or escaped as \|,
# is part of the cell, not a column break.
CELL_BREAK = re.compile(r"(?<!\\)\|(?=(?:[^`]*`[^`]*`)*[^`]*$)")
SEPARATOR = re.compile(r"^\|?[\s:|-]+\|?$")
SPAN = re.compile(r"^`([^`]+)`$")
BARE_NAME = re.compile(r"^-{0,2}[A-Za-z_][A-Za-z0-9_-]*$")


def split_cells(line):
    return [c.strip() for c in CELL_BREAK.split(line.strip().strip("|"))]


def table_rows(text):
    """Return the cells of every body row of every table in text.

    A header row, the one right above a separator row, is left out, and
    so is the separator.
    """
    lines = [l.strip() for l in text.splitlines()]
    rows = []
    for i, line in enumerate(lines):
        if not line.startswith("|") or SEPARATOR.match(line):
            continue
        if i + 1 < len(lines) and SEPARATOR.match(lines[i + 1]) and "-" in lines[i + 1]:
            continue
        rows.append(split_cells(line))
    return rows


def bare_name(cell):
    """Return the name when cell is one code span holding one bare name.

    A bare name is one word of letters, digits, "_" and "-", with up to
    two leading dashes for a flag: no program name, parent command,
    module prefix, parentheses, argument, or "=value". Return None
    otherwise.
    """
    m = SPAN.match(cell.strip())
    if m and BARE_NAME.match(m.group(1)):
        return m.group(1)
    return None
