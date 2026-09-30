#!/usr/bin/env bash
set -euo pipefail

qmd="${1:?usage: get_code_file.sh <path/to/file.qmd>}"
to_debug="${2:-0}"

# 1) Pull just the YAML front matter (between the first two '---' lines).
# 2) From that, extract the value of `code-file:` (only the first match).
var_block=$(awk '/^---$/{c++; next} c==1' "$qmd")
code_file=$(printf '%s\n' "$var_block" | grep -m1 '^code-file:' | sed 's/^code-file:[[:space:]]*//')

if [[ "$to_debug" == "1" ]]; then
  printf 'YAML block:\n%s\n' "$var_block" 
  printf "\n"
  printf 'code-file: \n%s' "$code_file"
fi

printf code_file

