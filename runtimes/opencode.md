---
title: "Loop 运行时 — OpenCode"
type: guide
status: accepted
phase: N/A
updated: 2026-07-28
summary: "OpenCode Loop：会话内子 agent；禁止同栈 opencode run；换模型才可 CLI。"
---

# OpenCode 运行时

周期推进用 **`/loop`**（若环境提供）或 **交互续聊**；间隔由 OpenCode 内 `/loop` 自带。本仓库只维护 [`loop-prompt.txt`](../loop-prompt.txt)。

## 同栈：已在 OpenCode 会话（Loop 父 agent）

| 任务 | 做法 |
|:-----|:-----|
| **写代码、烟测、挖 bug** | **当前会话内子 agent** 分工 |
| **`opencode run`** | ❌ **禁止**（同栈重复起 CLI，抢 adb / 会话） |

**唯一例外 — 换用另一模型**：当前会话绑定模型 A，本轨**必须**用模型 B 时，可 `opencode run -m <另一 slug>`（须与当前不同；adb 仍全局仅 1 个后台）。

启动父会话：`opencode -m <provider/model>`。slug 对照 → [../cli/opencode.md](../cli/opencode.md)。

### 何时写进 prompt、何时只写 CLI

| 场景 | 模型怎么定 | prompt 写 `当前模型：`？ |
|:-----|:-----------|:-------------------------|
| **OpenCode 父会话** | 启动 `opencode -m …` 或 TUI 内切换 | 可选；每轮复述实际 slug |
| **OpenCode 父会话 + 换模型轨** | `opencode run -m <另一 slug>` | 否 |
| **跨栈**（父不在 OpenCode） | 调用方 `-m` | 否 |

## 跨栈 / 烟测

门禁与烟测默认 → [../external-cli.md](../external-cli.md)。跨栈命令 → [../cli/opencode.md](../cli/opencode.md)。

辅助脚本 `scripts/opencode-adb-singularity.sh`（若环境提供）供**跨栈**调用；OpenCode 父会话内应直接跑 adb，勿再起第二条 `opencode run`。

## 与 UA TUI

| | OpenCode 会话 / `opencode run`（跨栈） | `opencode` TUI + `--ua-grpc` |
|--|----------------------------------------|------------------------------|
| 引擎 | OpenCode + 配置的 slug | UniverseAgent 后端 |
| 用途 | Loop 开发 / 烟测 | 测 UA 引擎本身 |

详见 [../models-and-delegation.md](../models-and-delegation.md)。
