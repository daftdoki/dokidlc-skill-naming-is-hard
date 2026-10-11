# Answer key: the creator's iirc rename decisions, 2026-10-10

For the rename eval. Each row is the creator's final name for a command,
flag, or setting of dokidlc-iirc at 1c4bd16, before any rename. The
first 17 rows are the items the two test runs named; run 2 matched 9.

| # | At 1c4bd16 | Creator's name | Kind |
|---|---|---|---|
| 1 | `doubt` | `find-suspect-pages` | command |
| 2 | `cost` | `estimate-context-tokens` | command |
| 3 | `knobs` | `show-suggestion-thresholds` | command |
| 4 | `knobs set NAME VALUE` | `set-suggestion-threshold` | command |
| 5 | `/iirc open` | `unfold-suggested-pages` | slash command |
| 6 | `/iirc status-line` | `summary-line-visibility` | setting |
| 7 | `max-suggested` | `max-suggested-pages` | setting |
| 8 | `setup` | `set-search-backend` | command |
| 9 | `stats` | `summarize-page-usage` | command |
| 10 | `index` | `rebuild-search-index` | command |
| 11 | `index --vectors` | `--vectors-only` | flag |
| 12 | `tune` | `tune-suggestions` | command group |
| 13 | `tune gather` | `gather-suggestion-data` | subcommand |
| 14 | `tune judge` | `record-relevance-judgments` | subcommand |
| 15 | `tune sweep` | `evaluate-suggestion-thresholds` | subcommand |
| 16 | `tune done` | `mark-session-tuned` | subcommand |
| 17 | `recall` | `suggest-pages` | command (hook entry) |
| 18 | `tune sweep --replay` | `--replay-prompts` | flag |
| 19 | `stats --snapshot` | `record-session-summary` | command |
| 20 | `stats --session` | `summarize-session-usage` | command |
| 21 | `recall --success` | `record-command-success` | command |
| 22 | `nudge --stop`, `nudge --compact` | `remind-to-write --at stop\|compaction` | command |
| 23 | `nudge --summary` | `show-compaction-instructions` | command |
| 24 | `pull` | `read-matching-pages` | command |
| 25 | `approve` | `approve-page-check` | command |
| 26 | `stores` | `show-page-stores` | command |
| 27 | `stores add` | `add-remote-store` | command |
| 28 | `topics` | `show-page-topics` | command |
| 29 | `audit` | `audit-page-findability` | command |

Kept by the creator: `read`, `write`, `delete`, `verify`, `search`, the
CLI `show`, `/iirc show`, `/iirc reader`, `/iirc status`, `/iirc demo`.
Left for later, not scored: `doctor` and its flags, `init`, `help`,
`sync`, `migrate`.

The config table `[recall.MODEL-ID]` becomes `[suggestions.MODEL-ID]`;
the word "recall" leaves every name.
