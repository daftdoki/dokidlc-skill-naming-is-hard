---
name: review-internal-names
description: Review the names engineers read in code (functions, classes, variables, parameters, config keys, log fields) against the naming rule; report, then offer to apply the renames.
argument-hint: "[SCOPE]"
disable-model-invocation: true
---

# Review internal names

Scope: $ARGUMENTS

## 1. Read the rule and the procedure

Read both files in `../naming-is-hard/references/`, relative to this
skill's base directory: `naming-rule.md`, the standard, and
`review-procedure.md`, the steps every name review shares. Settle the
scope as its Scope section says. Code names map to the rule through its
section Outside a command line.

## 2. Collect the names

List every name the scope defines: modules, classes, functions,
methods, parameters, module-level variables and constants, attributes,
config keys, log event names, and environment variables. Include a
local variable whose name says nothing about what it holds (`data2`,
`tmp`); leave out the conventional short locals (`i`, `e`, `err`, `f`).

## 3. Judge, report, apply

Read each name as the project's engineers read it. Then follow the
procedure's Judge, Report, and On the user's yes sections. The report's
one header line is `Scope:`.
