---
title: "开发 Loop 外部 CLI"
type: guide
status: accepted
phase: N/A
updated: 2026-07-03
summary: "跨环境 CLI；同栈禁止重复 CLI；烟测默认当前环境子 agent。"
---

# 外部 CLI 委派

Loop 父 agent 在**另一套运行时**起独立进程干活。**不要**用本栈 CLI 重复起同模型（见 [models-and-delegation.md](models-and-delegation.md)）。

## 烟测（adb）默认

| 父 agent 在哪 | 烟测做法 |
|:--------------|:---------|
| **Cursor** | `Task` 子 agent（可 `run_in_background`） |
| **Claude Code** | 当前会话 / `--agents` |
| **OpenCode** | **当前会话内子 agent** — ❌ **`opencode run`** |
| **跨栈** | 仅 prompt **明文**授权，且父 agent **不在** OpenCode |

全局 **仅 1 个** adb 后台烟测。

## Cursor CLI 门禁（`agent -p`）

| 当前 Loop 在哪跑 | `agent -p` |
|:-----------------|:-----------|
| **Cursor IDE 内** | ❌ 用 `Task` |
| **非 Cursor** | ❌ 默认禁止 |
| **非 Cursor** + **「Cursor 可用」** | ✅ |

## OpenCode CLI 门禁（`opencode run`）

| 当前 Loop 在哪跑 | `opencode run` |
|:-----------------|:---------------|
| **OpenCode 会话内** | ❌ **禁止**（用会话子 agent） |
| **OpenCode 会话内 + 须换另一模型** | ✅ `opencode run -m <与当前会话不同的 slug>` |
| **不在 OpenCode**（Cursor/CC/Codex） | 跨栈按需；烟测仍**优先当前环境子 agent** |

## 何时用 / 何时不用

| 情况 | 做法 |
|:-----|:-----|
| 任意环境，adb 烟测 | **当前环境子 agent** |
| 父 agent 在 **OpenCode**，烟测 / 改码 | 会话分工；**不要** `opencode run` |
| 父 agent 在 **OpenCode**，必须用另一模型 | `opencode run -m <另一 provider/model>` |
| 父 agent 在 **Cursor**，写架构 doc | `Task`；**Cursor 可用** 才可 `agent -p` |
| 父 agent 在 **Claude Code**，改码 | 当前会话；**不要** `claude -p` |
| 父 agent 在 **Antigravity**，改码 / 研究 | `invoke_subagent`；**不要** `agy -p` |

## 命令对照（跨环境）

| 生态 | 非交互命令 | 何时用 |
|:-----|:-----------|:-------|
| Cursor | `agent -p --trust` | 非 Cursor + **Cursor 可用** |
| Claude Code | `claude -p` | 父不在 CC，跨栈改码（授权） |
| Antigravity | `agy -p --model <slug>` | 父不在 Antigravity，跨栈改码（授权） |
| Codex | `codex exec` | 父不在 Codex |
| OpenCode | `opencode run -m …` | 父**不在** OpenCode；或 OpenCode 内**换模型** |

## 详细参数

→ **[external-agent-cli.md](../../docs/guides/external-agent-cli.md)**

## 并行约束

同一 adb 设备尽量只跑一个测试类 agent。
