# Review procedure

The name reviews run this procedure against
[naming-rule.md](naming-rule.md). The review's own SKILL.md says which
names to collect and how to read them. The review only reads until the
user says yes: the report comes first, the offer last.

## Scope

An empty scope means the current diff: `git diff HEAD` and the
untracked files. When that diff is empty, say so and stop. Otherwise
the scope is the files, directories, or whole repository it names.

## Judge

For each collected name, read its definition and what the code does
when it runs. The code's behaviour, not its docstring or help text,
decides what the name has to say.

Run every name through the rule's four Done when checks. A name that
passes all four stays out of the report, even when another name would
also pass. A finding is a failed check, never a taste: case style,
formatting, "could be shorter", or a preferred synonym are findings
only through a failed check.

For each failure, write the rename that passes all four checks, and
name the rule section that decided it by its heading (The shape, The
object, The words, Product names, Done when).

## Report

Write the header lines the review names, then one findings table,
worst failure first:

```
Scope: WHAT WAS REVIEWED

| Name | Where | Rename to | Rule section | Why |
|---|---|---|---|---|
| `old_name` | path/file.py:12 | `new_name` | The object | One sentence on the failed check. |
```

The first cell is the current name alone in one code span, spelled as
it is defined: no path, module prefix, program name, parent command,
parentheses, or argument placeholders. A flag keeps its dashes
(`--purge`). The report has this one table; names that passed get no
table and no list.

Under the table, one line per rename that reaches beyond its
definition, naming what changes with it: call sites, tests, help text,
documents, scripts, and saved settings.

End the report with this line, and nothing after it:

Apply these renames? Say yes, or name the rows to apply.

## On the user's yes

Apply the renames the user named, or all of them for a plain yes.
Change each name everywhere it appears: definition, call sites, help
text, tests, documents, and examples. Then report what changed.
