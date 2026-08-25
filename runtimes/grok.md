---
title: "Loop 运行时 — Grok CLI"
type: guide
status: accepted
phase: N/A
updated: 2026-08-25
summary: "Grok Build CLI：子 agent 无 Grok 档时的架构/ADR/挖 bug 降级通道；直接 grok -p（勿 login）；跟 CLI default。"
---

# Grok CLI 运行时

**定位**：Loop **中强架构轨的 L3 通道**：仅当当前运行时**子 agent 模型列表不含 Grok**时，用本 CLI 做方案/ADR 主笔、Arch-First 审查、挖 bug、只读审计。父在 Cursor 且 Task 已有 `cursor-grok-*` 时，**不要**默认走本 CLI。实施写代码仍留在 **Cursor / Claude / Qoder** 等当前环境。

> **命令参数** → [../cli/grok.md](../cli/grok.md) 
> **能力档 / 费用** → [../models.md](../models.md) 
> **跨栈门禁** → [../external-cli.md](../external-cli.md)

## 默认模型

```bash
grok models
# Default model: <本机为准；常见 grok-4.6>
```

Loop prompt 可写：

```text
当前模型：Grok CLI（跟 grok models 的 Default）
方向：按 workflow 推进一轮。
```

**Shell 不传 `-m`**，除非人类本 tick 点名。**不要** `grok login`。

## 与 Cursor 的分轨（Task Grok 优先）

| 任务 | 优先 |
|:-----|:-----|
| 架构 / ADR / 方案首次起草 | Cursor **`Task` Grok**（列表有档）；否则 **`grok -p`** |
| Arch-First 审查 | 独立 **Task Grok** 实例（≠ 主笔）；无档才 **`grok -p`** |
| 挖 bug / 根因 | 同上；或当前环境子 agent |
| 大量改代码 | **Cursor `Task`**（Composer / Auto）— **不用** grok CLI |
| Loop 父 agent 调度 | **Cursor**（`/loop`、`Task`、并行 wave） |

**规则**：父 agent 在 **Cursor IDE 内**且 Task 模型列表含 Grok 时，架构/doc 轨用 **`Task` 传该 slug**（**不是** Shell `grok -p`，也**不要**切聊天模型到 Grok）。仅当列表无 Grok 档时才 `grok -p`。

## 周期调度

```bash
GROK_LOOP_AUTH='--no-plan --permission-mode bypassPermissions --always-approve'
grok $GROK_LOOP_AUTH -p "$prompt"
```

见 [../cli/grok.md](../cli/grok.md)。

## 子 agent / 委派

| 方式 | 说明 |
|:-----|:-----|
| **Shell `grok -p`** | 当前运行时**无** Grok 子 agent 档时，Loop 父 agent 委派 |
| **交互 `grok`** | 人类结对；Loop tick 内少用 |
| **`grok agent`** | headless agent 子命令（SDK/relay）；Loop 默认不用 |

**同栈禁止**：已在 Grok 交互会话时，**不要**再起 `grok -p`（续聊或 `--continue`）。

## 外部 CLI

命令全文 → [../cli/grok.md](../cli/grok.md)。

## 限制

- 须本机已安装 `grok`；**直接 `-p`**，**禁止** Loop 内 `grok login` 
- 模型跟 `grok models` 的 Default；勿硬编无关 `-m` 
- **禁止**用 grok CLI 写 prod 实施轨（除非人类本 tick 明确授权 grok 改码）
