---
title: "Loop 运行时 — Qoder"
type: guide
status: accepted
phase: N/A
updated: 2026-07-29
summary: "Qoder IDE / qodercli：Ultimate=GPT 5.6（须人类显式指定、禁写代码）；同栈用 Subagent。"
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

| 类别 | 典型 `-m` | Loop 用途 |
|:-----|:----------|:----------|
| **档位池** | `auto`、`performance`、`efficient`、`lite` | 日常实施；按费用选档 |
| **Ultimate = GPT 5.6** | **`ultimate`**（`--list-models` 显示 `Ultimate`） | **仅**方案/架构/挖 bug；**禁止**写 prod 代码；**必须人类显式指定**才可用 |
| **Frontier** | `kimi-k3`、`deepseek-v4-pro`、Qwen / GLM 等（以 list 为准） | 实施 / 前端（k3）/ 研究 |

| 要求 | 说明 |
|:-----|:-----|
| **Loop prompt** | 写 `当前模型：…（Qoder）`；有启动 `-m` 时可省略，但仍建议每轮复述 |
| **未写时** | `/status` 或假设 → **声明假设**，每轮输出复述 |
| **Ultimate / GPT 5.6（显式指定）** | **仅当**人类在本 tick/本轨**显式**写出下列之一才可用：CLI `-m ultimate`、或 prompt `当前模型：Ultimate` / `GPT 5.6` / `model=ultimate`。**禁止**因 `--list-models` 只有 Ultimate、IDE 停在 Ultimate、或「架构任务更合适」而自行选用 |

> **映射约定（本仓库）**：Qoder 档位 **Ultimate** 即能力表中的 **GPT 5.6**。CLI 传 `-m ultimate`；人类可写「Ultimate」或「GPT 5.6」，agent 按同一高费用门禁处理。  
> **无显式指定时**：Qoder 实施默认按 **`performance`**（或人类写明的非 Ultimate 档）计；不得升到 Ultimate。

官方其它模型随服务端更新；非 Ultimate 仍以 `qodercli --list-models` 与 TUI `/model` 为准。见 [docs.qoder.com/en/cli/model](https://docs.qoder.com/en/cli/model)。

## 交互会话（常见）

1. 仓库根：`qodercli -m <slug>`（或 IDE Chat）  
2. 首条：`@dev/loop/loop-prompt.txt` + **当前模型** + **方向**（[human-input.md](../human-input.md)）  
3. 每轮：「继续下一轮：先读 `dev/progress/status.md`，按 `dev/loop/workflow.md`。」  
4. `-c` / `-r` 续会话  

启动示例（实施）：

```text
qodercli -m performance
# 首条消息：
@dev/loop/loop-prompt.txt
当前模型：performance（Qoder）。方向：按 status 推进实施。
```

Ultimate / GPT 5.6 架构轨（**必须人类显式指定**；**禁止写代码**）：

```text
qodercli -m ultimate
@dev/loop/loop-prompt.txt
当前模型：Ultimate / GPT 5.6（Qoder · 主架构）。方向：首次方案/ADR 主笔；禁止写代码。
```

未写 `ultimate` / GPT 5.6 / Ultimate → **不得**使用该档，即使 list 仅有 Ultimate。

## 同栈：已在 Qoder 会话（Loop 父 agent）

| 任务 | 做法 |
|:-----|:-----|
| **写代码、烟测、挖 bug、分工** | **当前会话 Subagent**（`/agents`、内置 Explore / general-purpose、项目 `.qoder/agents/`）；写代码用 **非 Ultimate** 档（如 `performance`） |
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
| 大量改代码 | `performance` / `efficient` / Frontier；**勿**用 `ultimate` |
| 要 GPT 5.6 写架构 | **仅**人类已显式指定时本栈 **`-m ultimate`**（禁写代码）；否则降级或 `HUMAN_DECISION_REQUIRED` |
| adb 烟测 | **当前会话** Subagent |

见 [models-and-delegation.md](../models-and-delegation.md)。
