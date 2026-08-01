#!/bin/bash
set -euo pipefail

tests_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd -- "$tests_dir/.." && pwd)"

run() {
  printf '==> '
  printf '%q ' "$@"
  printf '\n'
  "$@"
}

cd "$repo_dir"
run latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

cd "$tests_dir"
export TEXINPUTS="$repo_dir:${TEXINPUTS:-}"
run latexmk -pdf -interaction=nonstopmode -halt-on-error \
  table1-compliance.tex
run python3 "$tests_dir/check_rendered_pdfs.py"
run python3 "$tests_dir/check_overleaf_archive.py"

printf '==> Alle relevanten Vorlagenprüfungen bestanden\n'
