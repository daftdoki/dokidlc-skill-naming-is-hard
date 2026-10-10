#!/bin/sh
# One headless run of /naming-is-hard:review-user-facing-names on one fixture.
#   run.sh lay|expert [OUT_DIR]
# ARM=with (default) loads this plugin by --plugin-dir; ARM=without loads
# the same plugin minus this skill, the red run. The plugin copy and the
# fixture copy live in a temporary directory; the plugin copy holds no
# evals/ directory and the fixture copy no expected.json, so the run never
# sees the answers. MODEL overrides the model. NAMING_RULE names a
# naming-rule.md to place in the copy when skills/naming-is-hard/references/
# does not have one yet.
set -eu
E=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$E/../../.." && pwd)
FIX=${1:?usage: run.sh lay|expert [OUT_DIR]}
case "$FIX" in lay|expert) ;; *) echo "fixture must be lay or expert" >&2; exit 2 ;; esac
ARM=${ARM:-with}
MODEL=${MODEL:-opus}
T=$(mktemp -d)
OUT=${2:-$T/out}
mkdir -p "$OUT" "$T/plugin"
cp -R "$ROOT/.claude-plugin" "$ROOT/skills" "$T/plugin/"
find "$T/plugin/skills" -type d -name evals -prune -exec rm -rf {} +
rule="$T/plugin/skills/naming-is-hard/references/naming-rule.md"
if [ ! -f "$rule" ] && [ -n "${NAMING_RULE:-}" ]; then
  mkdir -p "$(dirname "$rule")"; cp "$NAMING_RULE" "$rule"
fi
case "$ARM" in
  with) ;;
  without) rm -rf "$T/plugin/skills/review-user-facing-names" ;;
  *) echo "ARM must be with or without" >&2; exit 2 ;;
esac
cp -R "$E/$FIX" "$T/work"
rm "$T/work/expected.json"
cd "$T/work"
git init -q && git add -A && git -c user.name=eval -c user.email=eval@example.org commit -qm fixture
claude -p --setting-sources "" --strict-mcp-config --plugin-dir "$T/plugin" --model "$MODEL" \
  --permission-mode acceptEdits --allowedTools "Read,Grep,Glob,Bash(git *)" --output-format json \
  "/naming-is-hard:review-user-facing-names the whole repository" \
  < /dev/null > "$OUT/result.json" 2> "$OUT/stderr.log" || echo "claude exited $?" >> "$OUT/stderr.log"
python3 "$E/score.py" "$E/$FIX/expected.json" "$OUT/result.json" "$T/work" > "$OUT/score.json"
python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['summary'])" "$OUT/score.json"
echo "output: $OUT"
