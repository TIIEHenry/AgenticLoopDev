---
title: "Loop 运行时 — Grok CLI"
type: guide
status: accepted
phase: N/A
updated: 2026-08-08
summary: "Grok Build CLI：架构/ADR/挖 bug 优先轨；默认 grok-4.5；非交互 grok -p；与 Cursor 协调时分轨。"
---

# Grok CLI 运行时

**定位**：Loop **中强架构轨的首选运行时**（`grok-4.5`），用于方案/ADR 主笔、Arch-First 审查、挖 bug、只读审计。实施写代码仍留在 **Cursor / Claude / Qoder** 等当前环境。

> **命令参数** → [../cli/grok.md](../cli/grok.md)  
> **能力档 / 费用** → [../models.md](../models.md)  
> **跨栈门禁** → [../external-cli.md](../external-cli.md)

## 默认模型

```bash
grok models
# Default model: grok-4.5
```

Loop prompt 可写：

```text
当前模型：grok-4.5（Grok CLI）
方向：按 workflow 推进一轮。
```

## 与 Cursor 的分轨（grok CLI 优先）

| 任务 | 优先 |
|:-----|:-----|
| 架构 / ADR / 方案首次起草 | **`grok -p -m grok-4.5`**（CLI 可用时） |
| Arch-First 审查 | **`grok -p`** 独立实例（≠ 综合主笔会话） |
| 挖 bug / 根因 | **`grok -p`** 或当前环境子 agent |
| 大量改代码 | **Cursor `Task`**（Composer / Auto）— **不用** grok CLI |
| Loop 父 agent 调度 | **Cursor**（`/loop`、`Task`、并行 wave） |

**规则**：父 agent 在 **Cursor IDE 内**时，架构/doc 轨用 **Shell `grok -p`**（**不是** Cursor `Task` Grok，也**不要**切聊天模型到 Grok）。仅当 `which grok` 失败或人类写明禁用时，降级 Cursor Grok `Task`。

## 周期调度

Loop 父 agent 通常在 **Cursor** 跑 `/loop`，架构子任务用 Shell 调 `grok -p`，**须**：

```bash
GROK_LOOP_AUTH='--no-plan --permission-mode bypassPermissions --always-approve'
grok $GROK_LOOP_AUTH -m grok-4.5 -p "$prompt"
```

见 [../cli/grok.md](../cli/grok.md)。

## 子 agent / 委派

| 方式 | 说明 |
|:-----|:-----|
| **Shell `grok -p`** | Loop 父 agent 委派（**默认**；**Cursor 内也用 Shell**） |
| **交互 `grok`** | 人类结对；Loop tick 内少用 |
| **`grok agent`** | headless agent 子命令（SDK/relay）；Loop 默认不用 |

**同栈禁止**：已在 Grok 交互会话时，**不要**再起 `grok -p`（续聊或 `--continue`）。

## 外部 CLI

命令全文 → [../cli/grok.md](../cli/grok.md)。

## 限制

- 需本机安装 `grok` 且已 `grok login`  
- `grok-4.5` 为当前 CLI 默认；模型列表以 `grok models` 为准  
- **禁止**用 grok CLI 写 prod 实施轨（除非人类本 tick 明确授权 grok 改码）
