# review-internal-names eval

From the repository root:

    evals/run_review.sh with_skill|without_skill review-internal-names feedfetch [OUT_DIR]

`feedfetch/` is a small library with 10 bad and 10 good internal names,
listed in `feedfetch.expected.json`. `MODEL` defaults to
`claude-opus-5-5`.

Bar: at least 8 of 10 bad names flagged, at most 2 of 10 good, every
first cell one bare name, the report ending with the offer, and the
fixture unchanged.

2026-10-10, claude-opus-5-5: with the skill, 3 of 3 runs pass (bad
10/10, good 1/10 in each). Without it: bad 6/10, good 1/10, 6 first
cells not bare, no offer: fail.
