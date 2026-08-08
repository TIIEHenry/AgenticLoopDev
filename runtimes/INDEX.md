---
title: "Loop 运行时选型"
type: guide
status: accepted
phase: N/A
updated: 2026-08-07
summary: "Cursor / Grok CLI / Claude Code / Qoder / Codex / OpenCode 运行时对比；架构优先 grok -p；Opus 4.6 写作须 --model。"
---

# Loop 运行时选型

**语义层**（workflow、playbooks、prompts）共用；差异在**唤醒方式、模型声明、内置委派**。模型与跨环境策略 → [models-and-delegation.md](../models-and-delegation.md)。

## 对比

| 维度 | **Grok CLI** | Cursor | Claude Code | Qoder | Antigravity | OpenCode | Codex |
|:-----|:-------------|:-------|:------------|:------|:------------|:---------|:------|
| **模型** | **`grok-4.5` 默认** | 实施 Composer；架构 **Shell grok -p** | **不固定** — 须 prompt 写 slug | **不固定** — `-m` / `/model` | **不固定** — 允许指定 `--model` | **不固定** — 须 prompt 写 slug | 本地配置 |
| **常见 slug** | **`grok-4.5`** | Auto、Grok、Composer | mimo；**claude-opus-4-6**（写作·**须 `--model`**） | `performance`；**`ultimate`=GPT 5.6** | gemini-3.5-flash、gemini-3.1-pro | **`opencode-go/deepseek-v4-flash`**、k3、`v4-pro` | gpt-5.5 / gpt-5.6-* |
| **强项** | **架构/doc/bug 优先轨** | Loop 调度 + 实施 | 大量写代码（mimo）；**Opus 4.6 写作** | TUI Subagent、worktree | 高效改码、中度 Debug | 脚本、adb、前端 k3 | headless |
| **内置周期** | —（由 Cursor `/loop` 调度） | `/loop` | `/loop` 或续聊 | 续聊 | TUI/交互续聊 | `/loop` 或续聊 | `/loop` 或续聊 |
| **本子 agent** | Shell **`grok -p`** | `Task` | `--agents` / 会话 | `/agents` · Subagent | `invoke_subagent` | opencode **会话** | 同会话 / `exec resume` |
| **同栈 CLI** | ~~`grok -p`~~ | ~~`agent -p`~~ | ~~`claude -p`~~ | ~~`qodercli -p`~~ | ~~`agy -p`~~ | ~~`opencode run`~~ | 避免同栈 exec |
| **adb 烟测** | 当前环境子 agent | 同左 | 同左 | 同左 | 同左 | 会话内子 agent | 同左 |

## 选型建议

| 场景 | 推荐运行时 |
|:-----|:-----------|
| **架构 / ADR / 方案 / 挖 bug** | **Shell `grok -p -m grok-4.5`**（**含 Cursor 内**）；不可用 → Task Grok / kimi-k3 |
| Loop 主协调 + 实施改码 | **Cursor**（`Task` · Composer / Auto） |
| 实施量大、成本敏感 | 在 **当前环境**写代码（CC→mimo、Qoder→`performance`/`efficient`、OpenCode→`-m`、Antigravity→`gemini-3.5-flash`）；默认不跨栈 |
| Qoder 本机主会话 | **Qoder**（`qodercli -m …`）；架构用 **`-m ultimate`**（= GPT 5.6，须授权） |
| adb 烟测 | **当前环境子 agent** |
| CI 单命令 tick | **Codex** `exec` 或 **Claude** / **Qoder** / **Antigravity** `-p`（父 agent 不在该栈时） |
| 方案/评审多视角 | **grok -p** 主笔 + Cursor/mimo/Qoder 实现视角 + 只读 review |

## 文档

- [models-and-delegation.md](../models-and-delegation.md) — **必读**：同环境内置 vs 跨环境 CLI  
- [grok.md](grok.md) · [cursor.md](cursor.md) · [claude-code.md](claude-code.md) · [qoder.md](qoder.md) · [antigravity.md](antigravity.md) · [codex.md](codex.md) · [opencode.md](opencode.md)

## 迁移清单

1. 保留 [`loop-prompt.txt`](../loop-prompt.txt)、[`agent-playbooks/`](../agent-playbooks/)  
2. 项目向导：`AGENTS.md`（含 loop 入口）  
3. 项目进度：`dev/progress/`（status、两队列、**health-gates 命令**）  
4. 子 agent：用各栈**内置**委派，跨栈才 CLI  
