# review-user-facing-names eval

From the repository root:

    evals/run_review.sh with_skill|without_skill review-user-facing-names lay|expert [OUT_DIR]

`lay/` is a recipe tool for home cooks and `expert/` a PostgreSQL tool
for database administrators, each with 10 bad and 10 good user-facing
names, listed in `lay.expected.json` and `expert.expected.json`. `MODEL`
defaults to `claude-opus-5-5`.

Bar: the bar of review-internal-names, plus the fixture's audience named
in an `Audience:` line.

2026-10-10, against the rule at dde07b1, claude-opus-5-5, with the skill: lay 3 of 3 pass (bad
10/10, good 0/10 in each); expert 3 of 3 pass (bad 10/10, good 0/10 in
each). Without it: lay bad 8/10, good 1/10, 4 first cells not bare, no
offer, no audience: fail; expert bad 7/10, good 7/10, 7 first cells not
bare, no offer, no audience: fail.

Rerun at 0e392b9 on 2026-10-10 by the implementation review: every
fixture passes again.
