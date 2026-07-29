---
title: "Loop 运行时选型"
type: guide
status: accepted
phase: N/A
updated: 2026-07-29
summary: "Cursor / Claude Code / Qoder / Codex / OpenCode 运行时对比；模型不固定栈须声明 slug。"
---

# Loop 运行时选型

**语义层**（workflow、playbooks、prompts）共用；差异在**唤醒方式、模型声明、内置委派**。模型与跨环境策略 → [models-and-delegation.md](../models-and-delegation.md)。

## 对比

| 维度 | Cursor | Claude Code | Qoder | Antigravity | OpenCode | Codex |
|:-----|:-------|:------------|:------|:------------|:---------|:------|
| **模型** | 架构/挖 bug 默认 Grok；实施常 Composer | **不固定** — 须 prompt 写 slug | **不固定** — `-m` / `/model` | **不固定** — 允许指定 `--model` | **不固定** — 须 prompt 写 slug | 本地配置 |
| **常见 slug** | **Auto**、Grok、Composer（Cursor 无 GPT 可派） | mimo、opus | `performance`；**`ultimate`=GPT 5.6**（**须显式指定**） | gemini-3.5-flash、gemini-3.1-pro | deepseek；**`kimi-for-coding/k3`**（`k2p6`=旧档） | gpt-5.5 / gpt-5.6-* |
| **强项** | 架构/doc/bug 默认 Grok；改码 Composer 或更省的 Auto | 大量写代码（mimo） | TUI Subagent、worktree、多模型池 | 高效代码开发、中度 Debug 与研究 | 脚本、adb、**前端 k3** | headless |
| **内置周期** | `/loop` | `/loop` 或续聊 | 续聊（或环境 `/loop`） | TUI/交互续聊 | `/loop` 或续聊 | `/loop` 或续聊 |
| **本子 agent** | `Task` | `--agents` / 会话分工 | `/agents` · `--agents` · Subagent | `invoke_subagent` | opencode **会话** | 同会话 / `exec resume` |
| **同栈 CLI** | ~~`agent -p`~~ | ~~`claude -p`~~ | ~~`qodercli -p`~~（换另一 `-m` 除外） | ~~`agy -p`~~ | ~~`opencode run`~~（换另一 `-m` 除外） | 避免同栈 exec |
| **adb 烟测** | 当前环境子 agent | 同左 | 同左 | 同左 | 会话内子 agent | 同左 |

## 选型建议

| 场景 | 推荐运行时 |
|:-----|:-----------|
| Loop 主协调 + 架构/doc + bug | **Cursor**（`当前模型：Grok`；实施改码可 Composer） |
| 实施量大、成本敏感 | 在 **当前环境**写代码（CC→mimo、Qoder→`performance`/`efficient`、OpenCode→`-m`、Antigravity→`gemini-3.5-flash`）；默认不跨栈 |
| Qoder 本机主会话 | **Qoder**（`qodercli -m …`）；架构用 **`-m ultimate`**（= GPT 5.6，须授权） |
| adb 烟测 | **当前环境子 agent** |
| CI 单命令 tick | **Codex** `exec` 或 **Claude** / **Qoder** / **Antigravity** `-p`（父 agent 不在该栈时） |
| 方案/评审多视角 | 组合：Cursor 主笔 + mimo / Qoder / gemini 实现视角 + 只读 review |

## 文档

- [models-and-delegation.md](../models-and-delegation.md) — **必读**：同环境内置 vs 跨环境 CLI  
- [cursor.md](cursor.md) · [claude-code.md](claude-code.md) · [qoder.md](qoder.md) · [antigravity.md](antigravity.md) · [codex.md](codex.md) · [opencode.md](opencode.md)

## 迁移清单

1. 保留 [`loop-prompt.txt`](../loop-prompt.txt)、[`agent-playbooks/`](../agent-playbooks/)  
2. 项目向导：`AGENTS.md`（含 loop 入口）  
3. 项目进度：`dev/progress/`（status、两队列、**health-gates 命令**）  
4. 子 agent：用各栈**内置**委派，跨栈才 CLI  
