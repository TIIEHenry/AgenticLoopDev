---
title: "Loop 运行时 — Cursor"
type: guide
status: accepted
phase: N/A
updated: 2026-08-14
summary: "在 Cursor 中运行开发 Loop：/loop 须 notify_on_output 且替换已存在 loop；Task 子 agent；架构轨优先 grok CLI。"
---

# Cursor 运行时

**默认模型（实践）**：Loop 父 agent 常在 **Cursor** 调度；**架构轨一律 Shell `grok -p`**（跟 CLI default）；实施用 **Composer** `Task` 或 **Auto**。见 [models.md](../models.md)。

## Cursor 内子 agent 与模型

### 架构轨：Shell `grok -p`（**禁止 Task Grok**）

父 agent **在 Cursor IDE 内**跑 Loop 时，架构 / ADR / 方案 / 挖 bug / Arch-First **仍优先 Grok CLI**：

| ✅ 做法 | ❌ 禁止 |
|:--------|:--------|
| 父 agent 用 **Shell** 调 `grok -p`（默认不传 `-m`） | 用 **`Task`** 并指望 Cursor **Grok 模型档**做架构主笔/审查 |
| `which grok` 通过即默认走 CLI | 为架构轨把 Cursor 聊天模型切成 Grok（实施轨仍 Composer/Auto） |
| CLI 不可用 → 降级 `Task`（Grok） | 用 **Auto/Composer `Task`** 冒充架构终审；硬编无关 `-m` 空转 |

```bash
# Cursor 内 Loop 父 agent 委派架构/doc 的标准形态（Shell 工具 · 完全权限）
ROOT="$(git rev-parse --show-toplevel)"
GROK_LOOP_AUTH='--no-plan --permission-mode bypassPermissions --always-approve'
# 不传 -m → CLI default
grok $GROK_LOOP_AUTH -p "$prompt"
```

详见 [grok.md](grok.md) · [../cli/grok.md](../cli/grok.md) · [../external-cli.md](../external-cli.md)。

### 实施轨：`Task`（Composer / Auto）

- 可用不同 **`subagent_type`**（coder、explore、reviewer…）
- **默认**子 agent **不传 `model`**，与父 agent 同模型（费用与 `.cursor/rules/subagent-model-policy.mdc`）
- **本仓库可派档**：**Auto / Grok / Composer**（无 Cursor 侧 GPT/Opus/Sonnet 强架构轨）
- **Grok（Cursor 档）**：**仅** `grok` CLI 不可用时的架构降级；**不是** Cursor 内首选
- **Composer**：实施轨常用（相对 Auto 更强、更快，略贵）
- **Auto**：实施省钱档（略弱于 Composer、更慢、更便宜）
- **GPT / Opus**：Cursor **不派**；强架构走 **`grok -p`**；Qoder `ultimate` 等贵价须本 tick 人类明文 → [models.md](../models.md)

## 周期调度

```text
/loop 10m <prompt 或 @文件>
/loop cancel
```

- 固定间隔：`5m`、`30s`、`2h` 等
- 无间隔：动态模式，agent 自选下次 delay（`/loop` 自带说明）

### 必须配置 `notify_on_output`

Cursor 里 `/loop` 靠**后台 shell 定时打印 sentinel** 唤醒 agent。启动 sleep 循环时 **必须**给 Shell 配上 `notify_on_output`（`pattern` 匹配 tick 行），否则循环在终端空转、**不会**触发下一轮。

| 项 | 要求 |
|:---|:-----|
| **`notify_on_output.pattern`** | 匹配 sentinel，如 `^AGENT_LOOP_TICK_<purpose>`（勿匹配全部输出） |
| **`notify_on_output.reason`** | ≤5 词，说明在等什么（UI 显示为 Monitored …） |
| **`block_until_ms`** | 起循环时用 `0` 后台跑；勿把长 sleep 堵在前台 |
| **sentinel** | 唯一前缀 + JSON prompt；唤醒后读最新匹配行再执行 |

### 启动前替换已存在的 loop

**禁止**叠多条固定 sleep 循环。新开 `/loop`（或同目的 tick）时：

1. 查 terminals / 后台 shell，找已在跑的 `AGENT_LOOP_TICK_*` / `while true; sleep …` loop
2. **先停旧的**：`kill` 其 PID，并用 AwaitShell（或等价）吃掉完成通知，避免旧 tick 再唤醒
3. **再**起新循环，并带上 `notify_on_output`
4. 记下新 PID；用户 `/loop cancel` 或「停止 loop」时同样杀 PID + 消费完成通知

同一仓库 / 同一 purpose **只保留一条**活跃 loop。

固定间隔示意（agent 侧，非人类手敲）：

```bash
while true; do
 sleep 600
 echo 'AGENT_LOOP_TICK_imagekit {"prompt":"…"}'
done
```

对应 Shell 调用须带例如：`notify_on_output: { pattern: "^AGENT_LOOP_TICK_imagekit", reason: "loop tick" }`。
细则见 Cursor **loop** skill（`notify_on_output` 唤醒；禁止重复 fixed loop）。

启动示例（人类；Sticky 见 [human-input.md](../human-input.md)）：

```text
/loop 10m @dev/loop/loop-prompt.txt
<Sticky 调度不变量 — 见 human-input.md>
当前模型：Composer（Cursor · 实施轨）。架构/doc 用 Shell grok -p（跟 CLI default）。方向：按 workflow 推进一轮。
```

**Cursor 附加**（勿写进跨运行时 Sticky）：本机 `/loop` 须 `notify_on_output` 且替换旧 sleep → 上文。

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

同栈 / 跨栈门禁 → [../external-cli.md](../external-cli.md)。`agent -p` 命令 → [../cli/cursor.md](../cli/cursor.md)。

## 限制

- Multitask / 后台 worker 受账号账单与策略影响
- Cloud agent 环境与本地 loop skill 能力可能不同
