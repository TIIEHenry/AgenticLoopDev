#!/usr/bin/env bash
# Point Cursor skills at Loop suite SKILL.md (no content copy).
# Loop updates → no reinstall. Project: relative symlink. Personal: thin @ pointer.
#
# Usage:
#   ./scripts/install-cursor-skills.sh --personal
#   ./scripts/install-cursor-skills.sh /path/to/AnyRepo
#   ./scripts/install-cursor-skills.sh                 # auto-detect consumer
#   ./scripts/install-cursor-skills.sh --only NAME [...]
#   ./scripts/install-cursor-skills.sh --list
#   ./scripts/install-cursor-skills.sh --dry-run [...]
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
      sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
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
  local d
  for d in "$SKILLS_SRC"/*/; do
    [[ -d "$d" ]] || continue
    basename "$d"
  done | sort
}

skill_disable_model_invocation() {
  python3 - "$1" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
if not m:
    print("false")
    sys.exit(0)
block = m.group(1)
sm = re.search(r"^disable-model-invocation:\s*(true|false)\s*$", block, re.M | re.I)
print("true" if sm and sm.group(1).lower() == "true" else "false")
PY
}

skill_description() {
  # Extract YAML description (supports folded >-) from SKILL.md
  python3 - "$1" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
if not m:
    print("Loop suite skill; follow SSOT SKILL.md in the workspace.")
    sys.exit(0)
block = m.group(1)
# folded description: description: >-\n  line\n  line
fm = re.search(r"^description:\s*>-?\s*\n((?:[ \t]+.+\n)+)", block, re.M)
if fm:
    lines = [re.sub(r"^[ \t]+", "", ln) for ln in fm.group(1).splitlines() if ln.strip()]
    print(" ".join(lines).strip())
    sys.exit(0)
sm = re.search(r"^description:\s*[>|]?-?\s*(.+)$", block, re.M)
if sm and not sm.group(1).startswith(">") and sm.group(1).strip():
    print(sm.group(1).strip())
else:
    print("Loop suite skill; follow SSOT SKILL.md in the workspace.")
PY
}

relpath_to() {
  python3 -c 'import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))' "$1" "$2"
}

if [[ "$LIST" -eq 1 ]]; then
  echo "Available skills in $SKILLS_SRC:"
  list_skill_names
  exit 0
fi

detect_default_dest() {
  local parent_dev parent_repo
  parent_dev="$(dirname "$SUITE_ROOT")"
  parent_repo="$(dirname "$parent_dev")"
  if [[ "$(basename "$SUITE_ROOT")" == "loop" && "$(basename "$parent_dev")" == "dev" ]]; then
    if git -C "$parent_repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      echo "$parent_repo"
      return
    fi
  fi
  local super
  super="$(git -C "$SUITE_ROOT" rev-parse --show-superproject-working-tree 2>/dev/null || true)"
  if [[ -n "${super:-}" ]]; then
    echo "$super"
    return
  fi
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

install_symlink() {
  local name="$1"
  local src="${SKILLS_SRC}/${name}"
  local dst="${DEST_SKILLS}/${name}"
  local rel
  rel="$(relpath_to "$src" "$DEST_SKILLS")"
  if [[ "$DRY" -eq 1 ]]; then
    echo "dry-run: symlink $dst -> $rel  (SSOT $src)"
    return
  fi
  rm -rf "$dst"
  ln -sfn "$rel" "$dst"
  echo "linked: $dst -> $rel"
}

install_personal_pointer() {
  local name="$1"
  local src="${SKILLS_SRC}/${name}/SKILL.md"
  local dst_dir="${DEST_SKILLS}/${name}"
  local dst="${dst_dir}/SKILL.md"
  local desc
  local dmi
  local dmi_line=""
  local ssot_path="dev/loop/skills/${name}/SKILL.md"
  desc="$(skill_description "$src")"
  dmi="$(skill_disable_model_invocation "$src")"
  if [[ "$dmi" == "true" ]]; then
    dmi_line=$'\ndisable-model-invocation: true'
  fi
  if [[ "$DRY" -eq 1 ]]; then
    echo "dry-run: pointer $dst  (@${ssot_path})"
    return
  fi
  rm -rf "$dst_dir"
  mkdir -p "$dst_dir"
  cat >"$dst" <<EOF
---
name: ${name}
description: >-
  ${desc}${dmi_line}
---

# ${name}（指向 Loop SSOT）

**不要用本文件当正文。** 调用时必须：

1. 用工具 **Read** 当前工作区的 \`${ssot_path}\`（或在对话里 \`@${ssot_path}\`）
2. **严格按该 SKILL.md 全文执行**

Loop 套件更新后**无需重装**本指针。若工作区没有 \`dev/loop/skills/\`，先移植/同步 Loop，或在该仓库跑：

\`\`\`bash
./dev/loop/scripts/install-cursor-skills.sh
\`\`\`

（项目安装会创建指向套件的 symlink，同样不用每次重装。）
EOF
  echo "pointer: $dst -> @${ssot_path}"
}

install_one() {
  local name="$1"
  local src="${SKILLS_SRC}/${name}"
  if [[ ! -d "$src" ]]; then
    echo "error: unknown skill: $name" >&2
    exit 1
  fi
  if [[ ! -f "${src}/SKILL.md" ]]; then
    echo "error: missing SKILL.md in $src" >&2
    exit 1
  fi
  if [[ "$PERSONAL" -eq 1 ]]; then
    install_personal_pointer "$name"
  else
    install_symlink "$name"
  fi
}

if [[ -n "$ONLY" ]]; then
  install_one "$ONLY"
else
  while IFS= read -r name; do
    [[ -n "$name" ]] || continue
    install_one "$name"
  done < <(list_skill_names)
fi

if [[ "$DRY" -eq 0 ]]; then
  echo "done. Cursor skills dir: $DEST_SKILLS"
  if [[ "$PERSONAL" -eq 1 ]]; then
    echo "mode: personal pointers → @dev/loop/skills/<name>/SKILL.md (per workspace)"
  else
    echo "mode: symlinks → loop suite skills (updates apply without reinstall)"
  fi
  echo "invoke: /architecture-first-solution  or  /sync-docs-and-commit"
fi
