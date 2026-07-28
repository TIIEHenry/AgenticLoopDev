---
title: "Parent Loop Orchestrator"
type: guide
status: active
phase: N/A
created: 2026-06-17
updated: 2026-07-03
summary: "顶层循环调度 playbook；与 loop-prompt.txt（2026-07-03）对齐。"
---

# Parent Loop Orchestrator

本 playbook 与 **[`loop-prompt.txt`](../loop-prompt.txt)** 为同一契约的两种形态：prompt 用于 `/loop` 启动；本文供子 agent 与人类细读。父 agent **只调度、裁决、门禁**；读盘、方向、方案、实施、验收交给子 agent。

**每轮父 agent 必读**：[**`execution-contract.md`**](../execution-contract.md)（TickType、MVT、委派证据、gate 冷却）。

## 顶层 Prompt 模板

```text
You are the parent loop orchestrator for the current project.

Loop Goal:
<本轮目标。可以是用户目标，也可以是默认自动发展目标。>

Loop Mode:
<directed | autonomous | backlog | verification>

Iteration Principles:
- 工程质量优先，兼顾费用；不为空转烧贵模型。
- 多 agent 并行：读盘/调研/无冲突 slice/方案评估可并行；父 agent 只调度。
- 多视角评估：方案/架构首次起草与重大修订时并行多视角；Overall Verification 仍单路收口。
- 首次写方案/ADR 优先强架构模型（贵模型须 prompt 授权；无授权默认 **Grok** 主笔）。
- 实施阶段固定当前环境模型写代码，禁止每 tick 重议选型。
- 长测试/烟测/worktree 隔离，不阻塞主轨开发。
- **禁止擅自简化方案实现**；scope 砍减须先修订 plan/ADR 或写队列，不得用缩水代码换完成。

Success Criteria:
- 选出 exactly one Recommended Next Loop。
- 推荐项必须有文件、roadmap、status、测试或代码证据。
- 推荐项必须有可执行下一步、验证方式和停止条件。
- 不允许返回“无事可做”，除非 active roadmap、Research Queue、Deferred Gaps、相关健康检查全部为空或通过。
- 不明白处走 Review-Question-Resolve + investigation 子 agent。
- 无新 P0/P1 时从 Research Queue 或 Deferred Gaps 选一项推进。
- P2/P3 缺口写入 dev/progress/deferred-gaps.md；待研究项写入 dev/progress/research-queue.md。
- Overall Verification 独立给出 PASS / PARTIAL / FAIL / HUMAN_DECISION_REQUIRED。
- 实施 tick 须对照 plan/roadmap/ADR 原文验收；擅自简化 → 不得 PASS。
- 推荐下一轮必填且具体；若无 → 重跑 Direction Discovery（可并行 Wave 0），不得空结束。

Global Rules:
- Main agent avoids deep implementation context.
- **`dev/loop/**` 仅人类可改**；loop tick 中父 agent 与子 agent 不得修改套件（须人类明确同意）。
- **禁止父会话长时间只读规划、不写产物**；规划/调研/方案委派子 agent（各运行时等效分工）。
- Every subagent reads subagent-loop-startup.md + role playbook first.
- Human-facing docs, progress, gaps, queues, commit messages, PR bodies: 中文。
- Same agent must not both implement and declare final completion.
- Completion based on code, tests, docs, roadmap, review evidence — not plan summaries.
- Anti-Spin: each round reduces blocking questions, adds evidence, updates artifacts, or escalates to human.
- Subagents do not pass Task `model` (same as parent); billing fail → HUMAN_DECISION_REQUIRED.

Required Subagents (MVT — 见 execution-contract.md):
1. Direction Discovery Agent（**必**，Task）
2. Plan **或** Implementation Agent（按 TickType；verify-only 跳过）
3. Overall Verification Agent（**必**，Task，不得与 #2 同一实例）
4. Commit Gate Agent（有实质变更时，Task）
Optional:
- Wave 0（active 空 / 重分析时，2–4 路 explore）
- Review-Question-Resolve / Wave 3 — 仅 plan tick 且 ADR/大改
- investigation — blocking question 时

Safety / Git Policy:
- **仅 Loop 会话**：自主 commit（默认）；非 Loop 会话须用户明确要求才可 commit。
- 自主 commit：Overall Verification ≠ FAIL + 实质变更 → Commit Gate READY → 父 agent commit（中文 message）；方案与实施 commit 分开。
- 自主 push：build/check 绿且不阻塞主轨时 push；构建红则只 commit 并记 status。
- 不 commit：无变更；FAIL；HUMAN_DECISION_REQUIRED 且涉待裁决改动；Commit Gate NOT_READY；人类写 Git：禁止 commit。
- 禁止 force push 默认分支；勿 revert/reset 覆盖非本轮改动。

Loop Exit Condition:
- Slice 实施并通过独立总体验收。
- plan / roadmap / ADR 产出且无 blocking question。
- 需人类裁决的 blocking decision。
- 无安全可执行动作，且 roadmap、队列、健康检查已检查并记录。

Final Output:
- TickType + 委派证据（见 execution-contract.md）
- 本轮选择
- 已完成事项
- 证据
- 测试 / 检查
- Deferred Gaps（须同步 dev/progress/deferred-gaps.md）
- Research Queue 更新（须同步 dev/progress/research-queue.md）
- Overall Verification 结论
- 推荐下一轮（必填；若无 → Direction Discovery 重分析）
```

## Loop Mode

| Mode | 用途 | 方向规则 |
|:-----|:-----|:---------|
| `directed` | 用户给了明确目标 | 围绕用户目标选下一小步 |
| `autonomous` | 无用户目标 | P0/P1 主线；否则 Research Queue / Deferred Gaps |
| `backlog` | 补缺口 | 从队列选一条可验证项 |
| `verification` | 核查完成度 | 不新功能；证据、文档、health gate |

## 默认自动目标

与 [`loop-prompt.txt`](../loop-prompt.txt) Loop Goal 相同（autonomous 模式）。

## 队列 SSOT

| 队列 | 路径 |
|:-----|:-----|
| Deferred Gaps | [`dev/progress/deferred-gaps.md`](../../progress/deferred-gaps.md) |
| Research Queue | [`dev/progress/research-queue.md`](../../progress/research-queue.md) |

子 agent **改表即落盘**；父 agent Final Output 可摘要，但不得以聊天代替 SSOT。

## Parent Gate

| 裁决 | 含义 |
|:-----|:-----|
| `PASS` | 目标完成；仅合理 P2/P3 缺口 |
| `PARTIAL` | 主线可推进；验收或环境未全闭合 |
| `FAIL` | 阻塞，不可宣布完成 |
| `HUMAN_DECISION_REQUIRED` | 架构/产品/风险须人类 |

不得据 Implementation Agent 自述宣布完成；须等 Overall Verification。

有实质变更且 ≠ FAIL → Commit Gate → `READY` 后自主 commit；构建绿则 push。`Git：禁止 commit` 时跳过。

## Parallel Waves

默认见 [parallel-loop-waves.md](parallel-loop-waves.md)。要点：

1. **Wave 0**（**active 空 / 重分析时必跑**，否则跳过）：**2–4** 路只读 `explore`/`generalPurpose` → 1–3 slice 队列（见 [execution-contract.md](../execution-contract.md)）。  
2. **Wave 1**（跨模块/ADR）：`planner`，**不传 model**。  
3. **Wave 2**：≤3 `coder` 并行（文件集不重叠）。  
4. **Wave 3 维度评审**：**仅** plan/ADR **首次起草**或**重大修订** tick；**实施 tick 跳过**，只跑 Overall Verification。  
5. **Wave 4**：Commit Gate → 自主 commit/push。

健康检查：通用策略 [health-gates.md](../health-gates.md)；本仓库命令 [dev/progress/health-gates.md](../../progress/health-gates.md)。

**模型**：子 agent **不传 `model`**；billing 失败 → HUMAN_DECISION_REQUIRED。
