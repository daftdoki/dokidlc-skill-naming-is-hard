# naming-is-hard

Names a person understands on first read: a Claude Code plugin with a naming rule and two name reviews.

The plugin's name nods to the old quip: there are only two hard things in computer science, cache invalidation, naming things, and off-by-one errors. This plugin takes on the second. The repository is `dokidlc-skill-naming-is-hard` because it belongs to the dokidlc family; the plugin you install is `naming-is-hard`.

The main skill is a rule Claude follows while it names commands, subcommands, flags, settings, and other parts of software. It loads by itself when Claude is naming something. To ask for names directly, type `/naming-is-hard:naming-is-hard DESCRIPTION`; Claude Code 2.1.296 also accepts `/naming-is-hard DESCRIPTION`. You get one row per name with its kind, what it does, and the rule section that decided it. The rule's examples come from `bak`, a made-up backup tool.

Two reviews check names that already exist. You run them yourself; Claude never starts one on its own. `/naming-is-hard:review-internal-names [SCOPE]` reviews the names engineers read in code: functions, classes, variables, parameters, config keys, and log fields. `/naming-is-hard:review-user-facing-names [SCOPE]` reviews the names users see: commands, flags, settings, labels, and output fields, judged for expert or lay users. Without a scope, a review reads the current diff. Each one reports a table of failed names with a proposed rename, then asks before it changes a file.

## Why this one

In the rename eval, an agent with no rule renamed 17 commands of a real plugin and got 1 acceptable name. With this skill it got a mean of 13.7 of 17 over six runs. A separate judge model graded each name and voted three times. On seeded fixtures, each review flags 10 of 10 bad names and at most 1 of 10 good ones, and it renames nothing without your yes. The evals' READMEs under `skills/*/evals/` say how each run works.

Status: experimental. It is new on 2026-10-10, it works, and so far the measurements come from one project.

## Install

```
claude plugin marketplace add daftdoki/dokidlc-plugins
claude plugin install naming-is-hard@dokidlc
```

## Run it

Review the names in your uncommitted changes:

```
/naming-is-hard:review-user-facing-names
```

The review names the audience it judged for, prints one table, worst failure first, and ends with the offer:

```
| Name | Where | Rename to | Rule section | Why |
|---|---|---|---|---|

Apply these renames? Say yes, or name the rows to apply.
```

## Caveats

- The measurements come from one plugin's 17 commands and three small fixtures. Your project may score differently.
- A review with no scope and no diff says so and stops. Pass a path or a directory to review code that is already committed.
- The rule targets names a person types or reads. It does not settle case style or formatting.

## Other docs

- [skills/naming-is-hard/references/naming-rule.md](skills/naming-is-hard/references/naming-rule.md) is the rule.
- [skills/naming-is-hard/references/review-procedure.md](skills/naming-is-hard/references/review-procedure.md) is the procedure both reviews share.
- [skills/naming-is-hard/evals/README.md](skills/naming-is-hard/evals/README.md), [skills/review-internal-names/evals/README.md](skills/review-internal-names/evals/README.md), and [skills/review-user-facing-names/evals/README.md](skills/review-user-facing-names/evals/README.md) hold the evals and their scores.

Bugs and questions go to the [issue tracker](https://github.com/daftdoki/dokidlc-skill-naming-is-hard/issues).

## License

MIT, by DaftDoki. See [LICENSE](LICENSE).
