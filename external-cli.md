---
title: "开发 Loop 外部 CLI"
type: guide
status: accepted
phase: N/A
updated: 2026-08-14
summary: "跨环境 CLI 门禁；架构优先 grok -p；同栈禁止重复 CLI；命令参数见 cli/。"
---

# 外部 CLI 委派

Loop 父 agent 在**另一套运行时**起独立进程干活。**不要**用本栈 CLI 重复起同模型。

**命令怎么写** → **[cli/INDEX.md](cli/INDEX.md)**（**Grok** / Cursor / Claude / **Qoder** / Antigravity / Codex / OpenCode / **Kimi `--yolo`**）。
**架构轨优先** → **`grok -p`**（****；CLI 可用时，**即使父 agent 在 Cursor 内**；默认不传 `-m`）。
**选谁干活** → [models-and-delegation.md](models-and-delegation.md)。

## 烟测（adb）默认

| 父 agent 在哪 | 烟测做法 |
|:--------------|:---------|
| **Cursor** | `Task` 子 agent（可 `run_in_background`） |
| **Claude Code** | 当前会话 / `--agents` |
| **Qoder** | 当前会话 / Subagent（`/agents`）— ❌ **`qodercli -p`** |
| **OpenCode** | **当前会话内子 agent** — ❌ **`opencode run`** |
| **Kimi** | 当前会话继续 — ❌ 再起同目录 `kimi -p` |
| **Grok CLI** | 当前 `grok` 交互会话 — ❌ 再起同目录 `grok -p` |
| **跨栈** | 仅 prompt **明文**授权，且父 agent **不在**目标栈 |

全局 **仅 1 个** adb 后台烟测。

## 同栈禁止 / 跨栈放行

| 当前环境 | ✅ 本子 agent | ❌ 同栈 CLI |
|:---------|:-------------|:-----------|
| **Cursor** | IDE `Task` | `agent -p` |
| **Claude Code** | 会话 / `--agents` | `claude -p` |
| **Qoder** | 会话 / Subagent（`/agents`） | `qodercli -p`（换另一 `-m` 除外） |
| **Antigravity** | `invoke_subagent` | `agy -p` |
| **OpenCode** | 会话内子 agent | `opencode run`（换另一 `-m` 除外） |
| **Codex** | 会话 / `exec resume` | 无必要并行同栈 exec |
| **Kimi** | 当前 `kimi` 会话 | 同目录再起 `kimi -p` |
| **Grok CLI** | 当前 `grok` 交互会话 | 同目录再起 `grok -p`（换另一 `-m` 除外） |

### Cursor 内架构轨（grok CLI 优先 · 非 Task）

父 agent **在 Cursor IDE 内**时：

| 轨 | 委派方式 |
|:---|:---------|
| **架构 / ADR / 方案 / 挖 bug / Arch-First** | ✅ 父 agent **Shell** → `grok --no-plan --permission-mode bypassPermissions --always-approve -p`（默认不传 `-m`） |
| **实施写代码** | ✅ Cursor **`Task`**（Composer / Auto） |
| ~~架构用 Task Grok~~ | ❌ **禁止**（CLI 可用时） |
| ~~`agent -p`~~ | ❌ 同栈禁止（用 `Task` 或 Shell `grok`） |

`grok -p` 在 Cursor 内是 **Shell 调外部 CLI**，**不算**「同栈再起 Cursor 子 agent」；也**不要**为架构把 Cursor 聊天模型切成 Grok。

## Cursor CLI 门禁（`agent -p`）

| 当前 Loop 在哪跑 | `agent -p` |
|:-----------------|:-----------|
| **Cursor IDE 内** | ❌ 用 `Task` |
| **非 Cursor** | ❌ 默认禁止 |
| **非 Cursor** + **「Cursor 可用」** | ✅ |

**不算授权**：只写「用 Composer」但未写 **Cursor 可用**；agent 自行判断「应该开 Cursor」。

## OpenCode CLI 门禁（`opencode run`）

| 当前 Loop 在哪跑 | `opencode run` |
|:-----------------|:---------------|
| **OpenCode 会话内** | ❌ **禁止**（用会话子 agent） |
| **OpenCode 会话内 + 须换另一模型** | ✅ `opencode run -m <与当前会话不同的 slug>` |
| **不在 OpenCode** | 跨栈按需；烟测仍**优先当前环境子 agent** |

## Qoder CLI 门禁（`qodercli -p`）

| 当前 Loop 在哪跑 | `qodercli -p` |
|:-----------------|:--------------|
| **Qoder 会话内** | ❌ **禁止**（用会话 Subagent） |
| **Qoder 会话内 + 须换另一模型** | ✅ `qodercli -p -m <与当前不同的 slug>` |
| **不在 Qoder** | 跨栈按需；烟测仍**优先当前环境子 agent** |

命令 → [cli/qoder.md](cli/qoder.md)。

## Grok CLI 门禁（`grok -p`）

| 当前 Loop 在哪跑 | `grok -p` |
|:-----------------|:----------|
| **Grok 交互会话内** | ❌ **禁止**（续聊 / `--continue`） |
| **Grok 会话内 + 须换另一模型** | ✅ `grok -p -m <另一 slug>` |
| **Cursor 内 · 架构/doc/bug** | ✅ **Shell `grok -p`** + **`--no-plan --permission-mode bypassPermissions --always-approve`**（**禁止 Task Grok**） |
| **其它栈 · 架构/doc/bug** | ✅ **优先** `grok -p`（跟 CLI default） |
| **Cursor / 其它 · 实施写代码** | ❌ 用 `Task` / 当前环境实施模型，**不用** grok CLI |

命令 → [cli/grok.md](cli/grok.md) · L2 → [runtimes/grok.md](runtimes/grok.md)。

## 何时用 / 何时不用

| 情况 | 做法 |
|:-----|:-----|
| 任意环境，adb 烟测 | **当前环境子 agent** |
| 父 agent 在某栈内，同栈能力 | 上表「本子 agent」；**不要**同栈 CLI |
| 父 agent 在 **OpenCode**，必须用另一模型 | `opencode run -m <另一 provider/model>` |
| 父 agent 在 **Qoder**，必须用另一模型 | `qodercli -p -m <另一 slug>` |
| 父 agent 在 **Cursor**，写架构 doc | **Shell `grok -p`**；`grok` 不可用时才 `Task`（Grok）或 `agent -p`（须 **Cursor 可用**） |
| 父 agent 在 **Cursor**，实施改码 | `Task`（Composer / Auto）；**不要** `grok -p` |
| 跨栈 kimi-k3 / 前端 | `kimi --yolo` 或 `opencode run -m kimi-for-coding/k3` → [cli/kimi.md](cli/kimi.md) · [cli/opencode.md](cli/opencode.md) |

## 并行约束

同一 adb 设备尽量只跑一个测试类 agent。
