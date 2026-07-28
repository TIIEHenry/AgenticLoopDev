#!/usr/bin/env bash
# Install portable Loop Cursor skills for manual invocation.
#
# Destinations:
#   --personal     ~/.cursor/skills/   (all local Cursor projects)
#   <repo-path>    <repo>/.cursor/skills/
#   (default)      consumer repo root when suite lives at <repo>/dev/loop;
#                  else git superproject / toplevel of cwd
#
# Usage:
#   ./scripts/install-cursor-skills.sh --personal
#   ./scripts/install-cursor-skills.sh /path/to/AnyRepo
#   ./scripts/install-cursor-skills.sh                 # auto-detect consumer
#   ./scripts/install-cursor-skills.sh --only NAME [--personal|/path]
#   ./scripts/install-cursor-skills.sh --list
#   ./scripts/install-cursor-skills.sh --dry-run [--personal|/path]
set -euo pipefail

SUITE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SRC="${SUITE_ROOT}/skills"

LIST=0
DRY=0
PERSONAL=0
ONLY=""
DEST_ARG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --list) LIST=1; shift ;;
    --dry-run) DRY=1; shift ;;
    --personal) PERSONAL=1; shift ;;
    --only)
      ONLY="${2:-}"
      if [[ -z "$ONLY" ]]; then
        echo "error: --only requires a skill directory name" >&2
        exit 2
      fi
      shift 2
      ;;
    -h|--help)
      sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'
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

list_skill_names() {
  # Portable (no GNU find -printf)
  local d
  for d in "$SKILLS_SRC"/*/; do
    [[ -d "$d" ]] || continue
    basename "$d"
  done | sort
}

if [[ "$LIST" -eq 1 ]]; then
  echo "Available skills in $SKILLS_SRC:"
  list_skill_names
  exit 0
fi

detect_default_dest() {
  # Suite nested as <consumer>/dev/loop → install into <consumer>
  local parent_dev parent_repo
  parent_dev="$(dirname "$SUITE_ROOT")"
  parent_repo="$(dirname "$parent_dev")"
  if [[ "$(basename "$SUITE_ROOT")" == "loop" && "$(basename "$parent_dev")" == "dev" ]]; then
    if git -C "$parent_repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      echo "$parent_repo"
      return
    fi
  fi
  # Running inside a submodule: prefer superproject
  local super
  super="$(git -C "$SUITE_ROOT" rev-parse --show-superproject-working-tree 2>/dev/null || true)"
  if [[ -n "${super:-}" ]]; then
    echo "$super"
    return
  fi
  # Fallback: cwd git root (may be the suite repo itself when developing AgenticLoopDev alone)
  if git rev-parse --show-toplevel >/dev/null 2>&1; then
    git rev-parse --show-toplevel
    return
  fi
  echo "$SUITE_ROOT"
}

if [[ "$PERSONAL" -eq 1 ]]; then
  if [[ -n "$DEST_ARG" ]]; then
    echo "error: --personal cannot be combined with a repo path" >&2
    exit 2
  fi
  DEST_SKILLS="${HOME}/.cursor/skills"
else
  if [[ -n "$DEST_ARG" ]]; then
    DEST_ROOT="$(cd "$DEST_ARG" && pwd)"
  else
    DEST_ROOT="$(detect_default_dest)"
  fi
  DEST_SKILLS="${DEST_ROOT}/.cursor/skills"
fi

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
    [[ -n "$name" ]] || continue
    copy_one "$name"
  done < <(list_skill_names)
fi

if [[ "$DRY" -eq 0 ]]; then
  echo "done. Cursor skills dir: $DEST_SKILLS"
  if [[ "$PERSONAL" -eq 1 ]]; then
    echo "scope: personal (~/.cursor/skills) — available in all local Cursor projects"
  else
    echo "scope: project — share via git if the team wants the same skills"
  fi
  echo "invoke: /architecture-first-solution  or  /sync-docs-and-commit"
fi
