---
title: "Loop 执行契约"
type: guide
status: accepted
phase: N/A
updated: 2026-08-06
summary: "Playbook 与执行桥接：Boot、MVT、carry-forward 轻量确认 vs 触发式全量 Direction Discovery、同 tick 立即执行、委派证据、tick 分型。"
---

# Loop 执行契约

> Playbook 目录很长，但**每轮父 agent 只须遵守本文 + [`parent-loop-orchestrator.md`](agent-playbooks/parent-loop-orchestrator.md)**。  
> 子 agent 读自己的角色 playbook；父 agent **不必**每轮通读全部 8 份。

## 问题

| 理论 | 常见偏离 |
|:-----|:---------|
| 父 agent 只调度 | 父会话亲自改 prod 代码 |
| 每轮 4+ 子 agent | 跳过 Overall Verification，聊天里宣布完成 |
| 按 playbook 完整实施 | 擅自简化 plan/roadmap/ADR，用 stub 顶替后勾 checkbox |
| 套件只读 | Loop tick 中修改 `dev/loop/**`（须人类同意） |
| Wave 0 四六路并行 | 每 tick 都跑或从不跑，无判断标准 |
| Discovery → 同 tick 执行 → 验收 | Discovery-only tick：只写 status/Next 后等下一轮 `/loop` wake |
| carry-forward 轻量确认 | 每 tick 全量 Discovery；或盲信 status/Next 不验证 |
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

## 方向决策：carry-forward vs 全量 Discovery

**默认**：上轮 Overall Verification 已留下具体 **Next Tick Hint**（或等价 `status.md` 条目）且仍有效时，父 agent 做 **轻量确认（carry-forward）**，**不必**每 tick spawn Direction Discovery。

**全量 Discovery（Task）** 在以下**任一**成立时 **必须**运行（本 tick 内给不出可执行项时须重跑，可并行 Wave 0）：

| 触发条件 |
|:---------|
| 上轮无具体 Next，或 Next 模糊 / 不可验证 |
| Next 指向的 roadmap slice **已闭合**，或 active roadmap **为空** |
| 上轮 Overall Verification = **FAIL** / **HUMAN_DECISION_REQUIRED**（且人类尚未在本 tick 给出新裁决） |
| 人类在本 tick 输入中**变更**了 Loop Goal / 方向范围 |
| 队列 / active roadmap / gate 冷却使原 TickType **不再合法**（如须从 `verify-only` 改 `implement`） |
| carry-forward 轻量确认**失败**（证据与 Next 矛盾、checkbox 不存在、依赖未满足） |
| 本 tick 内 Overall Verification 给不出具体「推荐下一轮」 |

### carry-forward 轻量确认（父 agent，非子 agent）

跳过全量 Discovery 时，父 agent **仍须**在同一 tick 内完成：

1. 读 `status.md` **最近 1–2 条** + Next 指向的 roadmap / plan / 文件路径；
2. 确认：slice **仍 open**、无新 blocking、TickType 仍合法、gate 冷却未强制改向；
3. 在 Final Output 写明 `direction-discovery: skipped-carry-forward` + **沿用理由**（引用路径）；
4. 将上轮 Next **当作**本 tick 的 `Recommended Next Loop`，**同 tick 立即**继续 MVT（执行 → 验收）。

**禁止**：不读盘就沿用 Next（盲信 carry-forward）；或仅以「上轮已论证过」为由跳过验证。

## 调度与执行的关系（澄清 · 防误解）

- **父 agent（调度者）负责分发**：本 tick 动作的落地**必须**通过 spawn 子 agent 执行；「只调度」≠「旁观」——父 agent 在 MVT 步骤中**必须调用 Task/Agent 工具实际 spawn** 对应子 agent（Direction Discovery / Plan Roadmap / Implementation / Overall Verification / Commit Gate），不得把推荐写入 status 后结束等待下一轮。
- **「只调度」的准确含义**：不亲自改 prod 源码、不亲自实现、不亲自跑实施类 gate；但**必须亲自分发任务（spawn 子 agent）**。
- **模型价格不改变调度职责**：即使调度者为贵价模型（如 grok-4.5 / GPT-5.5 等），仍须且可以直接 spawn 子 agent 做实现；价格只影响「父 agent 亲自写代码」的成本取舍，不影响「调度者必须分发」的硬约束。

## 最小可行路径（MVT）

### 父 agent 每轮必做

0. **Boot（强制）** — 工具 **Read** `dev/loop/loop-prompt.txt` 与本文（`execution-contract.md`），**不可凭记忆**；Final Output 须含 `boot: loop-prompt + execution-contract`  
1. 读人类模型/方向（见 [human-input.md](human-input.md)）+ `status.md` 最近 3 条 tick + 两队列 +（若有）active roadmap（status/Next 当**假设**，须验证）  
2. **方向决策** — 若满足上文 **carry-forward** 条件 → 父 agent 轻量确认并记下 `TickType` + 本 tick 动作；否则 **Task** spawn **Direction Discovery**（只读）；无推荐 → **本 tick 内**重分析（可 Wave 0），禁止心跳式结束  
3. **同 tick 立即执行（硬）** — 无论 carry-forward 或全量 Discovery，确定 `Recommended Next Loop` + `TickType` 后，**不得**仅写入 `status.md` 或 Final Output 后结束 session 等待下一轮 `/loop` wake；须在本步骤继续 MVT  
4. 若本轮发现新的问题点且仓库中**没有对应方案文档 / ADR / active roadmap**，先切 `plan` 或先补 plan 产物，再进入实现  
5. 按 `TickType` spawn **一个**执行子 agent（见下表）  
6. **Task** spawn **Overall Verification**（只读裁决，不得与实施同一 Task）  
7. 有实质变更 → **Task** spawn **Commit Gate** → 父 agent commit  
8. 更新 `status.md` + 两队列（若变）；Final Output 的「推荐下一轮」= **下一 tick 提示**（Next Tick Hint），与 Direction Discovery 的「本 tick 动作」区分  

### 按 TickType 的执行子 agent

| TickType | 必 spawn | 可选 |
|:---------|:---------|:-----|
| `implement` | Implementation Agent | Wave 0（active 空或重分析时） |
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

| 条件 | Wave 0 |
|:-----|:-------|
| `dev/roadmap/active/` 为空 | **必跑**（2–4 路 `explore`/`generalPurpose`，非 6 路全满） |
| Direction Discovery 给不出可执行推荐 | **必跑** |
| 有明确单一 roadmap checkbox | **跳过** |
| 常规 implement tick | **跳过** |

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
  - direction-discovery: yes | skipped-carry-forward | re-run — <原因或沿用路径>
  - <plan-roadmap | implementation>: yes/no
  - architecture-first-review: Approve | Approve with changes | Reject | skipped-trivial | n/a（implement 已有方案）
  - overall-verification: yes/no
  - commit-gate: yes/no（或 skip 原因）
Parent prod edits: none | <路径>（应为 none；非 none → Overall Verification 不得 PASS）
Wave 0: skipped | <N> agents — <原因>
```

Overall Verification **PASS** 条件之一：`boot` 已声明、`Parent prod edits: none` 且 `overall-verification: yes`；**`plan` tick** 另须 `architecture-first-review` 为 Approve（或合并后的 Approve with changes）或合法 `skipped-trivial`。

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
