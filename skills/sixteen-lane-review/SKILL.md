---
name: sixteen-lane-review
description: >-
  Sixteen-lane parallel review: split the tree into 16 non-overlapping slices,
  write one findings doc per lane, then a different subagent per lane verifies
  the findings and writes a solution plan. Project-agnostic. Do not auto-invoke.
  Use only when the user names this skill, uses /sixteen-lane-review or
  @sixteen-lane-review, or says 16并行分析 / 十六路并行审查.
disable-model-invocation: true
title: "Skill: sixteen-lane-review"
type: guide
status: accepted
phase: N/A
updated: 2026-09-24
summary: "Opt-in 16-lane review: parallel findings, then a different agent verifies and writes the plan. No project names."
---

# 十六路并行审查

**跨项目通用。** 不写任何仓库专名、模块名或构建命令。父代理只切分、派发、汇总。分析与方案都由子代理写。

两波，顺序固定：

1. **分析**：16 个子代理各读一块互不重叠的代码，各写一份发现稿。
2. **核查写方案**：分析稿落盘后，**另 16 个实例**（禁止 resume 原作者）对照活码核对，不成立的删掉，成立的写成方案稿。

默认不改生产代码、不改测试、不 commit。

## When to apply

**不自动触发。** 仅当用户显式调用：

| 方式 | 示例 |
|:-----|:-----|
| 斜杠 / @ | `/sixteen-lane-review`、`@sixteen-lane-review`、`@dev/loop/skills/sixteen-lane-review/SKILL.md` |
| 口令 | **「16并行分析」**、**「十六路并行审查」** |

「帮我看看有没有 bug」「审查一下」**不算**调用。不要因此自行启动。

与另外两份技能分工：本技能产出发现稿 + 方案稿。方案定稿前的架构审查走显式调用的 [architecture-first-solution](../architecture-first-solution/SKILL.md)。同一任务多路候选再综合走显式调用的 [multi-party-design-review](../multi-party-design-review/SKILL.md)。本技能**不**代替那两份，也**不**在其未获调用时开跑。

## 硬规则

- 子代理**不传** `model`，与父代理同模型。本 tick 没有人类明文点名的付费档，不得传。
- 子代理报 billing / unpaid invoice → 停止再派，向用户报告，不换模型重试。
- 每路只有一个输出文件。两路不得写同一路径。
- 禁止改生产代码、测试、以及本次输出目录以外的文件。工作区里已有的未提交改动只读，不改。
- 禁止 commit、切分支、merge、rebase、reset、stash。
- 发现必须来自本次读到的活码，带路径和行号。读不到就不算。禁止编造。每路最多 **5** 条。没有就写 0 条。
- 用户指出的已有审查 / 方案里记过的问题，不要再当新发现。活码里已经按那个方向改过的，也不要再报。
- 核查者必须是**新实例**。禁止 `resume` 写发现稿的那个代理来写方案。

## 输出位置

用户指定了目录就用那个目录。否则：仓库已有 `dev/plans/` 就写那里；没有就写 `docs/reviews/`（没有则创建这一层）。

日期用当天 `YYYY-MM-DD`。编号 `r01`–`r16`。

| 波 | 文件 |
|:---|:-----|
| 分析 | `review-<date>-rNN-<slug>.md` |
| 方案 | `review-<date>-rNN-<slug>-plan.md` |
| 父代理索引 | `review-<date>.md`（新建；不要改已有索引文件） |

文档若有仓库自己的 frontmatter 规范，照那个写。没有则用：

```yaml
---
title: "<一句话>"
type: audit
status: draft
phase: N/A
created: YYYY-MM-DD
updated: YYYY-MM-DD
summary: "<一行>"
---
```

方案稿的 `type` 用 `plan`。正文语言跟仓库既有方案；没有则中文。

## 父代理

### 1. 切 16 路

读仓库顶层，把**源码**切成 16 块。块与块的路径前缀不得相交。

- 自然块不足 16：把最大的块再切开，直到 16。
- 自然块多于 16：把相邻小块并成一块，直到 16。
- 某块几乎没有源码：仍占一路，发现稿写「范围内无源码」。

每路给一个短 slug（英文小写连字符）。不要把仓库专名写进技能或提示词的固定部分；slug 来自这次看到的目录名。

切分表先写给用户：路号、路径前缀、发现稿路径、方案稿路径。然后**同一条消息里**派齐 16 个分析子代理。

### 2. 分析提示词

每路一份，自包含。必须写明：

- 仓库根的绝对路径
- 只许读的路径前缀；越界不算
- 只许创建的那一个发现稿路径
- 最多 5 条；0 条合法
- 每条要有：编号 `rNN-N`、严重度（数据丢失或越权为高，用户可见行为错误为中，边界为低）、症状、带行号的代码引用、为什么是问题、一句话方向
- 用户给了已有审查路径就列进去，命中则跳过
- 写完回读该文件确认存在
- 回复只要：路径、条数、每条一句话

### 3. 等分析落盘

16 份发现稿都在磁盘上之后，再派核查。缺的那路只重派**那一路**的分析，不要重派已写完的。

### 4. 核查提示词

每路一个**新**子代理。提示词必须附上该路发现稿路径，并要求：

- 逐条打开引用的文件，核对行号是否仍是那个行为
- 每条标记 `hold` / `drop` / `weaken`。`drop` 的不进方案。`weaken` 降级并写明读到的反证
- 只为 `hold` 与 `weaken` 写方案稿，路径用切分表里的方案路径
- 方案只写怎么改：问题类（一句话）、不变量、要动的符号或文件、明确不改什么、怎样本地验证（有测试名就写测试名，没有就写应新增的断言意图）
- 不占决策记录编号，不改生产，不改发现稿
- 回复：路径、hold/drop/weaken 计数、方案是否写了

### 5. 索引

两波都结束后，父代理新建 `review-<date>.md`：16 路路径、每路条数、hold 数、方案路径。不改其它索引。然后用这张表向用户汇报。

## 子代理回复

分析子代理和核查子代理的最终回复都只要父代理汇总需要的那几行，不要复述全文。
