---
title: "Loop 运行时 — Claude Code"
type: guide
status: accepted
phase: N/A
updated: 2026-07-03
summary: "在 Claude Code 中运行开发 Loop；模型不固定，须在 prompt 声明 slug。"
---

# Claude Code 运行时

## 模型（不固定）

Claude Code **不绑定单一模型** — 用户可在 CLI / 设置中切换 **mimo-v2.5-pro**、opus 等。

| 要求 | 说明 |
|:-----|:-----|
| **Loop prompt** | 写 `当前模型：<slug>（Claude Code）` |
| **未写时** | 首轮读会话 `/status` 或配置 → **声明假设**，每轮输出复述 |
| **能力档** | 按 [models.md](../models.md) 查**实际 slug**，勿写「CC 默认 mimo」 |

**常见 slug 实践**：mimo-v2.5-pro（实施首选）、opus（须 loop 费用授权）。要 **kimi-k3** 时跨栈用 [../cli/kimi.md](../cli/kimi.md)，勿与旧 `kimi-k2.6` 混用。

Claude Code 用 **`/loop`**（若环境提供）或 **交互续聊** 复用同一套 [workflow.md](../workflow.md)。间隔与唤醒由 `/loop` 自带，本仓库只维护 [`loop-prompt.txt`](../loop-prompt.txt)。

## 交互会话（常见）

1. 在仓库根启动 `claude`（自动读 `CLAUDE.md` / `AGENTS.md`）  
2. 首条消息：`@dev/loop/loop-prompt.txt` + **当前模型** + **方向**（见 [human-input.md](../human-input.md)）  
3. 每轮结束后发送：「继续下一轮：先读 `dev/progress/status.md`，按 `dev/loop/workflow.md` 执行。」  
4. 用 `--continue` / `--resume` 恢复同目录最近会话  

适合：人在旁、需要频繁看终端输出。

## `/loop`（若环境提供）

```text
/loop 10m @dev/loop/loop-prompt.txt
当前模型：mimo-v2.5-pro（Claude Code）
方向：按 status 推进。
```

间隔与停止方式以 Claude Code 内 `/loop` 提示为准。

## 非交互 `claude -p`（跨栈）

跨栈或单次 headless → **[../cli/claude.md](../cli/claude.md)**。同栈禁止再起 `claude -p` → [../external-cli.md](../external-cli.md)。

## 子 agent / 分工

| 方式 | 说明 |
|:-----|:-----|
| **`--agents` JSON** | 启动时注册 reviewer、coder 等；父会话按名调用 |
| **会话内显式分工** | 一条消息里写「你只做 Direction Discovery，按 playbook X」 |
| **外部进程** | 另开终端 `claude -p` 跑单个 playbook slice |
| **Hooks** | `PreToolUse` 等约束写路径/命令（见 Claude Code hooks 文档） |

无 Cursor `Task` 的并行 UI；并行需多终端或脚本同时起多个 `claude -p`（注意文件冲突，遵守 orchestration 矩阵）。

## 规则放哪

| 位置 | 说明 |
|:-----|:-----|
| `AGENTS.md` / `CLAUDE.md` | 新会话必读；含 [dev/loop/INDEX.md](../INDEX.md) 入口 |
| `dev/loop/` | Loop **SSOT**（workflow、playbook、loop-prompt） |
| `.claude/` | 项目 settings、hooks、agents 配置（若使用） |

## 与 Cursor / CLI

| 场景 | 做法 |
|:-----|:-----|
| 父 agent 已在 Claude Code | 当前会话 / `--agents`（**不要**再起 `claude -p`）；prompt 写明 slug |
| 需要大量改代码 | **mimo-v2.5-pro**；前端优先跨栈 **kimi-k3** → [../cli/kimi.md](../cli/kimi.md) / [../cli/opencode.md](../cli/opencode.md) |
| 需要 Grok / kimi-k3 写架构 / 挖 bug | Cursor **Grok**，或跨栈 k3（见上） |
| 需要 adb 烟测 | **当前会话**子 agent（**不要** `opencode run`） |

见 [models-and-delegation.md](../models-and-delegation.md)。
