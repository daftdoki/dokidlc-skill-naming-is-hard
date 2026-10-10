# naming-is-hard evals

## Rename eval

`run.sh with_skill|without_skill [OUT_DIR]` asks a headless session to
rename 17 commands of dokidlc-iirc at 1c4bd16. `IIRC_REPO` names a
dokidlc-iirc clone (default `~/Code/agents/dokidlc-iirc`); `MODEL`
defaults to `claude-opus-5-5`.

`score.py` grades the report two ways. Exact: the name equals the
creator's name in `answer-key.md`. Acceptable: an exact match, or a name
that a judge (`claude -p --model claude-fable-5-1`) says passes the
rule's four Done when checks and reads to a newcomer the same way as the
creator's name. The judge gets `naming-rule.md`, `items.json` (what
each item does), the creator's name, and the proposed name, and never
the run or arm. A New cell that is not one bare name fails the run.
`run.sh` exits non-zero on a format failure or a run under 14
acceptable; `bar.py OUT_DIR...` checks the mean.

Bar: with the skill, a mean of at least 14 of 17 acceptable over three
runs. Exact matches are reported beside it.

Scores, acceptable / exact, all rescored on 2026-10-10 by the same judge
against the rule as of "Existing terms are checked first":

| Run | Acceptable | Exact |
|---|---|---|
| Creator's run 0, no rule | 1 | 0 (format fail) |
| Creator's run 1, first draft (16 items) | 11 | 8 |
| Creator's run 2, second draft | 15 | 9 |
| Skill, first build, runs 1 to 3 | 10, 10, 15 | 9, 8, 13 |
| Skill, after the rule moved, runs 1 to 3 | 8, 11, 13 | 7, 9, 12 |
| Skill, existing terms first, runs 1 to 3 | 14, 14, 14 (mean 14.0, bar met) | 8, 9, 11 |
| Without the skill, existing terms first | 1 | 0 |

The runs used claude-opus-5-5. The judge varies between calls: it
accepted `session-line-visibility` in one call and rejected it in
another.

## Trigger eval

`trigger-eval.json` holds 10 prompts that should load the skill and 10
that should not. Run it with agent-builder's `scripts/trigger_eval.py`
from a scratch directory that holds only `.claude/`:

    python3 trigger_eval.py --eval-set trigger-eval.json \
      --skill-path skills/naming-is-hard --num-workers 1 \
      --runs-per-query 1 --model claude-opus-5-5

Bar: at least 8 of 10 load it, at most 1 of 10 others.

2026-10-10, claude-opus-5-5: 10 of 10 loaded, 0 of 10 others.
