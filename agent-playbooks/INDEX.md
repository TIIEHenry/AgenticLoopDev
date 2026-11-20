---
title: "Agent Playbooks Index"
type: index
status: active
phase: N/A
created: 2026-06-17
updated: 2026-11-02
summary: "跨项目通用 playbook 索引；父 agent 另读 execution-contract（任务源优先级、本 wake 续派）。"
---

# Agent Playbooks Index

本目录保存**跨项目通用**的 agent playbook：父 agent 调度、子 agent 执行。与 [`loop-prompt.txt`](../loop-prompt.txt) 配套。父 agent 每轮还须读 [`execution-contract.md`](../execution-contract.md)（MVT、TickType）。项目任务、待处理项与验证命令按 [porting.md 的项目侧绑定](../porting.md#项目侧绑定) 读取，显式未采用的旧来源不读、不建。健康 gate 通用策略见 [`health-gates.md`](../health-gates.md)。

## Playbooks

| Playbook | Purpose |
|:---------|:--------|
| [parent-loop-orchestrator.md](parent-loop-orchestrator.md) | 顶层 loop prompt，要求每轮有目标、成功标准和退出条件 |
| [parallel-loop-waves.md](parallel-loop-waves.md) | 并行 wave；冲突域 / slice；Wave 0 仅无明确任务；Wave 4 本地 commit ≠ 合入 |
| [subagent-loop-startup.md](subagent-loop-startup.md) | 所有子 agent 必读的通用启动契约 |
| [direction-discovery-agent.md](direction-discovery-agent.md) | 寻找下一轮最有价值方向；没有新方向时选择 Research Queue / Deferred Gap |
| [plan-roadmap-agent.md](plan-roadmap-agent.md) | 写方案、优化方案、拆 roadmap、记录待研究项和延期缺口 |
| [architecture-first-design.md](architecture-first-design.md) | plan 门禁：问题类 + **独立 ≥中强架构审查**（贵价须明文；审查 ≠ 授权）；与 Wave 3/OV 划界 |
| [review-question-resolve-loop.md](review-question-resolve-loop.md) | 反复评审、问题提取、阻塞调查和收敛循环 |
| [implementation-agent.md](implementation-agent.md) | 实施一个边界明确的 slice，但不宣布最终完成 |
| [overall-verification-agent.md](overall-verification-agent.md) | 多维评审和实施后的总体验收（回答“做完了吗”） |
| [commit-gate-agent.md](commit-gate-agent.md) | 落地前检查 diff、文档门禁、中文 commit message（loop **默认自主 commit** 前必跑） |

## Default Loop Order（MVT）

详见 [execution-contract.md](../execution-contract.md)。摘要：

1. 父 agent 读 execution-contract + 本文。
2. **方向决策** — 按 [任务源优先级](../execution-contract.md#方向决策任务源优先级ssot) 轻量确认或在第 4 档运行 Discovery；无安全目标按契约记录来源和限制后停止。
3. 有安全目标时按契约 **Task** Plan **或** Implementation（verify-only 跳过）；无目标不造动作。
4. **Task** Overall Verification（**必**，且 ≠ #3）。
5. 有变更 → **Task** Commit Gate → 父 agent commit/push。
6. 更新绑定的任务/协调记录与待处理项（无绑定旧项目沿用默认）；Final Output 含委派证据。

Wave 0 / Wave 3 / Review-Question-Resolve 仅按 execution-contract 与 parallel-loop-waves 触发。

## Verification vs Commit Gate

| Agent | 何时调用 | 核心问题 |
|:------|:---------|:---------|
| Overall Verification | **每轮必跑** | 做完了吗？ |
| Commit Gate | **有变更、准备落地时** | 能安全 commit 吗？ |

## Language Rule

子 agent 更新文档、进度、roadmap、Deferred Gaps、Research Queue、commit message 或 PR 描述时，面向人的正文必须使用中文。代码标识、路径、命令、API 名、枚举名、日志和测试输出保持原文。

## Hard Rule

Implementation Agent 不得宣布自己实现的工作最终完成。完成必须由 Overall Verification Agent 独立对照原始目标、代码、测试、roadmap、文档和已记录缺口后裁决。
