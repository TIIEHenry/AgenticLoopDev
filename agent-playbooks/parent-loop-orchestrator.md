---
title: "Parent Loop Orchestrator"
type: guide
status: active
phase: N/A
created: 2026-06-17
updated: 2026-11-02
summary: "顶层循环调度 playbook；任务源优先级；本 wake 续派；Wave 4 本地 commit；关仓见 closeout 转换表。"
---

# Parent Loop Orchestrator

先按 [porting.md 的项目侧绑定](../porting.md#项目侧绑定) 读取实际来源；显式未采用的旧来源不读、不建，无绑定旧项目保留默认布局。下文队列与 status 指实际绑定角色，不要求固定文件名或双队列。

本 playbook 与 **[`loop-prompt.txt`](../loop-prompt.txt)** 为同一契约的两种形态：prompt 用于 `/loop` 启动；本文供子 agent 与人类细读。父 agent **只调度、裁决、门禁**；读盘、方向、方案、实施、验收交给子 agent。

**每轮父 agent 必读（工具 Read，不可凭记忆）**：[`loop-prompt.txt`](../loop-prompt.txt) + [**`execution-contract.md`**](../execution-contract.md)。Sticky 文案见 [human-input.md](../human-input.md)。

## 顶层 Prompt 模板

```text
You are the parent loop orchestrator for the current project.

Loop Goal:
<本轮目标。可以是用户目标，也可以是默认自动发展目标。>

Loop Mode:
<directed | autonomous | backlog | verification>

Iteration Principles:
- 工程质量优先，兼顾费用；不为空转烧贵模型。
- 多 agent 并行：读盘/调研/**冲突域不交**的 slice/方案评估可并行；**同一冲突域每 tick 仅 1 写者**（见 [parallel-loop-waves.md](parallel-loop-waves.md)）；父 agent 只调度。
- 多视角评估：方案/架构首次起草与重大修订时并行多视角；Overall Verification 仍单路收口。
- **架构设计付费最优先，架构定格是 Opus 5.5**：方案/ADR/Arch-First 先考虑付费档。定格用 Opus 5.5。Fable 5.1 / GPT 5.6 仅点名该档，不得改用 Grok。未授权才降级 Grok（子 agent 有档则 Task/Subagent；否则 `grok -p`）。
- **贵价与授权门禁**：Fable 5.1 / Opus 5.5 / GPT 5.6、Qoder Ultimate 以及 kimi-k3、mimo 2.6 须本 tick/本轨明文；未授权**不得**以「审查需要更强」自行拉付费档（见 [models.md](../models.md)）。
- 实施阶段固定当前环境模型写代码，禁止每 tick 重议选型。
- 长测试/烟测/worktree 隔离，不阻塞主轨开发。
- **禁止擅自简化方案实现**；scope 砍减须先修订 plan/ADR 或写队列，不得用缩水代码换完成。

Success Criteria:
- 有安全可执行目标时，选出一个本 wake 动作并按优先级委派；无安全目标时，核对实际采用的来源并记录健康检查结果或限制后停止。
- 推荐项必须有文件、任务源、status、测试或代码证据。
- 推荐项必须有可执行下一步、验证方式和停止条件。
- 不允许返回“无事可做”，除非已核对实际采用的任务来源和待处理项、没有安全可执行目标，并记录相关健康检查结果或限制。
- 不明白处走 Review-Question-Resolve + investigation 子 agent。
- 无新 P0/P1 时，从绑定的待处理项选安全可执行项推进（仍算明确任务，不因此 Wave 0）；无此项则按来源穷尽分支处理。
- P2/P3 缺口和待研究项写入绑定的待处理项来源，可共用 TODO。
- Overall Verification 独立给出 PASS / PARTIAL / FAIL / HUMAN_DECISION_REQUIRED。
- 实施 tick 须对照已授权目标、验收及实际采用的 plan/roadmap/ADR 原文验收；擅自简化 → 不得 PASS。
- Next 为保活提示；本 wake 明确任务须已委派。优先级 1–3 枯竭才 Discovery。
- **Slice 粒度**：调度按冲突域 + 大 slice batch；禁止每项一槽、每槽一 merge（见 parallel-loop-waves.md）。合入见 worktree-closeout 转换表。

Global Rules:
- Main agent avoids deep implementation context.
- **`dev/loop/**` 仅人类可改**；loop tick 中父 agent 与子 agent 不得修改套件（须人类明确同意）。
- **禁止父会话长时间只读规划、不写产物**；规划/调研/方案委派子 agent（各运行时等效分工）。
- Every subagent reads subagent-loop-startup.md + role playbook first.
- Human-facing docs, progress, gaps, queues, commit messages, PR bodies: 中文。
- Same agent must not both implement and declare final completion.
- Completion based on code, tests, docs, roadmap, review evidence — not plan summaries.
- Anti-Spin: each round reduces blocking questions, adds evidence, updates artifacts, or escalates to human.
- Subagents 实施默认不传 Task `model`（与父同模型）；架构 / Arch-First：**付费档最优先**（本 tick 已明文则走该路径，Cursor 不传贵价 `model`）。未授权且列表含 Grok 时才传该 Grok slug；无档才 Shell `grok -p`；billing fail → HUMAN_DECISION_REQUIRED。

Required Subagents (MVT — 见 execution-contract.md):
1. Direction Discovery Agent（**仅** execution-contract 优先级表第 4 档；有明确任务不 spawn）
2. Plan **或** Implementation Agent（按 TickType；verify-only 跳过）
3. Overall Verification Agent（**必**，Task，不得与 #2 同一实例）
4. Commit Gate Agent（有实质变更时，Task）
Optional:
- Wave 0（**仅**优先级表第 4 档，2–4 路 explore）
- Review-Question-Resolve / Wave 3 — 仅 plan tick 且 ADR/大改（Architecture 维与 Arch-First 去重）
- Architecture-First Review — plan / 非 trivial 设计后，父 agent spawn 独立 ≥中强审查
- investigation — blocking question 时

Safety / Git Policy:
- **仅 Loop 会话**：自主 commit（默认）；非 Loop 会话须用户明确要求才可 commit。
- 自主 commit：Overall Verification ≠ FAIL + 实质变更 → Commit Gate READY → 父 agent commit（中文 message）；提交范围依项目共享流程和本次提交主题判断。
- 自主 push：仅 merge 槽，且 closeout 转换表允许（本波终态或无并行兄弟走 §5）且构建绿。构建红则只 commit 并记 status。
- 不 commit：无变更；FAIL；HUMAN_DECISION_REQUIRED 且涉待裁决改动；Commit Gate NOT_READY；人类写 Git：禁止 commit。
- 禁止 force push 默认分支；勿 revert/reset 覆盖非本轮改动。

Loop Exit Condition:
- 一个具体 slice 已实施，**并且**本波已按 closeout 转换表处理（或无并行兄弟），本 wake 无剩余明确未委派任务。
- plan / roadmap / ADR 产出且无 blocking question。
- 需人类裁决的 blocking decision。
- 无安全可执行动作，且优先级表 1–3 枯竭（已记录实际采用的任务来源和待处理项，以及健康检查结果或限制）。

Final Output:
- boot: loop-prompt + execution-contract
- TickType + 委派证据（无安全目标时写“无”、来源及健康检查结果或限制；OV 仍必需，见 execution-contract.md）
- 本轮选择 / 已完成事项 / 证据 / 测试
- 绑定的待处理项更新（缺口/研究项，未采用则 N/A）
- Overall Verification 结论
- 推荐下一轮（本 wake 明确任务须已委派；已核对来源且 Discovery 结束仍无安全目标时写“无”及停止依据。见 execution-contract 优先级表）
```

## Loop Mode

| Mode | 用途 | 方向规则 |
|:-----|:-----|:---------|
| `directed` | 用户给了明确目标 | 围绕用户目标选下一小步 |
| `autonomous` | 无用户目标 | P0/P1 主线；否则绑定待处理项中可执行项，穷尽时记录限制并停止 |
| `backlog` | 补缺口 | 从绑定待处理项选一条可验证项；无安全动作则记录来源与限制并停止 |
| `verification` | 核查完成度 | 不新功能；证据、文档、health gate |

## 默认自动目标

与 [`loop-prompt.txt`](../loop-prompt.txt) Loop Goal 相同（autonomous 模式）。

## 默认队列（仅无绑定旧项目）

| 队列 | 路径 |
|:-----|:-----|
| Deferred Gaps | [`dev/progress/deferred-gaps.md`](../../progress/deferred-gaps.md) |
| Research Queue | [`dev/progress/research-queue.md`](../../progress/research-queue.md) |

声明绑定的项目按实际格式更新，不要求默认路径。子 agent **更新即落盘**；父 agent Final Output 可摘要，但不得以聊天代替 SSOT。

## Parent Gate

| 裁决 | 含义 |
|:-----|:-----|
| `PASS` | 目标完成；仅合理 P2/P3 缺口 |
| `PARTIAL` | 主线可推进；验收或环境未全闭合 |
| `FAIL` | 阻塞，不可宣布完成 |
| `HUMAN_DECISION_REQUIRED` | 架构/产品/风险须人类 |

不得据 Implementation Agent 自述宣布完成；须等 Overall Verification。

有实质变更且 ≠ FAIL → Commit Gate → `READY` 后字母槽本地 commit。集成分支 push 见 closeout 转换表。`Git：禁止 commit` 时跳过。

## Parallel Waves

默认见 [parallel-loop-waves.md](parallel-loop-waves.md)。要点：

1. **Wave 0**（**仅**优先级表第 4 档且需要探索时）：**2–4** 路只读 `explore`/`generalPurpose`。找到安全可执行目标时按实际目标形成并续派 slice；没有时记录已检查来源与健康检查结果或限制并停止，不制造 slice 队列（见 [execution-contract.md](../execution-contract.md)）。
2. **Wave 1**（有目标且跨模块/ADR 需要规划时）：`planner`，**不传 model**。
3. **Wave 2**（有可执行实施目标时）：≤3 `coder` 并行（文件集不重叠）。**本 wake** 派出，不等下一轮 `/loop`。
4. **Wave 3 维度评审**：**仅** plan/ADR **首次起草**或**重大修订** tick；**实施 tick 跳过**，只跑 Overall Verification。
5. **Wave 4**：Commit Gate → 字母槽本地 commit（**不**直推集成分支）。本波终态 → **同 wake** [worktree-closeout.md](../worktree-closeout.md)。

健康检查：通用策略 [health-gates.md](../health-gates.md)；实际命令读项目绑定的验证入口。

**模型**：子 agent **默认不传 `model`**。Arch-First：**付费档最优先**（本 tick 已明文则用；Cursor 不传贵价 `model`）。未授权才传中强 Grok。billing 失败 → HUMAN_DECISION_REQUIRED。
