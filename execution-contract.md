---
title: "Loop 执行契约"
type: guide
status: accepted
phase: N/A
updated: 2026-07-28
summary: "Playbook 与执行桥接：每 tick Boot 重读契约、MVT、父边界、委派证据、tick 分型。"
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
| 8 份 playbook 必读 | token 浪费在重复读全文 |

**做法**：按 **tick 类型**走 **最小可行路径（MVT）**，Final Output 带 **委派证据**；Overall Verification 对照本文裁决是否合规。

## Tick 类型

Direction Discovery **必须**为本轮标注 `TickType`（写入 Recommended Next Loop）：

| TickType | 何时 | 禁止 |
|:---------|:-----|:-----|
| `implement` | active roadmap 有可勾选 slice；或队列项可在单轮内落地代码/测试 | 仅跑 gate、父 agent 写 prod |
| `plan` | `dev/roadmap/active/` **为空**；或 Research Queue 项须先产出 plan/roadmap/ADR；或大架构未定 | 直接改 prod（除文档） |
| `verify-only` | **受限** — 见 [health-gates.md](health-gates.md#verify-only-tick-门禁) | 连续两轮 verify-only；无 delta 重复同一 gate |

**任务源枯竭**（active 空 + 队列无单轮可实施项）→ 本轮 **必须** `plan`，调度 Plan Roadmap Agent 产出 `dev/plans/` + `dev/roadmap/active/phase-*.md`（或闭合 Research Queue 一项）。

## 最小可行路径（MVT）

### 父 agent 每轮必做

0. **Boot（强制）** — 工具 **Read** `dev/loop/loop-prompt.txt` 与本文（`execution-contract.md`），**不可凭记忆**；Final Output 须含 `boot: loop-prompt + execution-contract`  
1. 读人类模型/方向（见 [human-input.md](human-input.md)）+ `status.md` 最近 3 条 tick + 两队列 +（若有）active roadmap（status/Next 当**假设**，须验证）  
2. **Task** spawn **Direction Discovery**（只读，不改文件）；无推荐 → **调度者立即启动**重分析（可 Wave 0），禁止心跳式结束  
3. 若本轮发现新的问题点且仓库中**没有对应方案文档 / ADR / active roadmap**，先切 `plan` 或先补 plan 产物，再进入实现  
4. 按 `TickType` spawn **一个**执行子 agent（见下表）  
5. **Task** spawn **Overall Verification**（只读裁决，不得与实施同一 Task）  
6. 有实质变更 → **Task** spawn **Commit Gate** → 父 agent commit  
7. 更新 `status.md` + 两队列（若变）  

### 按 TickType 的执行子 agent

| TickType | 必 spawn | 可选 |
|:---------|:---------|:-----|
| `implement` | Implementation Agent | Wave 0（active 空或重分析时） |
| `plan` | Plan Roadmap Agent | Wave 0；Wave 3（首次 ADR/大改） |
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
  - direction-discovery: yes/no
  - <plan-roadmap | implementation>: yes/no
  - overall-verification: yes/no
  - commit-gate: yes/no（或 skip 原因）
Parent prod edits: none | <路径>（应为 none；非 none → Overall Verification 不得 PASS）
Wave 0: skipped | <N> agents — <原因>
```

Overall Verification **PASS** 条件之一：`boot` 已声明、`Parent prod edits: none` 且 `overall-verification: yes`。

## 与完整 Playbook 的关系

| 文档 | 谁读 |
|:-----|:-----|
| 本文 + `parent-loop-orchestrator.md` | **父 agent 每轮** |
| `subagent-loop-startup.md` + 角色 playbook | **对应子 agent** |
| `parallel-loop-waves.md` | 父 agent 开 Wave 0/2/3 前 |
| `review-question-resolve-loop.md` | blocking question 未收敛时 |

`loop-prompt.txt` 列出的 8 份 playbook = **子 agent 角色库**，不是父 agent 每轮必读清单。

## 相关

- [health-gates.md](health-gates.md) — gate 频率与 verify-only 门禁  
- [workflow.md](workflow.md) — tick 顺序  
- [direction-discovery-agent.md](agent-playbooks/direction-discovery-agent.md) — 产出 TickType  
