# naming-is-hard evals

## Rename eval

`run.sh with_skill|without_skill [OUT_DIR]` asks a headless session to
rename 17 commands of dokidlc-iirc at 1c4bd16 and scores the report
against `answer-key.md` by exact name. `IIRC_REPO` names a dokidlc-iirc
clone (default `~/Code/agents/dokidlc-iirc`); `MODEL` defaults to
`claude-opus-5-5`. A New cell that is not one bare name fails the run.

Bar: with the skill, the mean of three runs is at least 10 of 17.

2026-10-10, claude-opus-5-5, after the rule moved into one file: with
the skill 7, 9, and 12 of 17 (mean 9.3, bar not met); without 0 of 17.
Format ok in every run.

## Trigger eval

`trigger-eval.json` holds 10 prompts that should load the skill and 10
that should not. Run it with agent-builder's `scripts/trigger_eval.py`
from a scratch directory that holds only `.claude/`:

    python3 trigger_eval.py --eval-set trigger-eval.json \
      --skill-path skills/naming-is-hard --num-workers 1 \
      --runs-per-query 1 --model claude-opus-5-5

Bar: at least 8 of 10 load it, at most 1 of 10 others.

2026-10-10, claude-opus-5-5: 10 of 10 loaded, 0 of 10 others.
