#!/bin/sh
# One headless run of a name review on one fixture, then its score.
#   run_review.sh with_skill|without_skill SKILL FIXTURE [OUT_DIR]
# SKILL is review-internal-names or review-user-facing-names. FIXTURE is
# a directory in skills/SKILL/evals/; its answers are FIXTURE.expected.json
# beside it, outside the fixture. The run gets a copy of this plugin made
# without any evals/ directory, and a git repository holding a copy of
# the fixture, both in a temporary directory, so it never sees the
# answers. The without_skill arm deletes SKILL from the plugin copy.
# Writes result.json, stderr.log, and score.json to OUT_DIR (default: a
# new temporary directory, kept), then prints the summary line.
# Env: MODEL (default claude-opus-5-5).
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
usage="usage: run_review.sh with_skill|without_skill SKILL FIXTURE [OUT_DIR]"
arm=${1:?$usage}; skill=${2:?$usage}; fixture=${3:?$usage}
MODEL=${MODEL:-claude-opus-5-5}
E="$ROOT/skills/$skill/evals"
expected="$E/$fixture.expected.json"
[ -d "$E/$fixture" ] && [ -f "$expected" ] || { echo "no fixture $E/$fixture with $expected" >&2; exit 2; }

out=${4:-$(mktemp -d)}
mkdir -p "$out"
out=$(cd "$out" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/plugin" "$tmp/state"
(cd "$ROOT" && tar -c --exclude .git --exclude evals .) | tar -x -C "$tmp/plugin"
case "$arm" in
  with_skill) ;;
  without_skill) rm -rf "$tmp/plugin/skills/$skill" ;;
  *) echo "$usage" >&2; exit 2 ;;
esac
cp -R "$E/$fixture" "$tmp/work"
cd "$tmp/work"
git init -q && git add -A && git -c user.name=eval -c user.email=eval@example.org commit -qm fixture

# The parent shell may carry installed plugin bin directories on PATH.
path=$(printf %s "$PATH" | tr : '\n' | grep -v '/.claude/plugins/cache/' | paste -sd: -)
PATH=$path XDG_STATE_HOME=$tmp/state claude -p --setting-sources "" --strict-mcp-config \
  --plugin-dir "$tmp/plugin" --model "$MODEL" \
  --permission-mode acceptEdits --allowedTools "Read,Grep,Glob,Bash(git *)" --output-format json \
  "/naming-is-hard:$skill the whole repository" \
  < /dev/null > "$out/result.json" 2> "$out/stderr.log" || echo "claude exited $?" >> "$out/stderr.log"

python3 "$ROOT/evals/score_review.py" "$expected" "$out/result.json" "$tmp/work" > "$out/score.json"
python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['summary'])" "$out/score.json"
echo "output: $out"
