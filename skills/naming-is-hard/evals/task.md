You are naming commands for a command-line tool. Work only from the tool's code and docs in the current directory, and read nothing outside it.

The tool is `iirc`, a Claude Code plugin that keeps notes ("pages") past sessions wrote and suggests matching pages when the user types a prompt. The CLI is `bin/iirc` (Python, argparse at the bottom). The slash command `/iirc ARGS` is handled in `hooks/register.tsx`, which also draws what the person sees on screen. The docs are in `docs/` (USAGE.md lists every command; UI.md shows the screen) and `skills/iirc/`.

Task: these names are unclear to a person reading them for the first time. Propose a new name for each item below. Read the code and docs enough to know what each one really does when it runs: what it reads, changes, writes, or prints. Do not edit any file. If you rename a word used across several items, name that word's replacement once and use it consistently.

Items:

1. CLI `iirc doubt`
2. CLI `iirc cost`
3. CLI `iirc knobs`
4. CLI `iirc knobs set NAME VALUE`
5. slash command `/iirc open`
6. slash command `/iirc status-line [on|off]`
7. CLI and slash `max-suggested [N]`
8. CLI `iirc setup`
9. CLI `iirc stats`
10. CLI `iirc index`
11. the `--vectors` flag of `iirc index`
12. CLI `iirc tune`
13. its subcommand `tune gather`
14. its subcommand `tune judge`
15. its subcommand `tune sweep`
16. its subcommand `tune done`
17. CLI `iirc recall` (the hook entry the plugin's hooks call)

Report as one markdown table with exactly these columns, one row per item, in the order above:

| # | Old | New | Kind | Why |

- `#` is the item's number.
- `New` holds one name in backticks: no program name, no parent command, no arguments. Write a flag with its leading dashes.
- `Kind` is command, subcommand, flag, or setting.
- `Why` says in one line what the item does, from the code, and what decided the name.

After the table, list any word you renamed across items, and any item where two names seemed equally good. Keep the report under 800 words.
