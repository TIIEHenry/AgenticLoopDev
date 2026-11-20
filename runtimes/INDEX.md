---
title: "Loop 运行时选型"
type: guide
status: accepted
phase: N/A
updated: 2026-11-20
summary: "运行时对比。未授权降级 Grok 4.7。Cursor 实施 Composer 2.5；AGY 按套餐选 3.8 Flash 或 Gemini 4 Hydrogen；Codex 日常 gpt-6.2-sol；Kimi 架构审 K3.1 Pro。Qoder 只登记档位。"
---

# Loop 运行时选型

**语义层**（workflow、playbooks、prompts）共用；差异在**唤醒方式、模型声明、内置委派**。模型与跨环境策略 → [models-and-delegation.md](../models-and-delegation.md)。

## 对比

| 维度 | **Grok CLI** | Cursor | Claude Code | Qoder | Antigravity | OpenCode | Codex |
|:-----|:-------------|:-------|:------------|:------|:------------|:---------|:------|
| **模型** | **`grok-4.7` 默认** | 实施 Composer 2.5；架构未授权才 **Task 最新 Grok** | **不固定** — 须 prompt 写 slug | **不固定** — `-m` / `/model` | **必须指定 `--model`** | **不固定** — 须 prompt 写 slug | 本地配置，日常 `gpt-6.2-sol` |
| **常见 slug** | **`grok-4.7`**（另有 4.6 / 4.5） | Composer 2.5、Auto Cost、Grok 4.7 | **无** — 以会话实际 slug 为准 | 非顶档以 list 为准；顶档不写具体型号 | 3.8 Flash；Pro+ 用 Hydrogen / Orchestrator | **`opencode-go/deepseek-v4.1-flash`** | `gpt-6.2-sol`、`gpt-6.1-terra`、`gpt-6-luna` |
| **强项** | **无付费授权时的架构降级（不做执行）** | Loop 调度 + 实施 | 交互会话、`--agents`（模型不固定） | 顶档须明文，不映射到其他 CLI 的某一代；TUI Subagent、worktree | Free/Plus 便宜实施；Pro+ 用 Gemini 4 执行档 | 通用后端实施 | 父会话写代码；Astra 须点名且不写代码 |
| **内置周期** | —（由 Cursor `/loop` 调度） | `/loop` | `/loop` 或续聊 | 续聊 | TUI/交互续聊 | `/loop` 或续聊 | `/loop` 或续聊 |
| **本子 agent** | Shell **`grok -p`** | `Task` | `--agents` / 会话 | `/agents` · Subagent | `invoke_subagent` | opencode **会话** | 同会话 / `exec resume` |
| **同栈 CLI** | ~~`grok -p`~~ | ~~`agent -p`~~ | ~~`claude -p`~~ | ~~`qodercli -p`~~ | ~~`agy -p`~~ | ~~`opencode run`~~ | 避免同栈 exec |
| **adb 烟测** | 当前环境子 agent | 同左 | 同左 | 同左 | 同左 | 会话内子 agent | 同左 |

## 选型建议

| 场景 | 推荐运行时 |
|:-----|:-----------|
| **架构 / ADR / 方案 / 挖 bug** | **Grok 子 agent 优先**（Cursor：`Task` + 版本最新的 Grok slug）；无档 → **Shell `grok -p`** / 已授权的 K3.1 Pro |
| Loop 主协调 + 实施改码 | **Cursor**（`Task` · Composer 2.5 / Auto Cost） |
| 实施量大、成本敏感 | 在 **当前环境**写代码（Claude Code 用会话实际模型、Qoder 用 list 里的非顶档、OpenCode→`opencode-go/deepseek-v4.1-flash`、AGY Free/Plus→`gemini-3.8-flash`、AGY Pro+→Hydrogen 或 Orchestrator）；默认不跨栈 |
| Qoder 本机主会话 | **Qoder**（`qodercli -m …`）；顶档须授权，不写代码，不写成某一代 |
| adb 烟测 | **当前环境子 agent** |
| CI 单命令 tick | **Codex** `exec` 或 **Claude** / **Qoder** / **Antigravity** `-p`（父 agent 不在该栈时） |
| 方案/评审多视角 | **Grok** 主笔（Task 优先）+ Cursor/mimo/Qoder 实现视角 + 只读 review |

## 文档

- [models-and-delegation.md](../models-and-delegation.md) — **必读**：同环境内置 vs 跨环境 CLI
- [grok.md](grok.md) · [cursor.md](cursor.md) · [claude-code.md](claude-code.md) · [qoder.md](qoder.md) · [antigravity.md](antigravity.md) · [codex.md](codex.md) · [opencode.md](opencode.md)

## 迁移清单

1. 保留 [`loop-prompt.txt`](../loop-prompt.txt)、[`agent-playbooks/`](../agent-playbooks/)
2. 项目向导：`AGENTS.md`（含 loop 入口）
3. 项目进度与命令：根开发入口按 [porting.md](../porting.md#项目侧绑定) 绑定实际来源；未采用的旧来源不读、不建，无绑定旧项目沿用默认布局
4. 子 agent：用各栈**内置**委派，跨栈才 CLI
