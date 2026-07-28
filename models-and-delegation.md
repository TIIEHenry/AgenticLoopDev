---
title: "模型能力与委派策略"
type: guide
status: accepted
phase: N/A
updated: 2026-07-28
summary: "任务→运行时/委派；同栈内置 vs 跨栈 CLI（门禁见 external-cli）；多视角与验收。"
---

# 模型能力与委派策略

Loop 父 agent 选「谁干活」时，先看**当前在哪个运行时**，再看**任务类型**与**是否跨环境**。

> **能力对比 / 费用硬门禁 / 方案主笔** → [models.md](models.md)。  
> **人类写什么** → [human-input.md](human-input.md)。  
> **跨栈 CLI 门禁** → [external-cli.md](external-cli.md)；**命令** → [cli/INDEX.md](cli/INDEX.md)。

## 费用门禁（摘要）

**Opus、GPT 5.5**：无 loop prompt **明文授权**不得使用。细则与降级 → [models.md § 费用维度](models.md#费用维度硬门禁)。

**Codex GPT（迁移授权）**：关键架构决策与 `dev/plans/`、`dev/decisions/`、`docs/architecture/` 主笔 → Cursor 父 agent 可用 **`codex exec`**（本地默认 `gpt-5.5`）；**禁止**写 prod 代码。见 [`loop-prompt.txt`](loop-prompt.txt) `Model Authorization`。

## 同栈内置，跨栈才 CLI

**当前父 agent 已在某运行时内时，同栈能力用内置委派，不要起同栈 CLI。** 完整表与 Cursor / OpenCode / 烟测门禁 → [external-cli.md](external-cli.md)。

**Cursor 内**：可用不同 `subagent_type`，但**默认不传 `model`**（与父同模型）。GPT 5.5 / Opus 须 prompt 明文且不得写代码 → [models.md](models.md)。

## 任务 → 运行时 / 委派

费用档与「默认用哪款模型」→ [models.md § 费用 × 任务](models.md#费用--任务矩阵速查)。下表只答**走哪条委派路径**：

| 任务 | 优先委派 |
|:-----|:---------|
| 主架构 / ADR（首次） | 强架构主笔（见 models）；Cursor `Task` 或已授权 `codex exec` |
| 主架构 / ADR（修订） | 当前环境主笔（Grok / kimi-k3）；跨栈仅明文授权 |
| 方案多视角评估 | 并行 reviewer / plan-analyst（不写代码） |
| **架构设计审查（Arch-First）** | ≥中强独立审查（默认 Grok/k3）；见 [architecture-first-design.md](agent-playbooks/architecture-first-design.md)；禁 Composer 单审 |
| 方案写作、润色 | 当前环境；叙述可 Composer |
| 大量实现 | **当前环境模型**（不重议选型）；前端可跨栈 kimi-k3（见 models） |
| 挖 bug / 根因 | 当前环境；贵模型须 prompt 授权 |
| adb / 烟测 | **当前环境子 agent** → [external-cli.md](external-cli.md) |

## 多视角评估（方案阶段）

**工程质量优先**前提下，**方案 / 架构首次起草与重大修订**鼓励多 agent **并行多视角**：

| ✅ 做法 | ❌ 不做 |
|:--------|:--------|
| 强架构主笔 + 并行 reviewer / plan-analyst 提质疑 | 弱模型各自改一版方案正文 |
| Review-Question-Resolve：问题清单 → 强模型改 doc | 为「好看」 spawn Opus+GPT+mimo 各写全文 |
| 费用可控：评估轨用中档模型，贵模型仅 prompt 授权 | 实施阶段仍用贵模型写代码 |

**实施阶段**：固定当前环境模型 → [models.md § 实施阶段](models.md#实施阶段少纠结模型)。

## 验收：单路收口

**Overall Verification** 每轮仍要跑（见 [workflow.md](workflow.md)），但 **不要**为验收再开多路 reviewer 各写一份评审报告。

**Wave 3 维度评审**（architecture / tester / security）**仅** plan/ADR 首次或重大修订 tick；**实施 tick 跳过 Wave 3** → [parallel-loop-waves.md § Wave 3](agent-playbooks/parallel-loop-waves.md#wave-3--评审触发条件)。

| ✅ 验收做法 | ❌ 不做 |
|:------------|:--------|
| **当前 tick 父 agent**对照 Loop Goal、roadmap、测试、diff 做**单路** PASS/FAIL | 验收轨再 spawn 3+ 视角「再评一遍」 |
| 弱模型验收：只核对清单与证据，质疑项**反馈给强模型**改 doc | 验收用 Opus + GPT 各写总结 |
| 方案未闭合：记 blocking question，下轮强架构 + 多视角评估改 plan | 用多视角验收代替实施 |

## 技术授权示例

人类输入格式见 [human-input.md](human-input.md)。技术授权（非任务）示例：

```text
Cursor 可用：授权 agent -p 跑架构 doc
本轨跨栈 OpenCode：父 agent 不在 OpenCode 且 prompt 明文时，`opencode run -m kimi-for-coding/k3`
```

## 相关

- [models.md](models.md) — 能力量化与费用  
- [human-input.md](human-input.md) — 人类输入  
- [runtimes/INDEX.md](runtimes/INDEX.md) — 运行时选型  
- [external-cli.md](external-cli.md) — CLI 门禁  
- [cli/INDEX.md](cli/INDEX.md) — CLI 命令  
- [parallel-loop-waves.md](agent-playbooks/parallel-loop-waves.md)  
