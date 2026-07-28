---
title: "Subagent Loop Startup"
type: guide
status: active
phase: N/A
created: 2026-06-17
updated: 2026-07-03
summary: "所有开发子 agent 必读；与 loop-prompt.txt（2026-07-03）对齐。"
---

# Subagent Loop Startup

每个开发子 agent **第一份**读本文，再读角色 playbook。父 prompt 仍须提供本轮 role、goal、inputs、constraints、output format。

## Must Read

1. 仓库根 `AGENTS.md` 或 `CLAUDE.md`
2. 文档规范（若存在，如 `docs/DOCUMENTATION.md`）
3. `dev/progress/status.md`
4. **[`dev/progress/deferred-gaps.md`](../../progress/deferred-gaps.md)** — Deferred Gaps **SSOT**
5. **[`dev/progress/research-queue.md`](../../progress/research-queue.md)** — Research Queue **SSOT**
6. 父 agent 传入的 plan、roadmap、parallel board、代码路径或评审材料

仅读职责范围内模块文档。非 Direction Discovery / Overall Verification 且父 agent 未要求时，勿全库扫描。

验收与健康检查：通用策略见 [`dev/loop/health-gates.md`](../health-gates.md)；**本仓库命令**见 [`dev/progress/health-gates.md`](../../progress/health-gates.md)。

## Operating Rules

- 结论须有代码、测试、roadmap 或文档路径证据。
- plan/roadmap 文本是意图，不是证明。
- 保留无关 working-tree 改动。
- **`dev/loop/**` 为套件 SSOT：Loop tick 中不得修改**；仅人类明确同意后可改，并由人类/rsync 同步。
- 子 agent **不 commit/push**（父 agent 在 Commit Gate `READY` 后执行）。
- 不得为自己实施的工作宣布最终完成。
- 不得返回「无事可做」，除非 active work、两队列、健康检查均已空或通过。
- 无新高优方向时，从 Research Queue 或 Deferred Gaps **选一条**可执行项。

## Language Rules

- 更新文档、进度、roadmap、**两队列表**、commit message、PR 描述：**中文**。
- 代码符号、路径、命令、API、枚举、日志、测试输出：保持原文。
- 父 prompt 对单 artifact 指定其他语言时，仅该 artifact 例外。

## 队列写入（SSOT）

| 类型 | 写入位置 | 何时写 |
|:-----|:---------|:-------|
| P2/P3 或环境受限、不阻塞当前目标 | `deferred-gaps.md` | 当轮无法完成但已知缺口 |
| 须先调查/定稿再编码 | `research-queue.md` | 当轮只能产出问题清单或需 ADR |

**禁止**只在返回给父 agent 的文本里列 gap 而不改上表。闭合项：`Status` → `closed`，并在 `status.md` 记摘要。

## Completion Guardrails

不得声称完成，若：

- Loop 目标下仍有未勾 P0/P1 roadmap
- 必测/手测跳过且无记录（应写入 Deferred Gaps）
- 缺 status/roadmap/队列更新
- Deferred gap 缺 priority、reason、exit condition
- 证据仅来自本轮摘要、无代码/测试交叉
- 代码、测试、文档不一致

## Gap Classification

| Class | Meaning | Handling |
|:------|:--------|:---------|
| Blocking Question | 实施或完成前必须解决 | investigation 或 HUMAN_DECISION_REQUIRED |
| Clarification Question | 影响质量但可带假设推进 | 记录假设与验证路径 |
| Deferred Question | P2/P3 或环境限制 | → `deferred-gaps.md` |
| Research Topic | 未知方案、须调查 | → `research-queue.md` |
| Noise | 重复、无依据、过宽 | 丢弃并简短说明 |

## Deferred Gaps Format

写入 [`deferred-gaps.md`](../../progress/deferred-gaps.md)：

| ID | Priority | Gap | Why Deferred | Exit Condition | Track | Status |
|:---|:---------|:----|:-------------|:---------------|:------|:-------|
| D1 | P2 | 具体缺口（含文件/组件/测试引用） | 为何不阻塞本轮 | 可验证的闭合条件 | UI/Test/Docs/… | open |

## Research Queue Format

写入 [`research-queue.md`](../../progress/research-queue.md)：

| ID | Topic | Why It Matters | Discovery Needed | Expected Output | Status |
|:---|:------|:---------------|:-----------------|:----------------|:-------|
| R1 | 具体主题 | 产品/架构/维护价值 | 待回答问题 | plan、ADR、roadmap 或 closure | open |

## Default Output Contract

父 prompt 未指定时：

```text
Scope:
Facts:
Gaps:
Decisions Needed:
Proposed Next Step:
Tests / Verification:
Deferred Gaps:（若改表，写明 ID 与 dev/progress/deferred-gaps.md 已更新）
Research Queue Updates:（若改表，写明 ID 与 dev/progress/research-queue.md 已更新）
Risks:
```
