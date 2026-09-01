---
title: "Architecture-First Design"
type: guide
status: active
phase: N/A
created: 2026-07-28
updated: 2026-08-30
summary: "plan/非trivial 设计：问题类模板 + 独立架构审查（≥中强）；Cursor 技能不自动触发；Grok 子 agent 优先、CLI 其次；GPT 须本 tick 人类明文；与 Wave 3 / OV 划界。"
---

# Architecture-First Design

防复发设计门禁。Cursor 技能入口**不自动触发**（`disable-model-invocation`）：[skills/architecture-first-solution](../skills/architecture-first-solution/SKILL.md)（须先 [安装](../skills/INDEX.md)；仅 `/`、`@` 或明文要求）。Loop `plan` tick 门禁不受此限。

## 何时强制

| 触发 | Arch-First |
|:-----|:-----------|
| `TickType: plan`；首次/重大 ADR；局部 vs 结构取舍；非 trivial bugfix **设计** | **强制**（trivial 除外） |
| 已有 **Approve** 方案上的纯 `implement` | **不重复**；OV 对照方案原文 |
| 无方案却要大改 prod | 先切 `plan`，再本门禁 |

## 角色

| 角色 | 谁 | 做什么 |
|:-----|:---|:-------|
| 主笔 | Plan Roadmap Agent（或手动 skill 会话） | 步骤 1–4：问题类 → 选项 → 选定 → 草案 |
| **架构审查者** | 独立 ≥中强实例（**≠ 主笔**；通道见下） | 步骤 5：只读审查；**不得**与主笔同一实例 |
| 调度 | 父 agent | 收草案 → spawn 审查 → 合并 must-fix → 才允许大实施 |

## 主笔最小产出（步骤 1–4）

方案/ADR 中须可见：

1. **Problem class**（症状 / 类标签 / 复发机制 / 一句防复发目标）
2. **Options**（≥2，含 Reject 理由）
3. **选定设计**与不变量
4. 触点 / 非目标 / 验证

细节模板见 skill。主笔**不得**自宣 `Approve`。

## 架构审查者（步骤 5）

**模型**：≥ **中强架构**（默认 **Grok**）。**禁止** Composer / 弱档作为唯一审查者。见 [models.md](../models.md)。

**通道**（见 [models-and-delegation.md](../models-and-delegation.md)）：当前运行时**子 agent 模型列表含 Grok** → `Task` / Subagent 传该 slug（Cursor：列表最新 `cursor-grok-*`）。**禁止**此时默认 `grok -p`。列表无 Grok 才 Shell `grok -p`。独立审查 = **另一实例**，不是必须走 CLI 进程。

**费用硬门禁（审查 ≠ 授权）**：Arch-First /「架构审查需要更强模型」**不构成** GPT 5.5 / GPT 5.6 / Opus / Qoder Ultimate 的授权。无本 tick 人类明文时：

- 审查用 **Grok**（子 agent 优先）或 kimi-k3
- **禁止** Task `model=gpt-*` / `opus` / `ultimate`，也禁止因此拉贵价 CLI
- 认为必须用贵价 → `HUMAN_DECISION_REQUIRED`，不得自行升档

**降级**：子 agent 无 Grok 档且 `grok` CLI 不可用时，才改 kimi-k3 或其它中强——**不含贵价**。见 [parallel-loop-waves.md](parallel-loop-waves.md)。

审查清单与 Verdict：`Approve` / `Approve with changes` / `Reject`（同 skill §5）。

**Anti-Spin**：同一方案最多 **2** 轮；仍 Reject → `HUMAN_DECISION_REQUIRED`。

## 与 Wave 3 / OV

| 机制 | 职责 |
|:-----|:-----|
| **Arch-First Review** | 「该这么设计吗」— 草案后 **1 路串行**门禁 |
| Wave 3 Architecture 维 | 若本 tick 已跑 Arch-First → **跳过**第二路 architecture 泛评；Testing/Security 仍可按需 |
| Overall Verification | 「做完了吗」；`plan` tick 缺 `architecture-first-review`（非 trivial）→ 不得 PASS |

## 委派证据（plan tick）

```text
architecture-first-review: Approve | Approve with changes | Reject | skipped-trivial
architecture-first-reviewer: Task Grok <slug> | Shell grok -p --no-plan --permission-mode bypassPermissions --always-approve | <会话等价>
```

`Approve with changes` 须在合并修改后写最终态；未达 Approve（或合法 skip）不得开大范围 Wave 2。

## Trivial

单行笔误、无结构含义文案/日志 → `skipped-trivial` 并简述理由。有复发疑虑 → 不 trivial。
