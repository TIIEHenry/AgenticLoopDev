---
title: "Loop 运行时 — Cursor"
type: guide
status: accepted
phase: N/A
updated: 2026-07-09
summary: "在 Cursor 中运行开发 Loop：/loop 调度、Task 子 agent、规则与 hooks。"
---

# Cursor 运行时

**默认模型（实践）**：架构 / ADR / 挖 bug 默认 **Grok**；大量改代码仍常绑 **Composer**（代码性价比更高）。见 [models.md](../models.md)。

## Cursor 内子 agent 与模型

- 可用不同 **`subagent_type`**（coder、explore、reviewer…）  
- **默认**子 agent **不传 `model`**，与父 agent 同模型（费用与 `.cursor/rules/subagent-model-policy.mdc`）  
- **Grok**：架构 / ADR 主笔与挖 bug **默认**；loop prompt 写明 `当前模型：Grok`  
- **Composer**：实施轨常用（代码性价比优于 Grok）  
- **GPT 5.5 / Opus**：仅 loop prompt **明文授权**时用于**主架构/方案文档**或**挖 bug**；**不得**用于写代码 → [models.md § 代码](../models.md#代码写代码--大量改代码)

## 周期调度

```text
/loop 10m <prompt 或 @文件>
/loop cancel
```

- 固定间隔：`5m`、`30s`、`2h` 等  
- 无间隔：动态模式，agent 自选下次 delay（`/loop` 自带说明）  

启动示例：

```text
/loop 10m @dev/loop/loop-prompt.txt
当前模型：Composer。方向：按 workflow 推进一轮。
```

或 `@dev/loop/loop-prompt.txt` + 模型与方向。详见 [prompts.md](../prompts.md)。

## 子 agent

IDE 内 **`Task` 工具**：

| 参数 | 说明 |
|:-----|:-----|
| `description` | UI 标题 |
| `subagent_type` | `coder`、`explore`、`shell`、`generalPurpose` 等 |
| `prompt` | 完整任务说明 |
| `run_in_background` | 异步，不阻塞父会话 |

**不传 `model`** — 子 agent 与父 agent 同模型（见 `.cursor/rules/subagent-model-policy.mdc`）。

并行 wave 见 [orchestration.md](../orchestration.md) 与 [parallel-loop-waves.md](../agent-playbooks/parallel-loop-waves.md)。

## Cursor 专属规则（可选）

Loop 契约 **SSOT 仅在 [`dev/loop/`](../INDEX.md)**，由 `/loop` 或 `@dev/loop/loop-prompt.txt` **显式触发**；不在 `.cursor/rules/` 重复注入 loop 工作流。

| 位置 | 用途 |
|:-----|:-----|
| [`dev/loop/`](../INDEX.md) | Loop 工作流、playbook、启动契约（**唯一 SSOT**） |
| `.cursor/rules/subagent-model-policy.mdc` | Cursor Task 子 agent 同模型、费用门禁（非 loop 专属，但 loop 须遵守） |
| `AGENTS.md` / `CLAUDE.md` | 项目向导与 loop 入口 |

## 外部 CLI

| 方向 | 规则 |
|:-----|:-----|
| **在 Cursor 内** | 用 `Task`；**不要** `agent -p`（同栈重复） |
| **从 Claude Code / OpenCode 等调 Cursor** | **禁止**默认 `agent -p`；prompt 须明文 **Cursor 可用** → [external-cli.md](../external-cli.md) |
| **从 Cursor 跨栈** | 仅 prompt 授权时 `claude -p` / `opencode run -m …`（烟测仍优先 `Task`） |

## 限制

- Multitask / 后台 worker 受账号账单与策略影响  
- Cloud agent 环境与本地 loop skill 能力可能不同  
