---
title: "开发 Loop 单轮工作流"
type: guide
status: accepted
phase: N/A
updated: 2026-08-10
summary: "单轮 tick：Boot 强制重读契约；carry-forward 轻量确认或触发式全量 Discovery；merge 两边保留；步骤、验收与退出。"
---

# 单轮 Tick 工作流

> 平台无关。原则见 [overview.md § 迭代原则](overview.md#迭代原则)。**MVT 与 TickType**见 [execution-contract.md](execution-contract.md)。各运行时如何「触发」一轮见 [runtimes/](runtimes/INDEX.md)。

## 每轮必做（顺序）

0. **Boot（强制）** — **工具 Read**（不可凭记忆）[`loop-prompt.txt`](loop-prompt.txt) 与本文档链接的 [`execution-contract.md`](execution-contract.md)；Final Output 写 `boot: loop-prompt + execution-contract`。见 [human-input.md § Sticky](human-input.md#sticky-调度不变量推荐全运行时)。  
0b. **读人类输入** — **当前模型**（slug + 运行时）+ **大致方向** → [human-input.md](human-input.md)  
   - Claude Code / OpenCode：人类未写时，读会话配置后**声明**；OpenCode 有 **`-m`** 则直接复述该值  
   - 每轮开头或结尾**可见复述**当前模型，禁止只说「Claude Code 默认」  
1. **读进度** — `dev/progress/status.md` →「Next」与最新 session（**当假设**，须用代码/队列验证，勿盲信「已完成」）  
2. **读队列 SSOT** — [`deferred-gaps.md`](../progress/deferred-gaps.md) · [`research-queue.md`](../progress/research-queue.md)  
3. **读任务源** — 活跃 `dev/roadmap/active/`（或项目约定的 phase 文档）  
4. **自主选任务** — **默认** carry-forward：验证上轮具体 Next 仍有效 → 记下 **TickType** + 本 tick 动作；**否则** Direction Discovery（Task）全量发现。无论哪条路径，**同 tick 立即**按 TickType 委派 Plan/Implementation（禁止 Discovery-only tick）；无主线且 active 空 → **`plan`** tick；给不出推荐 → **本 tick 内重跑** Discovery（可并行 Wave 0），**禁止**当心跳结束（详见 [execution-contract.md § 方向决策](execution-contract.md#方向决策carry-forward-vs-全量-discovery)）  
5. **执行** — 按 [execution-contract.md](execution-contract.md) MVT 委派 Plan / Implementation；父 agent **不改 prod**  
6. **验证** — 遵守 [health-gates.md](health-gates.md) 冷却；有变更跑聚焦 gate；grand 受 8-tick 间隔约束  
7. **更新行动层** — 勾选 roadmap、更新 `status.md`；**缺口/研究项改表**（两队列 SSOT）；[规则 3a](../../docs/DOCUMENTATION.md#规则-3a提交前文档门禁commit-前必做)  
8. **Git（自主 commit，仅 Loop 会话）** — Overall Verification ≠ FAIL 且有实质变更 → Commit Gate `READY` → **父 agent 必须 commit**（不等用户说「请 commit」）；build/check 绿且不阻塞主轨时 **push**。仅 `Git：禁止 commit` 或门禁未通过时可跳过 → [loop-prompt.txt](loop-prompt.txt) Safety / Git Policy。**非 Loop 会话**须用户明确要求才可 commit。

## 自主 Loop 额外要求

使用 [`loop-prompt.txt`](loop-prompt.txt) 时：

- **方向决策** — 默认 carry-forward 轻量确认上轮 Next；不满足触发条件时 Direction Discovery 全量发现 → **exactly one** 本 tick 动作  
- 无 P0/P1 时从 [research-queue.md](../progress/research-queue.md) / [deferred-gaps.md](../progress/deferred-gaps.md) 选可验证项  
- **Overall Verification** 每轮必跑（PASS / PARTIAL / FAIL / HUMAN_DECISION_REQUIRED）— **单路收口**；**推荐下一轮**必填且具体可执行；若无 → **调度者立即启动 Direction Discovery 重分析**  
- **Wave 3 维度评审**仅用于 plan/ADR **首次起草或重大修订** tick；其中 Architecture 维与 [Arch-First](agent-playbooks/architecture-first-design.md) 去重；**实施 tick 只跑 Overall Verification**  
- **plan tick** 须完成 Architecture-First（≥中强独立审查）或合法 trivial skip，见 execution-contract  

- Implementation Agent **不得**自行宣布最终完成  
- **不得擅自简化方案实现** — 以 plan/roadmap/ADR 原文为 scope；缩水、未登记的 stub、静默砍步骤 → 不得勾 checkbox / 不得 PASS  
- 新 gap / 研究项 **必须**写入两队列 SSOT，不可只写在 tick 输出里  

## 退出条件（本轮停止）

- 一个 slice 实施并通过总体验收  
- plan / roadmap / ADR 草案产出且无 blocking question  
- 发现需人类裁决的 blocking decision  
- 无安全可执行动作，且队列/缺口已记录  

## 禁止

- **空转** — 无 prod/文档变更且仅重复已冷却的 gate（见 health-gates）  
- **连续 verify-only** — 两轮仅跑测试无实施/plan  
- **父 agent 改 prod** — 须 spawn Implementation Agent（见 execution-contract）  
- **跳过 Overall Verification** — 聊天里宣布完成  
- **擅自简化实现** — 未改 plan/ADR 就砍 scope、用 stub 顶替契约、勾 checkbox 冒充完成  
- **擅自改 `dev/loop/`** — 套件内文件须经**人类明确同意**；loop tick 中 agent 不得改 playbook/契约  
- **merge 整文件选边 / 口号 keep both** — 同步或合入时禁止 `--ours`/`--theirs` 整文件、`-X ours/theirs`；须真三路合并并跑 `scripts/check-merge-both-sides.sh`（见 [worktrees.md §5.1](worktrees.md)）  
- **空转收尾** — 无具体「推荐下一轮」却不由调度者本 tick 内启动 Direction Discovery 重分析；或确定本 tick 动作后未同 tick 执行就结束 session（Discovery-only tick）  
- **盲信 carry-forward** — 不读 roadmap/plan 就沿用 status/Next  
- **跳过 Boot** — 未工具 Read `loop-prompt.txt` + `execution-contract.md` 凭记忆开干  
- **SwitchMode 进只读 Plan** — 父 agent 须留在可写/可委派模式（见 loop-prompt Subagent Policy）  
- **构建红时 push** — 相关 check 失败或会阻塞主轨编译时不 push  
- **并行抢资源** — 同一 adb 设备上多个烟测 agent；OpenCode 会话内禁止 `opencode run` 抢设备（见 [external-cli.md](external-cli.md)）  
- **实施阶段重议模型** — 写代码/fix 应固定当前环境模型，禁止每 tick 换模型或跨栈  
- **弱架构模型改方案正文** — 见 [models.md](models.md#方案文档谁写谁只提问)  
- **验收多份重复评审报告** — Overall Verification 单路即可；不为验收再 spawn 多路 reviewer  
- **非 Cursor 调 Cursor CLI** — 无 prompt **「Cursor 可用」** 不得 `agent -p`（见 [external-cli.md](external-cli.md)）  
- **子 agent 传 `model` 写代码** — 默认禁止；实施用**当前环境模型**，**不用** GPT / Opus  
- **写代码默认跨栈** — 禁止；除非 prompt 授权或当前环境无法执行  
- **只读规划占满父会话** — 规划/调研/方案委派子 agent（或各运行时等效分工）；见 [overview.md](overview.md)

## 输出模板（父 agent 每轮结尾）

```text
- 当前模型：<slug>（<运行时>）— 实际绑定，非运行时默认值
- 人类方向：<复述范围，非任务列表>
- TickType + 委派证据：<见 execution-contract.md>
- 本轮自主的选择：<roadmap id / 主题>（为何与此方向一致）
- 完成：<勾选项>
- 证据：<文件 / 测试命令 / commit hash>
- 验证：<pass/fail/skip 原因>
- Commit：<hash 或 skip 原因>
- Next：<下一轮建议，引用文档路径；**必填**；具体可执行。若无 → 调度者立即启动 Direction Discovery 重分析，不得结束 tick  
```
