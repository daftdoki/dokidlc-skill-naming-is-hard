---
name: review-user-facing-names
description: Review the names users see (commands, flags, settings, labels, output fields) against the naming rule, judged for expert or lay users; report, then offer to apply the renames.
argument-hint: "[SCOPE]"
disable-model-invocation: true
---

# Review user-facing names

Scope: $ARGUMENTS

## 1. Read the rule and the procedure

Read both files in `../naming-is-hard/references/`, relative to this
skill's base directory: `naming-rule.md`, the standard, and
`review-procedure.md`, the steps every name review shares. Settle the
scope as its Scope section says. Interface names map to the rule
through its section Outside a command line.

## 2. Decide the audience

Find who the users are: the README, the docs, the help text, the
install guide. Decide one audience for the review:

- **expert**: people who work in the project's field and know its terms.
- **lay**: people outside the field.

The audience line in The words says which word each audience gets.
When the project does not say who its users are, judge from the
interface and say the audience is a judgement, with the reason.

## 3. Collect the names

List every name a user types, clicks, reads, or sets: commands,
subcommands, flags, positional argument names shown in help, settings
and config keys, environment variables, menu items, buttons, field
labels, output column headings, and the terms in error messages.

## 4. Judge, report, apply

Read each name as the chosen audience reads it. Then follow the
procedure's Judge, Report, and On the user's yes sections. The report
has two header lines:

```
Scope: WHAT WAS REVIEWED
Audience: expert|lay, because ONE SENTENCE OF EVIDENCE
```

Each line under the table also says whether existing users need the
old name kept as an alias.
