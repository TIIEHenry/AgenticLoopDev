---
title: "Loop 健康检查 Gate（通用）"
type: guide
status: accepted
phase: N/A
updated: 2026-07-03
summary: "跨项目通用：何时跑聚焦/grand gate、冷却、verify-only 门禁；具体命令在各仓库 dev/progress/。"
---

# Loop 健康检查 Gate（通用）

> **跨项目通用层**：本文约定 **何时跑**、**跑哪类**、**冷却**、**skip**。  
> **具体命令**写在各仓库 **`dev/progress/health-gates.md`**，不在 `dev/loop/`。

## 两类 gate

| 类型 | 用途 | 默认频率 |
|:-----|:-----|:---------|
| **聚焦 gate** | 覆盖**本轮改动模块** | 有 prod/test 变更的 tick **至少 1 次** |
| **Grand gate** | 跨模块回归套件 | **冷却制**，见下 |

## 硬规则（防空转）

### 聚焦 gate

| 规则 | 说明 |
|:-----|:-----|
| **有变更必跑** | 本轮改了 prod 或测试 → 跑与改动域匹配的聚焦 gate |
| **同 gate 冷却** | 同一聚焦 gate（相同 `--tests` 模式或文档中的域行）在 **status 最近 2 条 tick 已绿** 且 **其间无该域 prod 变更** → **禁止**本轮再跑 |
| **替代动作** | 冷却命中时 Direction Discovery 须选 `implement` 或 `plan`，不得 `verify-only` |

### Grand gate

| 规则 | 说明 |
|:-----|:-----|
| **最短间隔** | 距 status 上一条 **grand gate 全绿** 记录 **≥ 8 个 tick**，除非满足「大 slice 闭合」 |
| **大 slice 闭合** | 满足任一：active roadmap 一整节 checkbox 全勾；单 tick **≥5 个 prod 文件**变更；人类在方向中写明「闭合后跑 grand」 |
| **禁止堆叠** | 同一 tick **不得** grand + 多域 complement gate 凑「超大总数」；grand 已跑则 complement 域 gate 延到下一 implement tick |
| **记录** | status 须写 `grand gate X/X` 或 `聚焦 <域> Y/Y`，便于下轮判冷却 |

### verify-only tick 门禁

`TickType: verify-only`（见 [execution-contract.md](execution-contract.md)）**仅在**以下全部成立时允许：

1. 距上次同类型 gate 全绿 **≥ 3 tick**，**或** 上轮有该域 prod 变更待回归  
2. **不是**连续第二个 `verify-only` tick  
3. status「Next」或人类方向**写明**验证目的（例如「Queue slice #184 入库后 sentinel」）  
4. **无** active roadmap 可勾选且 **无** Research Queue 项可在单轮形成 plan  

否则 Direction Discovery **必须**选 `plan` 或 `implement`。

### 文档 tick

仅改 `dev/`、`docs/`、`.md` → 可 skip 测试；status 记 **skip 原因**。不算 verify-only。

## 何时跑（摘要）

| 场景 | 建议 |
|:-----|:-----|
| `implement` tick 有 prod/test 变更 | 聚焦 gate（遵守冷却） |
| 大 slice 闭合 | 下一 tick 可 grand（仍受 8-tick 间隔约束，闭合可豁免间隔） |
| `plan` tick | 通常 skip；若改了测试基线则跑相关聚焦 gate |
| Direction Discovery「健康检查」 | **不得**作为连续 tick 的默认理由；须引用冷却表判定 |
| 环境不可用 | skip → deferred-gaps 或 status |

## 记录约定

- tick 输出与 `status.md`：**命令**、**通过数/总数**、或 **skip 原因**  
- 建议每条 gate 记录带标签：`聚焦 Queue 45/45` · `grand gate 115/115`  
- Grand 命名（如 `115/115`）由项目 `dev/progress/health-gates.md` 定义  

## 项目侧命令

集成编译与聚焦/grand gate 的**具体命令**写在各仓库 **`dev/progress/health-gates.md`**（不在 `dev/loop/`）。移植见 [porting.md](porting.md)。

## 相关

- [execution-contract.md](execution-contract.md) — TickType 与 MVT  
- [workflow.md](workflow.md) — 验证步骤  
- [deferred-gaps.md](../progress/deferred-gaps.md) — 手测/环境 defer  
