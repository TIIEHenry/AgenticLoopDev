---
title: "Loop 运行时 — Qoder"
type: guide
status: accepted
phase: N/A
updated: 2026-11-20
summary: "Qoder IDE / qodercli：只登记档位。顶档须人类点名且不写代码，不映射到其他 CLI 的某一代。"
---

# Qoder 运行时

本机常见入口：

| 入口 | 二进制 | 用途 |
|:-----|:-------|:-----|
| **Qoder IDE** | `qoder` | 图形 IDE（VS Code 系） |
| **Qoder CLI** | `qodercli` | TUI / 非交互 `-p`（Loop 主路径） |

本仓库只维护 [`loop-prompt.txt`](../loop-prompt.txt)；周期用交互续聊，或环境若提供 `/loop` 则用之。

## 模型（不固定）

Qoder **不绑定单一模型** — 档位池、Frontier、Custom 均可切换。能力档按**实际档位**查 [models.md](../models.md)。

| 类别 | Loop |
|:-----|:-----|
| **非顶档** | 日常实施。档位名以 `qodercli --list-models` 和 TUI `/model` 为准。仓库不登记具体型号，也不再把已退下的旧档名当作现行档 |
| **顶档** | **仅**方案 / 架构 / 挖 bug。**禁止**写 prod 代码。**必须人类显式指定**。不映射到其他 CLI 的某一代 |

| 要求 | 说明 |
|:-----|:-----|
| **Loop prompt** | 写 `当前模型：<档位>（Qoder）`。写档位，不写具体型号 |
| **未写时** | 声明假设，每轮复述。假设只能落在非顶档 |
| **顶档** | 仅当本 tick 写出 `-m ultimate` 或 `当前模型` 点了顶档。list 里看得到、IDE 停在顶档、或「架构任务更合适」都不算 |

无显式指定时不得升到顶档。官方型号以 [Qoder CLI model](https://docs.qoder.com/cli/model) 和本机 list 为准，对照结果不抄进本文。

## 交互会话（常见）

1. 仓库根：`qodercli -m <slug>`（或 IDE Chat）  
2. 首条：`@dev/loop/loop-prompt.txt` + **当前模型** + **方向**（[human-input.md](../human-input.md)）  
3. 每轮：「继续下一轮：先读 `dev/progress/status.md`，按 `dev/loop/workflow.md`。」  
4. `-c` / `-r` 续会话  

启动示例（实施）：

```text
qodercli -m auto
# 首条消息：
@dev/loop/loop-prompt.txt
当前模型：auto（Qoder）。方向：按 status 推进实施。
```

`auto` 是档位示例。本机 list 的非顶档若不是这个名字，改用 list 里的名字。

顶档架构轨（**必须人类显式指定**；**禁止写代码**；不写外部代际）：

```text
qodercli -m ultimate
@dev/loop/loop-prompt.txt
当前模型：顶档（Qoder · 主架构）。方向：首次方案/ADR 主笔；禁止写代码。
```

未点名顶档 → **不得**使用，即使 list 里只有它。

## 同栈：已在 Qoder 会话（Loop 父 agent）

| 任务 | 做法 |
|:-----|:-----|
| **写代码、烟测、挖 bug、分工** | **当前会话 Subagent**（`/agents`、内置 Explore / general-purpose、项目 `.qoder/agents/`）；写代码用 **非顶档** |
| **`qodercli -p`** | ❌ **禁止**（同栈重复 CLI） |

**唯一例外 — 换用另一模型**：当前会话模型 A，本轨必须用 B 时，可另起 `qodercli -p -m <另一 slug>`（须与当前不同；adb 全局仅 1 个后台）。

## 跨栈 / 非交互

门禁 → [../external-cli.md](../external-cli.md)。命令 → [../cli/qoder.md](../cli/qoder.md)。

## 子 agent

| 方式 | 说明 |
|:-----|:-----|
| **TUI `/agents`** | 查看 / 创建 / 管理 Subagent |
| **`--agent` / `--agents`** | 启动时指定或注册自定义 agents |
| **内置** | `general-purpose`、`Explore`、`Plan` 等（随版本变化） |
| **会话内显式分工** | 「你只做 Direction Discovery，按 playbook X」 |
| **worktree 隔离** | `--worktree` 或 Subagent `isolation: worktree`（见 Qoder 文档） |

无 Cursor `Task` UI；并行靠多 Subagent / 多终端（遵守 orchestration 矩阵）。

## 规则放哪

| 位置 | 说明 |
|:-----|:-----|
| `AGENTS.md` | 新会话必读；含 [dev/loop/INDEX.md](../INDEX.md) 入口（Qoder `/init` 亦可生成） |
| `dev/loop/` | Loop **SSOT** |
| `.qoder/` | 项目 agents、settings、skills（若使用；**非** loop 套件） |

## 与其他运行时

| 场景 | 做法 |
|:-----|:-----|
| 父已在 Qoder | 会话 Subagent；**不要**再起同栈 `-p` |
| 大量改代码 | 本机 list 里的非顶档。不写具体型号 |
| 要顶档写架构 | **仅**人类已显式指定时用顶档（禁写代码，不写成某一代）；否则降级或 `HUMAN_DECISION_REQUIRED` |
| adb 烟测 | **当前会话** Subagent |

见 [models-and-delegation.md](../models-and-delegation.md)。
