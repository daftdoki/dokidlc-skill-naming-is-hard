---
name: naming-is-hard
description: Naming rule for software, so a person understands each name on first read. Use before you name or rename a command, subcommand, flag, setting, config key, slash command, or other name a person types or reads in a program, and when asked to propose such names.
argument-hint: "[DESCRIPTION]"
---

# Naming is hard

The rule is in [references/naming-rule.md](references/naming-rule.md). Read all of it before you propose the first name. Every name you make answers to every section.

When the user typed `/naming-is-hard DESCRIPTION`, the DESCRIPTION says what needs names. Without one, name what the current task is creating or renaming.

## Steps

1. Learn what each thing does when it runs: what it reads, changes, writes, or prints. Read the code when there is code. Note the words the interface already shows the person on screen and in output, and the project's existing terms.
2. Settle the project's existing terms first (Existing terms first). Then draft each name from the rule: its shape (The shape), its head noun and the words in front of it (The object), and each word's role, audience, and meanings in the field (The words).
3. Check every name against the four checks in Done when. A name that fails one goes back to step 2. When you rename a word, rename it in every name that uses it.
4. Report one row per name: the name, its kind (command, subcommand, flag, or setting), what it does in one line, and the rule section that decided it, by heading and the line that applied (for example "The object: end on the head noun"). When the caller fixes a report shape, put the section in its reason column.

The work is done when every name passes all four checks and every row cites a section.

