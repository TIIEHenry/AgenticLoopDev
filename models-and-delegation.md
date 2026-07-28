---
title: "模型能力与委派策略"
type: guide
status: accepted
phase: N/A
updated: 2026-07-09
summary: "各运行时模型绑定、费用门禁、Cursor CLI 授权、委派策略。"
---

# 模型能力与委派策略

Loop 父 agent 选「谁干活」时，先看**当前在哪个运行时**，再看**任务类型**与**是否跨环境**。

> **能力排序（架构 / 写作 / 代码 / 费用等）** → [models.md](models.md)（量化序关系与**费用硬门禁**）。

## 费用门禁（优先于能力）

**Opus、GPT 5.5** = 高 / 极高费用档。**无 loop prompt 明文授权，父 agent 与子 agent 均不得使用**（不传 Task `model`、不自发切换 IDE、不以「任务太难」自行升级）。

**Codex GPT（迁移授权）**：关键架构决策与 `dev/plans/`、`dev/decisions/`、`docs/architecture/` 主笔 → Cursor 父 agent 可用 **`codex exec`**（本地默认 `gpt-5.5`）；**禁止**写 prod 代码。见 [`loop-prompt.txt`](loop-prompt.txt) `Model Authorization`。

| 情况 | 行为 |
|:-----|:-----|
| prompt 写明 `当前模型：GPT 5.5` 等 | 本 tick 父 agent 可用；子 agent 另需轨内 `model=` 明文 |
| 无写明，架构仍难 | **Grok** 主笔 + blocking question，或 `HUMAN_DECISION_REQUIRED` 请人类改 prompt |
| 想为验收 spawn 贵模型 | **禁止** |
| billing / unpaid invoice | `HUMAN_DECISION_REQUIRED`，暂停 spawn |

详见 [models.md § 费用维度](models.md#费用维度硬门禁)。

## 运行时与模型

| 运行时 | 模型绑定 | 详见 |
|:-------|:---------|:-----|
| **Cursor** | 架构/挖 bug 默认 **Grok**；实施常 Composer | [models.md](models.md) · [runtimes/cursor.md](runtimes/cursor.md) |
| **Claude Code** | **不固定** — prompt 必填 slug | [models.md](models.md) |
| **Antigravity** | **不固定** — 常见 `gemini-3.5-flash`、`gemini-3.1-pro` | [runtimes/antigravity.md](runtimes/antigravity.md) |
| **OpenCode** | **`-m provider/model`**（见 [opencode.md](runtimes/opencode.md)） | [models.md](models.md) |
| **Codex** | 本地配置 — prompt 必填 slug | [runtimes/codex.md](runtimes/codex.md) |

**Cursor 内**：可用不同 `subagent_type`，但**默认不换计费模型**（子 agent 不传 `model`）。**GPT 5.5 / Opus** 须 loop prompt **明文授权**且仅限方案/架构文档，见 [models.md § 费用维度](models.md#费用维度硬门禁)。

## 硬规则：同环境用内置，跨环境才 CLI

**当前父 agent 已在某运行时内时，委派「同栈」能力必须用该环境的内置方式，不要起同栈 CLI。**

| 当前环境 | ✅ 本子 agent | ❌ 同栈 CLI |
|:---------|:-------------|:-----------|
| **Cursor** | IDE `Task` | `agent -p` |
| **Claude Code** | 会话 / `--agents` | `claude -p` |
| **Antigravity** | `invoke_subagent` (subagents) | `agy -p` |
| **OpenCode** | 当前会话内子 agent | `opencode run`（**例外**：`-m` 换另一模型） |
| **Codex** | 当前会话 / `exec resume` | 无必要时不并行同栈 exec |

**跨环境 CLI** → [external-cli.md](external-cli.md)。

## Cursor CLI 门禁（`agent -p`）

**当前 Loop 不在 Cursor 中跑**（Claude Code、OpenCode、Codex、纯 shell 等）时：

| 规则 | 说明 |
|:-----|:-----|
| **禁止默认** | **不得**因「需要 Composer / 挖 bug / 写架构 doc」就调用 `agent -p` |
| **须人类明文** | loop prompt / [`loop-prompt.txt`](loop-prompt.txt) / 人类消息 **必须**写明 **Cursor 可用** |
| **无授权** | 用当前运行时内置能力；架构 doc 记 blocking question 或 `HUMAN_DECISION_REQUIRED` |
| **在 Cursor 内** | 用 `Task`，**仍不用** `agent -p`（同栈重复） |

```text
Cursor 可用：本轨可用 agent -p --trust 写 dev/plans/foo.md（Composer）
当前模型：mimo-v2.5-pro（Claude Code）
方向：架构 doc 由 Cursor CLI 主笔，本轨只做实施
```

**不算授权**：文档里写「用 Composer」但未写 **Cursor 可用**；agent 自行判断「应该开 Cursor」。

## OpenCode CLI 门禁（`opencode run`）

**当前 Loop 在 OpenCode 会话内**时：

| 规则 | 说明 |
|:-----|:-----|
| **禁止默认** | **不得**用 `opencode run` 做烟测、改码、挖 bug（用**会话内子 agent**） |
| **换模型例外** | 仅当须 `-m` **与当前会话不同**的模型时，可 `opencode run -m …` |
| **不在 OpenCode** | 跨栈 `opencode run` 按需；烟测仍**优先当前环境子 agent** |

## Antigravity CLI 门禁（`agy -p`）

**当前 Loop 在 Antigravity 会话内**时：

| 规则 | 说明 |
|:-----|:-----|
| **禁止默认** | **不得**在交互式 TUI 会话中，对同工作区再调用 `agy -p`（使用内置 `invoke_subagent`） |
| **跨栈** | 当父 agent 在 Cursor/Claude Code，但需要使用 Gemini 模型且明文授权时，可调用 `agy --model <slug> -p` |

## 任务 → 运行时 / 委派建议

| 任务 | 优先 | 费用 |
|:-----|:-----|:-----|
| 主架构 / ADR（**首次起草**） | **强架构优先**（GPT 5.5/Opus 须授权；否则默认 **Grok**） | 高/中 |
| 主架构 / ADR（修订） | Cursor + **Grok**（或已授权强模型；无 Grok 则 Composer） | 中～高 |
| 方案多视角评估 | 并行 reviewer / plan-analyst | 可控；不写代码 |
| 方案写作、润色 | **Grok**（叙述亦可 Composer） | 中 |
| 大量实现 | **当前环境模型**（**不重议选型**） | 低～中；**禁止** GPT / Opus |
| 挖 bug / 根因 | **Grok 及以下** | 中；GPT/Opus **须 prompt 授权** |
| adb / 烟测 | **当前环境子 agent**（隔离/后台） | 低 |

## 多视角评估（方案阶段）

**工程质量优先**前提下，**方案 / 架构首次起草与重大修订**鼓励多 agent **并行多视角**：

| ✅ 做法 | ❌ 不做 |
|:--------|:--------|
| 强架构主笔 + 并行 reviewer / plan-analyst 提质疑 | 弱模型各自改一版方案正文 |
| Review-Question-Resolve：问题清单 → 强模型改 doc | 为「好看」 spawn Opus+GPT+mimo 各写全文 |
| 费用可控：评估轨用中档模型，贵模型仅 prompt 授权 | 实施阶段仍用贵模型写代码 |

**实施阶段**：固定当前环境模型，**禁止**每 tick 重议选型 → [models.md § 实施阶段](models.md#实施阶段少纠结模型)。

## 验收：单路收口

**Overall Verification** 每轮仍要跑（见 [workflow.md](workflow.md)），但 **不要**为验收再开多路 reviewer 各写一份评审报告——避免空转与重复成本。

**Wave 3 维度评审**（architecture / tester / security）**仅** plan/ADR 首次或重大修订 tick；**实施 tick 跳过 Wave 3**，只跑单路 Overall Verification → [parallel-loop-waves.md § Wave 3](agent-playbooks/parallel-loop-waves.md#wave-3--评审触发条件)。

| ✅ 验收做法 | ❌ 不做 |
|:------------|:--------|
| **当前 tick 父 agent**对照 Loop Goal、roadmap、测试、diff 做**单路** PASS/FAIL | 验收轨再 spawn 3+ 视角「再评一遍」 |
| 弱模型验收：只核对清单与证据，质疑项**反馈给强模型**改 doc | 验收用 Opus + GPT 各写总结 |
| 方案未闭合：记 blocking question，下轮强架构 + 多视角评估改 plan | 用多视角验收代替实施 |

方案**评估**与**验收**分工见 [models.md](models.md)、[overview.md § 迭代原则](overview.md#迭代原则)。

## Loop prompt 如何覆盖默认

人类侧只写**模型 + 方向**，见 [human-input.md](human-input.md)。约束示例：

```text
当前模型：mimo-v2.5-pro
方向：实施与测试；架构方案只提问题不改正文
```

```text
当前模型：GPT 5.5（主架构）
方向：根据 status 问题清单改 dev/plans/
```

技术授权（非任务）：

```text
Cursor 可用：授权 agent -p 跑架构 doc
本轨跨栈 OpenCode：父 agent 不在 OpenCode 且 prompt 明文时，`opencode run -m …`
```

## 相关

- [models.md](models.md) — **能力量化**  
- [runtimes/INDEX.md](runtimes/INDEX.md)  
- [external-cli.md](external-cli.md)  
- [parallel-loop-waves.md](agent-playbooks/parallel-loop-waves.md)  
