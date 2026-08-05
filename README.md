---
title: "AgenticLoopDev（dev/loop）"
type: index
status: accepted
phase: N/A
updated: 2026-08-03
summary: "Loop 套件入口 — workflow / playbook / skills；消费方可作 submodule；本仓库以本地门禁替代远端 CI。"
---

# AgenticLoopDev

This repository is the loop suite itself.

Its repository root directly corresponds to the previous `dev/loop/` folder
contents so downstream projects can consume it as a submodule at `dev/loop/`.

Runtime state such as `loop.pid`, locks, caches, and local logs should live in
`dev/loop/.runtime/` inside the consumer repository and stay ignored by git.

## Cursor skills (manual invoke)

SSOT: `skills/<name>/SKILL.md`. Install only creates symlink/pointer — **no reinstall** when the suite changes.

```bash
./scripts/install-cursor-skills.sh --personal          # @dev/loop/skills/... per workspace
./scripts/install-cursor-skills.sh /path/to/AnyRepo  # symlink into that repo
```

Or `@dev/loop/skills/sync-docs-and-commit/SKILL.md` directly.
See `skills/INDEX.md`.

## Quality gates（本仓）

ImageKit **禁用远端 CI**（无 `.github/workflows`，禁止擅自启用）。验收载体为本地
`./scripts/check-all-gates.sh`、pre-commit 与 merge 槽集成编译 — 见
[health-gates.md](../progress/health-gates.md) 与 [AGENTS.md](../../AGENTS.md)。
