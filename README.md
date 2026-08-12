---
title: "AgenticLoopDev（dev/loop）"
type: index
status: accepted
phase: N/A
updated: 2026-08-12
summary: "Loop 套件入口 — workflow / playbook / skills；消费方可作 submodule；gate 策略通用、命令在消费仓。"
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

## Quality gates

套件内只写**通用策略**（何时跑、冷却、verify-only）→ [health-gates.md](health-gates.md)。  
**具体命令与 ADR 不进本目录**（见 [porting.md](porting.md) / [INDEX.md](INDEX.md)）：

| 位置 | 职责 |
|------|------|
| 消费仓 `dev/progress/health-gates.md` | 集成编译、聚焦 / grand gate 命令 |
| 消费仓根 `AGENTS.md` | 仓库级禁止项与门禁权威 |

远端 CI 是否启用由消费仓自定；套件叙述默认按**本地门禁**，不绑定某一仓库的脚本名或 ADR 编号。
