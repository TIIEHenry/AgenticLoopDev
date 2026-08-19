---
title: "Parallel Loop Waves"
type: guide
status: active
phase: N/A
created: 2026-06-18
updated: 2026-08-19
summary: "Parent Loop 并行 wave；Arch-First 与 Wave 3 Architecture 去重；Wave 4 字母槽本地 commit；关仓 push 见 worktree-closeout。"
---

# Parallel Loop Waves

父 agent 在每轮 loop 中**必须**用并行 wave 调度子 agent，避免串行空转。实现与总体验收仍串行；发现、评审、测试探测可并行。

> 关联：[parent-loop-orchestrator.md](parent-loop-orchestrator.md) · [review-question-resolve-loop.md](review-question-resolve-loop.md)

## 硬约束

| 规则 | 说明 |
|:-----|:-----|
| **读/评审最大化并行** | Wave 0 目标 4–6 路；**方案 tick** 可 Wave 3 维度评审；**实施 tick** 仅单路 Overall Verification |
| **写路径 per-slice 串行** | 每个 slice 仅一个 Implementation Agent；多 slice 时各 coder 文件集不得重叠 |
| **实施 ≠ 验收** | 同一子 agent 不得既改代码又宣布 Overall Verification PASS |
| **Multi-Slice** | 同 tick 最多 **3 个独立 slice** 并行 Wave 2（不同模块、无 prod 文件冲突） |
| **Anti-Spin** | Wave 0 后必须合成 slice 队列（1–3 项）+ 冲突矩阵；禁止「等用户」 |
| **模型** | 子 agent **默认不传 `model`**，与父同模型。**例外**： [architecture-first-design.md](architecture-first-design.md) 审查者在父为弱架构时可传 **中强** `model`（或已授权 codex 只审） |
| **目标** | **功能补齐（架构优先）**；冲突时 契约闭合 > 用户可见功能 > 文档 |

## Wave 0 — 发现（并行，只读）

**同一 message 内并行 launch**，目标 **4–6 路**（按项目模块拆分，以下为通用模板）：

| Agent | subagent_type | model | 职责 |
|:------|:--------------|:------|:-----|
| Feature Area A Gaps | `researcher` | **不传** | 主客户端 / UI / 对外契约缺口 |
| Feature Area B Gaps | `researcher` | **不传** | 服务端 / API / 集成缺口 |
| Core / Engine Gaps | `researcher` | **不传** | 核心引擎 / 共享库缺口 |
| Architecture Scan | `architecture` | **不传** | 契约/parity/模块边界；slice 是否闭合 SSOT |
| Test Health | `tester` | （可选） | 聚焦 test 命令、已知 red suite |
| Stub/Gap Grep | `generalPurpose` | （可选） | TODO/FIXME/stub/UNIMPLEMENTED |

> **项目定制**：各仓库在 `dev/progress/status.md` 或 `dev/parallel/active/` 中定义具体 Feature Area 名称与扫描范围（例如多模块 monorepo 按子目录拆分）。

父 agent 合成：**1–3 个独立 slice 队列** + 文件冲突矩阵；无冲突项可同 tick 并行 Wave 2。

## Wave 1 — 计划（可选，单 agent）

仅当 slice 跨 2+ 模块或需 ADR 时启动：

| Agent | subagent_type | model |
|:------|:--------------|:------|
| Plan Split | `planner` | **不传** |

输出：3–5 步可验证子步 + 测试命令；**不在此 wave 写代码**。

## Wave 2 — 实施（per-slice 串行；多 slice 可并行）

| 模式 | 说明 |
|:-----|:-----|
| **单 slice** | 1× `coder`，父 agent 不深入实现 |
| **Multi-Slice（≤3）** | 无 prod 文件重叠时，**同一 message 并行 launch 多个 `coder`**，每 slice 独立分支描述 + 测试命令 |

可与 Wave 2 **并行**（只读）：`researcher` 预读下一 slice 文件；`tester` 跑上一 slice 聚焦 test。

**禁止：** 两 coder 改同一 prod 文件；同一 coder 兼做 Overall Verification。

## Wave 3 — 评审（触发条件）

### 何时跑维度评审（并行）

**仅**当本轮 tick 属于以下之一：

- 产出或**首次起草** `dev/plans/*.md`、ADR、`dev/roadmap/active/` 新 phase
- 对已有方案/ADR 做**重大修订**（架构取舍、跨模块契约变更）
- 父 agent 显式标记 `Loop Mode: plan` 或 Review-Question-Resolve 未收敛

此时：

1. **先**跑 [Architecture-First](architecture-first-design.md)：**串行** 1 路独立审查（≥中强），写入委派证据。 
2. 可再 **并行** launch Testing / Security（按需；非强制满员）：

| Dimension | subagent_type | 何时需要 |
|:----------|:--------------|:---------|
| Architecture | `architecture` | **仅当本 tick 未跑 Arch-First**（已跑则跳过，避免双路架构泛评） |
| Testing | `tester` | 测试策略或 gate 变更 |
| Security | `security-auditor` | 权限/路径/MCP/敏感数据 |

维度 agent（Testing/Security）**只提质疑与清单**，不各自改方案正文；收敛由 plan-roadmap + 中强/强模型改 doc。Arch-First Reviewer 给出 Approve 系结论。

### 何时跳过维度评审

**实施 tick**（改 prod 代码、勾 roadmap checkbox、补测试、文档随代码）：

- **不** spawn Wave 3 维度评审
- **只**跑 **单路** Overall Verification Agent
- 聚焦 test + diff + 两队列 SSOT + roadmap

> 与 [workflow.md § 禁止](../workflow.md#禁止)「验收多份重复评审报告」一致；避免实施 tick 空烧 token。

### Overall Verification（每轮必跑）

| Agent | subagent_type | model |
|:------|:--------------|:------|
| Overall Verification | `reviewer` 或 `generalPurpose` | **不传** |

每 slice **独立**裁决 PASS / PARTIAL / FAIL / HUMAN_DECISION_REQUIRED。多 slice 可并行 launch 不同 verification 实例，父 agent 汇总。

> Arch-First Reviewer：**默认 Shell `grok -p --no-plan --permission-mode bypassPermissions --always-approve`**（**含 Cursor 内**；直接用、勿 login；见 [architecture-first-design.md](architecture-first-design.md)）。**仅** `grok` CLI 不可用时，才允许 Task 传**中强** `model`（如 Cursor Grok）——**不含**贵价。Task **默认禁止**传 `model`（除非用户显式要求或上述降级）。**不含** GPT 5.5/5.6、Opus、Qoder Ultimate——贵价仍须本 tick/本轨明文；审查义务 ≠ 授权。billing 失败 → HUMAN_DECISION_REQUIRED。

## Wave 4 — 提交（字母槽本地 commit）

日常实施 tick（非关仓）：

1. 每 slice Overall Verification ≠ FAIL
2. Commit Gate = READY
3. 聚焦 test 已绿
4. **每 slice 在本字母槽独立 commit**（中文 message）
5. **不**从字母槽 `git push origin main`。合入 `main` 与远程 push 走 merge 槽：单槽日常合入见 [worktrees.md §5](../worktrees.md#5-合并流程字母槽--merge-槽--main)；**波次关仓**见 [worktree-closeout.md](../worktree-closeout.md) P5。

父 agent 在关仓完成且 merge 槽构建绿之后，才通过 closeout P5 推 `main`。

## 父 agent 合成模板

每 tick 结束前输出：

```text
Wave 0 合成: <slice 队列 1–3 + 冲突矩阵>
Wave 1: 跳过 | <计划摘要>
Wave 2: <单/多 coder 并行摘要 + commit hash(s)>
Wave 3: 跳过（实施 tick）| <维度评审摘要（仅方案/大改 tick）>
Overall Verification: <每 slice 结论>
下一轮: <Sprint backlog 下一批>
```

## 何时开 parallel board

仍遵守 `dev/parallel/README.md`：10+ 文件 / 多 agent / 跨会话时才建 `dev/parallel/active/<topic>.md`；单 slice tick 不必建 board。
