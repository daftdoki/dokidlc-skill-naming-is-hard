---
name: review-user-facing-names
description: Review the names users see (commands, flags, settings, labels, output fields) against the naming rule, judged for expert or lay users; report, then offer to apply the renames.
argument-hint: "[SCOPE]"
disable-model-invocation: true
---

# Review user-facing names

Scope: $ARGUMENTS

An empty scope means the current diff: `git diff HEAD` and the untracked
files. When that diff is empty, say so and stop. Otherwise the scope is
the files, directories, or whole repository it names.

This review only reads until the user says yes. The report comes first,
the offer last.

## 1. Read the rule

Read `../naming-is-hard/references/naming-rule.md`, relative to this
skill's base directory. It is the whole standard: every finding cites
one of its sections by heading (The shape, The object, The words, Done
when). It is written for commands, flags, and settings, and it applies
to a graphical interface the same way: a button or menu item is a
command, and a label on a value is a setting.

## 2. Decide the audience

Find who the users are: the README, the docs, the help text, the
install guide. Decide one audience for the review:

- **expert**: people who work in the project's field and know its terms.
  A field term is the right word for them. A plain or invented word
  that hides the term they know fails "The words": the interface wins,
  and the field's meaning comes first.
- **lay**: people outside the field. A word they would have to look up
  fails "The words", even when it is the field's correct term; use the
  word they already know.

When the project does not say who its users are, judge from the surface
and say the audience is a judgement, with the reason.

## 3. Collect the names

List every name a user types, clicks, reads, or sets: commands,
subcommands, flags, positional argument names shown in help, settings
and config keys, environment variables, menu items, buttons, field
labels, output column headings, and the terms in error messages. For
each name, read what the code does when the user reaches it. The code's
behaviour, not its help text, decides what the name has to say.

## 4. Judge each name

Run every name through the rule's four Done when checks, read as the
chosen audience. A name that passes all four stays out of the report,
even when another name would also pass. A finding is a failed check,
never a taste: "could be shorter" or a preferred synonym without a
failed check is not a finding.

For each failure, write the rename that passes all four checks for this
audience, and name the rule section that decided it.

## 5. Report

Write the report in this shape, worst failure first:

```
Scope: WHAT WAS REVIEWED
Audience: expert|lay, because ONE SENTENCE OF EVIDENCE

| Name | Where | Rename to | Rule section | Why |
|---|---|---|---|---|
| `old-name` | path/cli.py:12 | `new-name` | The words | One sentence on the failed check. |
```

The first cell holds the current name alone in one code span, as the
user types or sees it: no program name, no parent command, no argument
placeholders. A flag keeps its dashes (`--purge`). The report has this
one table. Names that passed get no table and no list.

Under the table, one line per rename that reaches beyond its definition:
the help text, documents, scripts, and saved settings that change with
it, and whether existing users need the old name kept as an alias.

End the report with this line, and nothing after it:

Apply these renames? Say yes, or name the rows to apply.

## 6. On the user's yes

Apply the renames the user named, or all of them for a plain yes. Change
each name everywhere it appears: definition, help text, documents,
tests, and examples. Run the project's tests when it has them, and
report what changed.
