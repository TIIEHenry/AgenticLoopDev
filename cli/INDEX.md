---
title: "Loop 外部 CLI 命令指南"
type: index
status: accepted
phase: N/A
updated: 2026-07-29
summary: "L3 跨栈 CLI 命令速查：Cursor / Claude / Qoder / Antigravity / Codex / OpenCode / Kimi；门禁见 external-cli.md。"
---

# 外部 CLI 命令指南

> **本目录**：各栈 **怎么敲命令**（参数、示例）。  
> **何时能用 / 同栈禁止** → [../external-cli.md](../external-cli.md)、[../models-and-delegation.md](../models-and-delegation.md)。  
> **IDE 内 loop**（`Task` / 会话子 agent）不是本目录范围。

## 命令对照

| 生态 | 非交互 / 脚本 | 交互（少审批） | 详见 |
|:-----|:--------------|:---------------|:-----|
| Cursor | `agent -p --trust` | —（用 IDE） | [cursor.md](cursor.md) |
| Claude Code | `claude -p --dangerously-skip-permissions` | `claude` | [claude.md](claude.md) |
| **Qoder** | `qodercli -p --dangerously-skip-permissions -m …` | `qodercli -m …` | [qoder.md](qoder.md) |
| Antigravity | `agy -p --dangerously-skip-permissions` | `agy` | [antigravity.md](antigravity.md) |
| Codex | `codex exec` | `codex` | [codex.md](codex.md) |
| OpenCode | `opencode run -m …` | `opencode -m …` | [opencode.md](opencode.md) |
| **Kimi Code** | `kimi -p "…"`（`-p` 自带 auto；默认 **k3**） | **`kimi --yolo`**（推荐） | [kimi.md](kimi.md) |

## 何时用哪一个（速查）

| 场景 | 推荐 CLI |
|:-----|:---------|
| 更新 `dev/plans/`、架构 doc（须 **Cursor 可用**） | `agent -p --trust` |
| 高性价比改码 / 研究 | `agy -p`、`qodercli -p -m performance`、`kimi --yolo` / `kimi -p`、`claude -p` |
| **前端**实施 | **`kimi --yolo`** 或 **`opencode -m kimi-for-coding/k3`**（Qoder 账号有 k3 也可用本栈） |
| 架构主笔（本仓库 Codex 授权轨） | `codex exec`；Qoder 用 **`qodercli … -m ultimate`**（= GPT 5.6，须 prompt 授权） |
| adb / 烟测（父**不在**目标栈） | 当前环境子 agent；跨栈按需 |
| 父已在某栈内 | **不要**再起同栈 CLI → [../external-cli.md](../external-cli.md) |

## Prompt 骨架（通用）

```bash
ROOT="$(git rev-parse --show-toplevel)"
prompt="$(cat <<EOF
仓库：$ROOT
先读：dev/progress/status.md、AGENTS.md、本轮 plan / roadmap
任务：<具体任务>
交付：<改哪些文件 / 跑哪些命令 / pass-fail>
约束：不 commit；无关模块不改；文档用中文。
EOF
)"
```

再按目标栈调用（见各页）。

## 相关

| 文档 | 说明 |
|:-----|:-----|
| [../external-cli.md](../external-cli.md) | L3 **门禁**（同栈禁止、Cursor 可用、烟测） |
| [../runtimes/INDEX.md](../runtimes/INDEX.md) | L2 运行时选型（IDE 内） |
| [../models.md](../models.md) | 模型能力对比 |
