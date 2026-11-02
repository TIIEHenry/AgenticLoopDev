---
title: "Direction Discovery Agent"
type: guide
status: active
phase: N/A
created: 2026-06-17
updated: 2026-11-02
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
Select a safe executable action under the parent Loop Goal from sources actually adopted by the project. If none exists, report checked sources, results and health-check results or limitations and stop.

Inputs:
First read:
- `dev/loop/agent-playbooks/subagent-loop-startup.md`
- `dev/loop/agent-playbooks/direction-discovery-agent.md`

Then inspect:
- `dev/loop/execution-contract.md`（TickType、MVT、gate 冷却）
- 项目绑定入口和实际采用的任务/待处理项来源
- 执行与协调记录（最近 3 条 tick、运行中槽位与波次，判恢复与冷却）
- 绑定的验证入口；未采用的旧来源不读、不建，无绑定旧项目沿用默认路径
- `dev/loop/health-gates.md`（何时跑 gate，通用）
- related plan/docs named by the parent prompt
- recent git status if provided by the parent

Constraints:
- Do not implement code.
- Do not update files.
- Return no action only after checking adopted sources and finding no safe executable target; report the sources, results and health-check results or limitations, including red or unavailable checks. Follow execution-contract.md.
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
<按实际候选列出价值 / 风险 / 验证方式；没有安全目标时写“无”及排除依据，不凑数。>

TickType:
<implement | plan | verify-only — 见 execution-contract.md；需要规划才 plan；任务源空不自动造计划，无安全动作时写“无”，记录已检查来源和限制后停止；verify-only 须证明满足 health-gates 门禁>

Recommended Next Loop:（= 本 tick 动作 · This Tick Action；非 Final Output 的「下一 tick 提示」）
<有安全可执行目标时写一个本 tick 动作，具体到文件、roadmap 项、测试或待研究问题；无目标时写已检查来源和限制，停止本 tick。>

Gate Cooldown Check:
<若建议跑 gate：引用 status 最近 tick，说明未命中冷却；若命中冷却，不得重复 gate 或 verify-only；有安全目标则按性质选 implement/plan，无安全目标则记录来源和健康检查结果或限制并停止>

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
2. 有安全可执行目标时，**同 session、同 tick** 按 `TickType` **调用 Task/Agent 工具实际 spawn** Plan Roadmap / Implementation 子 agent（或 `verify-only` 时父 agent 跑 gate）——「已输出推荐但未 spawn」即 Discovery-only tick（禁止）；
3. 继续 Overall Verification → Commit Gate（若有变更）→ 更新 `status.md`；
4. **仅在此之后**才结束本 tick / arm 下一次 `/loop` wake。

**禁止**：

- Discovery-only tick：只做方向发现、把推荐写入 `status.md` 或 Final Output 后结束，等下一轮 `/loop` 再执行；
- 把 `Recommended Next Loop` 误当作 Final Output 末尾的「推荐下一轮」（下一 tick 提示）——后者由 Overall Verification 收尾产出，供**下一 tick Boot** 参考。

任务来源穷尽且无安全动作也可停止；合法例外见 [execution-contract.md](../execution-contract.md)：`HUMAN_DECISION_REQUIRED`、gate 冷却、资源硬约束（adb / worktree 槽位满）——须在本 tick 书面记录原因，**不得**用「下轮再说」代替。

## Selection Policy

按以下顺序选择方向：

1. 用户明确目标中仍未完成的 P0/P1。
2. active roadmap 中阻塞或半完成的 P0/P1。
3. 来源为空时调查是否有已授权且明确的普通工作，可直接 `implement`；重要风险、跨模块协调、交接或未定设计才 `plan`。没有安全可执行目标时记录穷尽证据并停止。
4. 已实现但缺少独立验证、手测、文档门禁的主线项（**非**连续 gate — 见 health-gates 冷却）。
5. Research Queue 中高价值、可在一轮内形成方案或结论的项目。
6. Deferred Gaps 中具体、可验证、低风险的缺口。
7. docs health、TODO / P2 扫描、roadmap/status 一致性 — **不得**单独作为「再跑一遍全量 gate」的理由，除非冷却表允许 `verify-only`。

### Gate 冷却（硬）

读 status 最近条目：

- 同一**聚焦 gate**（相同域/`--tests` 模式）已连续 **2 tick 绿** 且其间无该域 prod 变更 → **禁止**再推荐该 gate；有安全目标时改 `implement` / `plan`，否则记录来源和健康检查结果或限制并停止。
- **Grand gate** 距上次全绿 **< 8 tick** 且无大 slice 闭合 → **禁止** grand。
- 上一轮已是 `verify-only` → 本轮 **禁止**再 `verify-only`。

## Anti-Idle Rule

禁止返回“继续观察”“保持现状”“再读文档”作为推荐动作。有安全目标时推荐动作必须包含以下内容；来源已核对且无安全目标时允许写“无”，并记录来源、结果和健康检查限制：

- 一个具体目标。
- 一个最小文件集合。
- 一个验证方式。
- 一个停止条件。

## 无下一轮时

给不出具体下一步时，调度者先走 [execution-contract.md](../execution-contract.md) 优先级 1–3（本波槽位 / 任务源 / 队列）。**仅枯竭**才启动本 agent 或 Wave 0。禁止有明确任务却「重分析方向」。

有安全目标时禁止用「暂无」「待定」「下轮再说」代替本 wake 委派；无安全目标时按上述证据停止。
