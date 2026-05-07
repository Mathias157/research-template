#!/bin/bash
# compile.sh — Local LaTeX compile + view workflow
# Usage: ./compile.sh [-f]
# -f : force clean rebuild

set -e

cd "$(dirname "$0")"
name="main"

if [ "${1}" == "-f" ]; then
  echo "Force clean rebuild..."
  latexmk -c
  latexmk -pdf -f "${name}.tex"
else
  latexmk -pdf "${name}.tex"
fi

# Check if zathura is running
if pgrep -x "zathura" >/dev/null; then
  echo "zathura is running, attempting to refresh existing tab..."
  # Focus zathura and refresh (zathura reloads on file change by default)
  hyprctl dispatch focuswindow "class:org.pwmt.zathura" 2>/dev/null || true
else
  echo "zathura not running, opening new instance..."
  nohup zathura ../build/${name}.pdf >/dev/null 2>&1 &
  sleep 0.3
fi
