---
name: review-internal-names
description: Review the names engineers read in code (functions, classes, variables, parameters, config keys, log fields) against the naming rule; report, then offer to apply the renames.
argument-hint: "[SCOPE]"
disable-model-invocation: true
---

# Review internal names

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
when). The rule is written for commands; in code it maps like this:

- **A function or method** is a command. Its name is a verb, then its
  object, so "the code VERBs OBJECT" is a true sentence. The verb follows
  the rule's three cases: return what is stored, work out a result, or
  change something.
- **A parameter that changes what a function does**, not just how much,
  is a flag that should be its own function.
- **A variable, constant, attribute, field, or config key** is an object
  or a setting: it ends on the head noun, with the words that say which
  kind in front. The head noun names what it holds, not what it is for.
- **A class** names the kind of thing each instance is. A suffix that
  names no kind (`Manager`, `Handler`, `Helper`, `Data`, `Info`) fails
  "The object".
- **Every name** answers to "The words": one role per word across the
  project, the meaning a word already has in the field, and the
  project's existing term while it passes.

The audience is the project's engineers, so a field's term is a fair
word here (rule: "Name for the audience").

## 2. Collect the names

List every name the scope defines: modules, classes, functions,
methods, parameters, module-level variables and constants, attributes,
config keys, log event names, and environment variables. Include a
local variable whose name says nothing about what it holds (`data2`,
`tmp`); leave out the conventional short locals (`i`, `e`, `err`, `f`).
For each name, read its definition and what the code does with it. The
code's behaviour, not its docstring, decides what the name has to say.

## 3. Judge each name

Run every name through the rule's four Done when checks. A name that
passes all four stays out of the report, even when another name would
also pass. A finding is a failed check, never a taste: case style,
formatting, and "could be shorter" without a failed check are not
findings.

For each failure, write the rename that passes all four checks, and
name the rule section that decided it.

## 4. Report

Write the report in this shape, worst failure first:

```
Scope: WHAT WAS REVIEWED

| Name | Where | Rename to | Rule section | Why |
|---|---|---|---|---|
| `old_name` | path/file.py:12 | `new_name` | The object | One sentence on the failed check. |
```

The first cell holds the current name alone in one code span: no path,
no module prefix, no parentheses. The report has this one table. Names
that passed get no table and no list.

Under the table, one line per rename that reaches beyond its definition:
how many call sites, tests, and documents change with it, since the rule
renames a term everywhere at once.

End the report with this line, and nothing after it:

Apply these renames? Say yes, or name the rows to apply.

## 5. On the user's yes

Apply the renames the user named, or all of them for a plain yes. Change
each name everywhere it appears: definition, call sites, tests, and
documents. Run the project's tests when it has them, and report what
changed.
