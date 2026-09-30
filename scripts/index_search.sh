#!/usr/bin/env bash
# Print "start end" line ranges of ```{python} code bodies, excluding #| lines
awk '
  /^```\{python\}/ { inblk=1; start=0; next }
  inblk && /^```/  { if (start) print start, NR-1; inblk=0; next }
  inblk {
    if ($0 ~ /^#\|/) next      # skip chunk-option lines
    if (start == 0) start = NR # first real code line
  }
' "$1"
