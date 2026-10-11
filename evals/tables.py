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

    A table is a run of lines that start with "|". Its body rows are the
    ones below its separator line; a run with no separator is no table.
    """
    rows, block = [], []
    for line in [l.strip() for l in text.splitlines()] + [""]:
        if line.startswith("|"):
            block.append(line)
            continue
        seps = [i for i, l in enumerate(block) if SEPARATOR.match(l) and "-" in l]
        if seps:
            rows += [split_cells(l) for l in block[seps[0] + 1:] if not SEPARATOR.match(l)]
        block = []
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
