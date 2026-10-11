#!/bin/sh
# One headless rename run, scored against the creator's iirc decisions.
# Exits non-zero when claude fails, a tool call reaches outside the run
# directory, the format check fails, or the run has fewer than 14
# acceptable names; bar.py checks the mean over six runs.
#   run.sh with_skill|without_skill [OUT_DIR]
# Exports dokidlc-iirc at 1c4bd16 into a temporary directory and runs
# one claude -p session there on task.md. Both arms use
# --setting-sources "", so no user plugins, settings, or CLAUDE.md reach
# the session, and only Read, Glob, and Grep are allowed. The with_skill
# arm adds a copy of this plugin without its evals/ directories by
# --plugin-dir, and the prompt names the copied SKILL.md, because a
# headless session does not load a skill on its own. The session never
# sees answer-key.md. Writes stream.jsonl, report.md, and score.txt to
# OUT_DIR (default: a new temporary directory, kept), then prints the
# score line.
# Env: IIRC_REPO (a dokidlc-iirc clone, default ~/Code/agents/dokidlc-iirc),
# MODEL (default claude-opus-5-5).
set -eu
E=$(cd "$(dirname "$0")" && pwd)
PLUGIN=$(cd "$E/../../.." && pwd)
usage="usage: run.sh with_skill|without_skill [OUT_DIR]"
arm=${1:?$usage}; out=${2:-$(mktemp -d)}
IIRC_REPO=${IIRC_REPO:-$HOME/Code/agents/dokidlc-iirc}
MODEL=${MODEL:-claude-opus-5-5}
COMMIT=1c4bd16

mkdir -p "$out"
out=$(cd "$out" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/code" "$tmp/state"
git -C "$IIRC_REPO" archive "$COMMIT" | tar -x -C "$tmp/code"

prompt=$(cat "$E/task.md")
extra=""
case "$arm" in
  with_skill)
    mkdir -p "$tmp/plugin"
    (cd "$PLUGIN" && tar -c --exclude .git --exclude evals .) | tar -x -C "$tmp/plugin"
    skill="$tmp/plugin/skills/naming-is-hard/SKILL.md"
    [ -f "$skill" ] || { echo "no SKILL.md in $PLUGIN" >&2; exit 2; }
    extra="--plugin-dir $tmp/plugin"
    prompt="Before you start, read the naming-is-hard skill at $skill and follow it.

$prompt" ;;
  without_skill) ;;
  *) echo "$usage" >&2; exit 2 ;;
esac

# The parent shell may carry installed plugin bin directories on PATH.
path=$(printf %s "$PATH" | tr : '\n' | grep -v '/.claude/plugins/cache/' | paste -sd: -)

cd "$tmp/code"
# shellcheck disable=SC2086
PATH=$path XDG_STATE_HOME=$tmp/state claude -p --setting-sources "" --strict-mcp-config $extra \
  --model "$MODEL" --allowedTools "Read,Glob,Grep" \
  --disallowedTools "Bash,Write,Edit,WebFetch,WebSearch,Agent" \
  --output-format stream-json --verbose "$prompt" \
  < /dev/null > "$out/stream.jsonl" 2> "$out/stderr.log" || claude_status=$?

python3 - "$out" "$arm" "$tmp" <<'PY'
import json, sys
out, arm, tmp = sys.argv[1:4]
result, reads, outside = "", [], []
for line in open(f"{out}/stream.jsonl"):
    try:
        ev = json.loads(line)
    except ValueError:
        continue
    if ev.get("type") == "result":
        result = ev.get("result") or ""
        print(f"{arm}: {ev.get('num_turns')} turns, {round(ev.get('duration_ms', 0) / 1000)}s, ${ev.get('total_cost_usd', 0):.2f}")
    for c in (ev.get("message") or {}).get("content") or []:
        if isinstance(c, dict) and c.get("type") == "tool_use":
            inp = c.get("input") or {}
            p = inp.get("file_path") or inp.get("path") or ""
            reads.append(p)
            if p.startswith("/") and not p.startswith(tmp) and not p.startswith("/private" + tmp):
                outside.append(f"{c.get('name')} {p}")
open(f"{out}/report.md", "w").write(result)
if arm == "with_skill" and not any(p.endswith("naming-is-hard/SKILL.md") for p in reads):
    print("FAIL: the with_skill run never read SKILL.md", file=sys.stderr)
    sys.exit(3)
for o in outside:
    print(f"FAIL: a tool call reached outside the run directory: {o}", file=sys.stderr)
if outside:
    sys.exit(4)
PY

status=0
python3 "$E/score.py" "$out/report.md" > "$out/score.txt" || status=$?
tail -3 "$out/score.txt"
if [ "${claude_status:-0}" -ne 0 ]; then
  echo "claude exited $claude_status" | tee -a "$out/stderr.log"
  status=1
fi
echo "output: $out"
exit "$status"
