#!/usr/bin/env bash
# Install Loop suite Cursor skills into a target project's .cursor/skills/
# for manual /slash invocation (e.g. /architecture-first-solution, /sync-docs-and-commit).
#
# Usage:
#   ./scripts/install-cursor-skills.sh                 # git root of cwd
#   ./scripts/install-cursor-skills.sh /path/to/repo
#   ./scripts/install-cursor-skills.sh --list
#   ./scripts/install-cursor-skills.sh --only NAME [/path/to/repo]
#   ./scripts/install-cursor-skills.sh --dry-run [/path/to/repo]
set -euo pipefail

SUITE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SRC="${SUITE_ROOT}/skills"

LIST=0
DRY=0
ONLY=""
DEST_ARG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --list) LIST=1; shift ;;
    --dry-run) DRY=1; shift ;;
    --only)
      ONLY="${2:-}"
      if [[ -z "$ONLY" ]]; then
        echo "error: --only requires a skill directory name" >&2
        exit 2
      fi
      shift 2
      ;;
    -h|--help)
      sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      DEST_ARG="$1"
      shift
      ;;
  esac
done

if [[ ! -d "$SKILLS_SRC" ]]; then
  echo "error: skills source missing: $SKILLS_SRC" >&2
  exit 1
fi

if [[ "$LIST" -eq 1 ]]; then
  echo "Available skills in $SKILLS_SRC:"
  find "$SKILLS_SRC" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort
  exit 0
fi

if [[ -n "$DEST_ARG" ]]; then
  DEST_ROOT="$(cd "$DEST_ARG" && pwd)"
else
  DEST_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
fi

DEST_SKILLS="${DEST_ROOT}/.cursor/skills"
mkdir -p "$DEST_SKILLS"

copy_one() {
  local name="$1"
  local src="${SKILLS_SRC}/${name}"
  local dst="${DEST_SKILLS}/${name}"
  if [[ ! -d "$src" ]]; then
    echo "error: unknown skill: $name" >&2
    exit 1
  fi
  if [[ ! -f "${src}/SKILL.md" ]]; then
    echo "error: missing SKILL.md in $src" >&2
    exit 1
  fi
  if [[ "$DRY" -eq 1 ]]; then
    echo "dry-run: rsync $src/ -> $dst/"
    return
  fi
  mkdir -p "$dst"
  rsync -a --delete "${src}/" "${dst}/"
  echo "installed: $name -> $dst"
}

if [[ -n "$ONLY" ]]; then
  copy_one "$ONLY"
else
  while IFS= read -r name; do
    copy_one "$name"
  done < <(find "$SKILLS_SRC" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
fi

if [[ "$DRY" -eq 0 ]]; then
  echo "done. Cursor project skills: $DEST_SKILLS"
  echo "Invoke manually in chat, e.g. /sync-docs-and-commit or /architecture-first-solution"
fi
