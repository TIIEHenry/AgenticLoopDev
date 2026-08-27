---
title: "Loop 执行契约"
type: guide
status: accepted
phase: N/A
updated: 2026-08-27
summary: "Boot、MVT、任务源优先级、本 wake 续派、委派证据；Wave 0 仅无明确任务；合入时机见 worktree-closeout。"
---

# Loop 执行契约

> Playbook 目录很长，但**每轮父 agent 只须遵守本文 + [`parent-loop-orchestrator.md`](agent-playbooks/parent-loop-orchestrator.md)**。  
> 子 agent 读自己的角色 playbook；父 agent **不必**每轮通读全部 8 份。  
> **套件不绑定消费仓库的任务内容。** Loop 只问「有没有明确可执行工作」。条目写在消费仓库的任务源（约定相对路径：`dev/progress/`、`dev/roadmap/active/` 等，见 [porting.md](porting.md)）。套件内禁止写某仓库名、模块名、业务主题。  
> **`/loop` 只保活**：定时唤醒不是调度量子。本 wake（含后台子 agent 回报后的续轮）须继续委派，直到本文停止条件；禁止把已明确的工作停成 Next、等下一轮 `/loop`。  
> 合入 `main` 的**何时** → [worktree-closeout.md](worktree-closeout.md) 转换表；本文不复制。

## 问题

| 理论 | 常见偏离 |
|:-----|:---------|
| 父 agent 只调度 | 父会话亲自改 prod 代码 |
| 每轮 4+ 子 agent | 跳过 Overall Verification，聊天里宣布完成 |
| 按 playbook 完整实施 | 擅自简化 plan/roadmap/ADR，用 stub 顶替后勾 checkbox |
| 套件只读 | Loop tick 中修改 `dev/loop/**`（须人类同意） |
| Wave 0 四六路并行 | 每 tick 都跑或从不跑，无判断标准 |
| Discovery → 同 wake 执行 → 验收 | 只写 status/Next 后等下一轮 `/loop` wake |
| 有明确任务则实施 | 每 tick 全量 Discovery / Wave 0；或盲信 status/Next |
| 8 份 playbook 必读 | token 浪费在重复读全文 |

**做法**：按 **tick 类型**走 **最小可行路径（MVT）**，Final Output 带 **委派证据**；Overall Verification 对照本文裁决是否合规。

## Tick 类型

Direction Discovery **必须**为本轮标注 `TickType`（写入 `Recommended Next Loop`，即**本 tick 动作**，非 Final Output 的下一 tick 提示）：

| TickType | 何时 | 禁止 |
|:---------|:-----|:-----|
| `implement` | active roadmap 有可勾选 slice；或队列项可在单轮内落地代码/测试 | 仅跑 gate、父 agent 写 prod |
| `plan` | `dev/roadmap/active/` **为空**；或 Research Queue 项须先产出 plan/roadmap/ADR；或大架构未定 | 直接改 prod（除文档） |
| `verify-only` | **受限** — 见 [health-gates.md](health-gates.md#verify-only-tick-门禁) | 连续两轮 verify-only；无 delta 重复同一 gate |

**任务源枯竭**（active 空 + 队列无单轮可实施项）→ 本轮 **必须** `plan`，调度 Plan Roadmap Agent 产出 `dev/plans/` + `dev/roadmap/active/phase-*.md`（或闭合 Research Queue 一项）。

## 方向决策：任务源优先级（SSOT）

消费仓库的任务源 = 其 `dev/progress/`（status / 两队列）+ `dev/roadmap/active/`（或项目约定的等价 phase 文档）+ parallel board。Loop **不**解释某仓库的业务主题。

**明确任务** = 本波未终态 slice ∪ 任务源中仍 open 的可执行项 ∪ 轻量确认仍有效的 Next ∪ 两队列中已具体、可单轮推进的一项。  
**没有明确任务** = 上列全部空或失效（AND）。实施 FAIL 但该项仍 open → 仍是明确任务（继续修同一项），**禁止**用 OV=FAIL 短路进 Wave 0。

spawn 全量 Direction Discovery / Wave 0 **之前**按序检查，**命中即本 wake 动作**，不得整体重分析：

| # | 若成立 | 本 wake 做什么 |
|:--|:-------|:---------------|
| 1 | 字母槽非 `idle`：有 `occupied` | 继续该 slice 实施（再 spawn Implementation）。不得 Discovery |
| 1b | 无 `occupied`，冻结本波均为 `merge-queued` 或书面 `blocked` | **同 wake** 跑 [worktree-closeout.md](worktree-closeout.md)。不 spawn Implementation / Discovery |
| 2 | 任务源仍有 open 可执行项，或 Next 轻量确认有效 | 按 TickType spawn Plan / Implementation |
| 3 | 两队列中已有具体、可单轮推进的一项 | `implement` 或 `plan`（按该项性质） |
| 4 | **仅当 1–3 均枯竭**，或 carry-forward **验证失败**，或**人类本 tick 改方向** | 才全量 Discovery；Wave 0 **仅此路径**（及人类明示） |

**默认 carry-forward**：上轮具体 Next（或等价 status 条目）仍有效 → 父 agent 轻量确认，**不** spawn Discovery。轻量确认须：读 status 最近 1–2 条 + Next 指向的任务源路径；slice 仍 open、无新 blocking、TickType 合法。Final Output 写 `direction-discovery: skipped-carry-forward` + 沿用路径。

**禁止**：不读盘盲信 Next；有明确任务仍 Wave 0 / 全量 Discovery；把已明确工作写成 Next 后结束、等下一轮 `/loop`。

## 调度与执行的关系（澄清 · 防误解）

- **父 agent（调度者）负责分发**：本 wake 动作的落地**必须**通过 spawn 子 agent 执行；「只调度」≠「旁观」——**必须调用 Task/Agent 工具实际 spawn**（Plan / Implementation / Overall Verification / Commit Gate；Discovery **仅**优先级表第 4 档）。不得把推荐写入 status 后结束、等待下一轮 `/loop`。后台子 agent 回报后，**同一会话**继续 MVT。
- **「只调度」的准确含义**：不亲自改 prod 源码、不亲自实现、不亲自跑实施类 gate；但**必须亲自分发任务（spawn 子 agent）**。
- **模型价格不改变调度职责**：即使调度者为贵价模型（如 grok-4.5 / GPT-5.5 等），仍须且可以直接 spawn 子 agent 做实现；价格只影响「父 agent 亲自写代码」的成本取舍，不影响「调度者必须分发」的硬约束。

## 最小可行路径（MVT）

### 父 agent 每轮必做

0. **Boot（强制）** — 工具 **Read** `dev/loop/loop-prompt.txt` 与本文（`execution-contract.md`），**不可凭记忆**；Final Output 须含 `boot: loop-prompt + execution-contract`  
1. 读人类模型/方向（见 [human-input.md](human-input.md)）+ `status.md` 最近 3 条 tick + 两队列 +（若有）active roadmap（status/Next 当**假设**，须验证）  
2. **方向决策** — 按上文 **任务源优先级表**；仅第 4 档才 Task spawn Direction Discovery。禁止有明确任务仍整体重分析。  
3. **本 wake 续派（硬）** — 确定动作后**不得**只写 status/Final Output 后结束、等下一轮 `/loop`。后台回报后同一会话继续：再 spawn、OV、或本波终态则 **同 wake closeout**。  
4. 若本轮发现新的问题点且消费仓库**没有对应方案 / ADR / active 任务源条目**，先切 `plan` 或先补 plan 产物，再进入实现  
5. 按 `TickType` spawn 执行子 agent；本波终态且有 `merge-queued` → **不**再 spawn Implementation / Discovery，跑 closeout  
6. **Task** spawn **Overall Verification**（只读裁决，不得与实施同一 Task）  
7. 有实质变更 → **Task** spawn **Commit Gate** → 父 agent **字母槽本地 commit**（不推默认分支）。合入默认分支 / push 仅 merge 槽，且须 closeout 转换表允许  
8. 更新消费仓库行动层（status / 两队列 / 任务源勾选，若变）。Final Output「推荐下一轮」仅用于**会话已结束后的保活重入**；本会话仍有明确任务时必须已在本 wake 委派，不得把委派本身写成 Next  

### 按 TickType 的执行子 agent

| TickType | 必 spawn | 可选 |
|:---------|:---------|:-----|
| `implement` | Implementation Agent | Wave 0 **仅**优先级表第 4 档 |
| `plan` | Plan Roadmap Agent → 父 agent spawn **Arch-First Review**（≥中强，见 [architecture-first-design.md](agent-playbooks/architecture-first-design.md)） | Wave 0；Wave 3 Testing/Security（Architecture 维与 Arch-First 去重） |
| `verify-only` | （无实施 agent） | 父 agent 仅跑 gate + 记 status |

### 问题点文档化门禁

当 loop 在实现、验收、真机反馈或用户反馈中发现**新的问题点**（尤其 UI/UX、显示、交互、行为异常）时，父 agent 需先检查仓库是否已有对应的：

- `docs/architecture/` 方案文档
- `docs/decisions/` ADR
- `dev/roadmap/active/` 实施项
- `dev/plans/` 计划文档

若以上都没有，**不得**把该问题仅记在聊天中或直接做 ad-hoc 修补；必须：

1. 将本轮或下一轮 `TickType` 设为 `plan`，或在当前 implement tick 中先补 plan 产物；
2. 委派 Plan Roadmap Agent（必要时配合 architecture 评审）产出文档；
3. 将问题的后续实施建立为 roadmap / plan / ADR 的可追溯项。

例外：单行 typo、纯测试断言、无行为变化 trivial bugfix。

### Wave 0 — 何时跑

谓词见上文优先级表第 4 档。下表不得单独作为「必跑」：

| 条件 | Wave 0 |
|:-----|:-------|
| 优先级表 1–3 仍有明确任务 | **跳过**（`skipped-clear-task` 或 `skipped-carry-forward`） |
| 仅第 4 档（任务源枯竭 / carry-forward 验证失败 / 人类改方向） | **可跑**（2–4 路 `explore`/`generalPurpose`，非每 tick 满员） |
| 常规 implement（已有 slice 委派单） | **跳过**；仍须输出冲突域矩阵再派 Implementation |

### Slice 粒度（implement tick）

- 委派 Implementation 须附 [implementation-agent.md](agent-playbooks/implementation-agent.md) § Slice 委派单；**禁止**同一 `conflict_domain` 同 tick 多写者。
- 模板化同质工作须达到 [parallel-loop-waves.md](agent-playbooks/parallel-loop-waves.md) 默认批量。合入次数与**何时**合入见 [worktree-closeout.md](worktree-closeout.md)；Merge 预算 ≠ 中途单槽进默认分支。
- Final Output `Wave 0` 行：`skipped-clear-task` | `skipped-carry-forward` | `<N> — 第4档原因`。

### 本 wake 停止条件

仅当：本波已 closeout（或无并行波且本刀已按 closeout/§5 Guard 处理）且优先级表 1–3 无剩余明确任务；或书面 `blocked` / `HUMAN_DECISION_REQUIRED`；或第 4 档已跑完 Discovery/`plan` 且队列穷尽。**禁止**以「一个 slice 已实施」为默认出口而把其余委派留给下一轮 `/loop`。

### 父 agent 允许改的文件

| 允许 | 禁止 |
|:-----|:-----|
| `dev/progress/*`、勾选 roadmap、两队列 | **prod 源码**（`*.kt` `*.java` `*.ts` `*.tsx` 等各模块 `src/`） |
| 父 agent 合成用短摘要 | **`dev/loop/**`（套件 SSOT；**仅人类明确同意**后可改，且非 loop tick 自发） |
| | 测试实现、构建脚本（除非人类明确让父修 trivial 门禁） |

实施子 agent 改 prod；父 agent 若发现需改 prod，**停止并 spawn Implementation Agent**，不得自己动手。

## 委派证据（Final Output 必填）

```text
boot: loop-prompt + execution-contract
TickType: implement | plan | verify-only
Subagents spawned:
  - direction-discovery: yes | skipped-carry-forward | skipped-clear-task | re-run — <第4档原因或沿用路径>
  - <plan-roadmap | implementation>: yes/no
  - architecture-first-review: Approve | Approve with changes | Reject | skipped-trivial | n/a（implement 已有方案）
  - overall-verification: yes/no
  - commit-gate: yes/no（或 skip 原因）
Parent prod edits: none | <路径>（应为 none；非 none → Overall Verification 不得 PASS）
Wave 0: skipped-clear-task | skipped-carry-forward | <N> — <第4档原因>
slots: <各字母槽 idle|occupied|merge-queued|blocked>
wave-members: <本波 Wave 2 冻结集合；无并行则 none>
merge-to-main: yes | no
```

Overall Verification **PASS** 条件之一：`boot` 已声明、`Parent prod edits: none` 且 `overall-verification: yes`；**`plan` tick** 另须 `architecture-first-review` 为 Approve（或合并后的 Approve with changes）或合法 `skipped-trivial`。缺 `slots` / `wave-members` 却宣称合入或跳过 Wave 0 → 不得 PASS。

## 与完整 Playbook 的关系

| 文档 | 谁读 |
|:-----|:-----|
| 本文 + `parent-loop-orchestrator.md` | **父 agent 每轮** |
| `subagent-loop-startup.md` + 角色 playbook | **对应子 agent** |
| `architecture-first-design.md` | plan / 非 trivial 设计门禁与审查者 |
| `review-question-resolve-loop.md` | blocking question 未收敛时 |

`loop-prompt.txt` 列出的 8 份 playbook = **子 agent 角色库**，不是父 agent 每轮必读清单。

## 相关

- [health-gates.md](health-gates.md) — gate 频率与 verify-only 门禁  
- [workflow.md](workflow.md) — tick 顺序  
- [direction-discovery-agent.md](agent-playbooks/direction-discovery-agent.md) — 产出 TickType  
