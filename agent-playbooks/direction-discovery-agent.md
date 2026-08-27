---
title: "Direction Discovery Agent"
type: guide
status: active
phase: N/A
created: 2026-06-17
updated: 2026-08-27
summary: "方向发现：仅任务源优先级第 4 档才跑；有明确任务父不得 spawn；本 wake 立即委派执行。"
---

# Direction Discovery Agent

Direction Discovery Agent 的任务不是泛泛总结文档，而是回答：**现在最值得推进哪一个具体下一步，为什么不是别的。**

## 何时运行本 agent

父 agent **默认不 spawn** 本 agent。谓词 SSOT：[execution-contract.md § 方向决策](../execution-contract.md#方向决策任务源优先级ssot) **第 4 档**。

有明确任务（本波未终态、任务源 open 项、有效 Next、队列中已具体可执行项）→ 父 **不得** spawn 本 agent，也 **不得** Wave 0。

carry-forward 轻量确认仍由父 agent 做（读 status + 任务源路径），不算整体重分析。

## Prompt 模板

```text
Role:
You are the Direction Discovery Agent for the current project.

Goal:
Determine the single best next loop for the project under the parent Loop Goal. If there is no new high-value P0/P1 direction, select one concrete item from Research Queue or Deferred Gaps.

Inputs:
First read:
- `dev/loop/agent-playbooks/subagent-loop-startup.md`
- `dev/loop/agent-playbooks/direction-discovery-agent.md`

Then inspect:
- `dev/loop/execution-contract.md`（TickType、MVT、gate 冷却）
- `dev/progress/status.md`（**最近 3 条 tick**，判 gate 是否处于冷却）
- `dev/progress/deferred-gaps.md`（Deferred Gaps SSOT）
- `dev/progress/research-queue.md`（Research Queue SSOT）
- active roadmaps in `dev/roadmap/active/`
- active parallel boards in `dev/parallel/active/`
- `dev/progress/health-gates.md`（本仓库测试 gate 命令）
- `dev/loop/health-gates.md`（何时跑 gate，通用）
- related plan/docs named by the parent prompt
- recent git status if provided by the parent

Constraints:
- Do not implement code.
- Do not update files.
- Do not return “nothing to do” unless active tasks, Research Queue, Deferred Gaps, and relevant health checks are empty or passing.
- Ground recommendations in specific files, roadmap entries, docs, tests, or code paths.
- Prefer unfinished P0/P1 work over P2/P3 gaps.
- Human-facing output must be written in Chinese.

Output:
Return only the required output format.
```

## Output Format

```text
Current State:
<当前主线、已完成但未验收项、明显阻塞项。>

Evidence:
- <路径或 roadmap/status/doc 证据>

Candidate Directions:
1. <候选方向> — <价值 / 风险 / 验证方式>
2. <候选方向> — <价值 / 风险 / 验证方式>
3. <候选方向> — <价值 / 风险 / 验证方式>

TickType:
<implement | plan | verify-only — 见 execution-contract.md；任务源枯竭时必须 plan；verify-only 须证明满足 health-gates 门禁>

Recommended Next Loop:（= 本 tick 动作 · This Tick Action；非 Final Output 的「下一 tick 提示」）
<exactly one 本 tick 须立即委派执行的动作，必须具体到文件、roadmap 项、测试或待研究问题。父 agent 收到后须同 session、同 tick 按 TickType spawn 执行子 agent，不得仅写入 status 后结束 session 等待下一轮 /loop wake。>

Gate Cooldown Check:
<若建议跑 gate：引用 status 最近 tick，说明未命中冷却；若命中冷却，不得 verify-only，须改 implement/plan>

Why Not Others:
- <未选择候选项的原因>

Research Queue Updates:
- <新增、保留或关闭的待研究项；没有则写“无”。>

Deferred Gap Candidate:
- <如果没有新方向，推荐修补的一个 Deferred Gap；没有则写“无”。>

Stop Conditions:
- <本推荐动作何时可以停止。>

Files To Read Next:
- <本 tick 执行子 agent（Plan / Implementation）应读取的最小文件集合。>
```

## 同 tick 立即执行（硬）

Direction Discovery **不是**独立 tick 的终点，而是本 tick MVT 的**开工决策**。

父 agent 收到本 agent 输出后 **必须**：

1. 读取 `TickType` 与 `Recommended Next Loop`（本 tick 动作）；
2. **同 session、同 tick** 按 `TickType` **调用 Task/Agent 工具实际 spawn** Plan Roadmap / Implementation 子 agent（或 `verify-only` 时父 agent 跑 gate）——「已输出推荐但未 spawn」即 Discovery-only tick（禁止）；
3. 继续 Overall Verification → Commit Gate（若有变更）→ 更新 `status.md`；
4. **仅在此之后**才结束本 tick / arm 下一次 `/loop` wake。

**禁止**：

- Discovery-only tick：只做方向发现、把推荐写入 `status.md` 或 Final Output 后结束，等下一轮 `/loop` 再执行；
- 把 `Recommended Next Loop` 误当作 Final Output 末尾的「推荐下一轮」（下一 tick 提示）——后者由 Overall Verification 收尾产出，供**下一 tick Boot** 参考。

合法例外见 [execution-contract.md](../execution-contract.md)：`HUMAN_DECISION_REQUIRED`、gate 冷却、资源硬约束（adb / worktree 槽位满）——须在本 tick 书面记录原因，**不得**用「下轮再说」代替。

## Selection Policy

按以下顺序选择方向：

1. 用户明确目标中仍未完成的 P0/P1。
2. active roadmap 中阻塞或半完成的 P0/P1。
3. **`dev/roadmap/active/` 为空** 且队列无单轮可实施项 → **TickType = `plan`**，推荐 Plan Roadmap Agent 主题（从 Research Queue、status「下一主轨」、Wave 0 证据选一项）。
4. 已实现但缺少独立验证、手测、文档门禁的主线项（**非**连续 gate — 见 health-gates 冷却）。
5. Research Queue 中高价值、可在一轮内形成方案或结论的项目。
6. Deferred Gaps 中具体、可验证、低风险的缺口。
7. docs health、TODO / P2 扫描、roadmap/status 一致性 — **不得**单独作为「再跑一遍全量 gate」的理由，除非冷却表允许 `verify-only`。

### Gate 冷却（硬）

读 status 最近条目：

- 同一**聚焦 gate**（相同域/`--tests` 模式）已连续 **2 tick 绿** 且其间无该域 prod 变更 → **禁止**再推荐该 gate；改 `implement` / `plan`。
- **Grand gate** 距上次全绿 **< 8 tick** 且无大 slice 闭合 → **禁止** grand。
- 上一轮已是 `verify-only` → 本轮 **禁止**再 `verify-only`。

## Anti-Idle Rule

禁止返回“继续观察”“保持现状”“再读文档”作为推荐动作。推荐动作必须包含：

- 一个具体目标。
- 一个最小文件集合。
- 一个验证方式。
- 一个停止条件。

## 无下一轮时

给不出具体下一步时，调度者先走 [execution-contract.md](../execution-contract.md) 优先级 1–3（本波槽位 / 任务源 / 队列）。**仅枯竭**才启动本 agent 或 Wave 0。禁止有明确任务却「重分析方向」。

禁止用「暂无」「待定」「下轮再说」代替本 wake 委派。
