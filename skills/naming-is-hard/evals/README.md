# naming-is-hard evals

## Rename eval

`run.sh with_skill|without_skill [OUT_DIR]` asks a headless session to
rename 17 commands of dokidlc-iirc at 1c4bd16. `IIRC_REPO` names a
dokidlc-iirc clone (default `~/Code/agents/dokidlc-iirc`); `MODEL`
defaults to `claude-opus-5-5`.

`score.py` grades the report two ways. Exact: the name equals the
creator's name in `answer-key.md`. Acceptable: an exact match, or a name
that at least two of three judge calls (`claude -p --model
claude-fable-5-1`) accept. A call accepts a name when it passes the
rule's four Done when checks and reads to a newcomer the same way as the
creator's name. The judge gets `naming-rule.md`, `items.json` (what each
item does), the creator's name, and the proposed name, and never the run
or arm. A judge failure exits 3 with no score. A New cell that is not one
bare name fails the run. `run.sh` exits non-zero on a claude failure, a
read outside the run directory, a format failure, or a run under 14
acceptable; `bar.py OUT_DIR...` checks the mean.

Bar: with the skill, a mean of at least 14 of 17 acceptable over six
runs. Exact matches are reported beside it.

Scores, acceptable / exact, scored on 2026-10-10 by the voting judge
against the rule as of "Existing terms are checked first". Runs used
claude-opus-5-5.

| Run | Acceptable | Exact |
|---|---|---|
| Creator's run 0, no rule | 1 | 0 (format fail) |
| Creator's run 1, first draft (16 items) | 10 | 8 |
| Creator's run 2, second draft | 15 | 9 |
| Skill, existing terms first, earlier runs 1 to 3, rescored | 14, 15, 15 | 8, 9, 11 |
| Skill, existing terms first, new runs 1 to 3 | 11, 11, 14 (mean 12.0, bar not met) | 10, 9, 9 |
| Skill, audience over config, runs 1 to 6 | 8, 14, 15, 10, 13, 11 (mean 11.8, bar not met) | 8, 12, 11, 9, 7, 9 |

In the existing-terms new runs 1 and 2, the threshold commands became `show-distance-limits`
and its family. The judge rejected that family 0 of 3 times each,
which costs three to four items at once.

The last row uses the rule as of "Names people read follow the
audience, not the config". Runs 1 and 6 kept "recall" across the
threshold and tuning commands, citing the user docs, which say "recall
distances"; run 4 used `max-distances`. The judge rejected each family
0 of 3 times.

## Trigger eval

`trigger-eval.json` holds 10 prompts that should load the skill and 10
that should not. Run it with agent-builder's `scripts/trigger_eval.py`
from a scratch directory that holds only `.claude/`:

    python3 trigger_eval.py --eval-set trigger-eval.json \
      --skill-path skills/naming-is-hard --num-workers 1 \
      --runs-per-query 1 --model claude-opus-5-5

Bar: at least 8 of 10 load it, at most 1 of 10 others.

2026-10-10, claude-opus-5-5: 10 of 10 loaded, 0 of 10 others.
