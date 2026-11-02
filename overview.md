---
title: "开发 Loop 概览 (ALDD 体系)"
type: guide
status: accepted
phase: N/A
updated: 2026-11-02
summary: "Agentic-Loop-Driven Development (ALDD) 角色、迭代原则、目标；/loop 只保活；合入时机见 closeout；任务源优先级见 execution-contract。"
---

# 开发 Loop 概览 (ALDD 体系)

## 是什么

**开发 Loop** 是 **Agentic-Loop-Driven Development（ALDD，以智能体循环为执行单元的研发工程体系）** 的核心运行机制。

它指：父 agent（协调者）按固定或动态节奏，反复执行「读进度 → 选任务 → 委派/实施 → 验证 → 更新 status/roadmap」的一轮 **tick**，直到 slice 完成、方案定稿或需要人类裁决。详见 [README.md](README.md)。

可在多种 **运行时** 上执行（见 [runtimes/INDEX.md](runtimes/INDEX.md)）。各环境唤醒方式不同，**语义层**相同。**`/loop` 只保活**；本 wake 续派直到 [execution-contract.md](execution-contract.md) 停止条件。合入时机 → [worktree-closeout.md](worktree-closeout.md)。

## 迭代原则

| 原则 | 说明 |
|:-----|:-----|
| **工程质量优先，兼顾费用** | 测试、文档、契约正确性优先；贵模型仅在有收益处显式使用，不为「看起来更聪明」空烧 token |
| **多 agent 并行** | 无**冲突域**重叠的 slice、读盘/调研、方案评估可并行；**同一冲突域每 tick 仅 1 写者**；父 agent 薄调度 → [orchestration.md](orchestration.md)、[parallel-loop-waves.md](agent-playbooks/parallel-loop-waves.md) |
| **多视角评估** | **方案/架构首次起草与重大修订**时并行多视角（review、plan-analyst、质疑清单）；**验收**仍单路收口，避免重复写评审报告 |
| **架构设计付费最优先** | 写 `dev/plans/`、ADR、架构 doc 时先考虑付费档。**架构定格是 Opus 5.5**。Fable 5.1 / GPT 5.6 仅点名该档。未授权才降级 **Grok 4.7** → [models.md](models.md) |
| **实施少纠结模型** | **写代码、修 bug、跑测试**阶段固定**当前环境模型**，禁止每 tick 重议选型或跨栈换模型 |
| **契约忠实实施** | **禁止擅自简化** plan/roadmap/ADR；做不了须改文档、写队列或人类裁决，不得用缩水实现勾 checkbox |
| **套件只读（tick 内）** | **`dev/loop/**` 仅人类可改**；loop 中 agent 不得自发修 playbook/契约，拟议变更交人类 |
| **运行态隔离** | `loop.pid`、lock、cache、logs 等运行态文件写到 `dev/loop/.runtime/`，并保持 git ignore；不要混入套件正文文件 |
| **隔离环境测试** | 烟测、长构建、instrumented 放**子 agent / worktree / 后台**，不占父会话主轨 → [worktrees.md](worktrees.md)、[external-cli.md](external-cli.md) |
| **不阻塞开发** | 主轨继续推进；等待测试结果时并行其他 slice 或文档，adb 全局互斥时 skip 并记录 |
| **自主 commit + push** | **Loop 会话**：OV ≠ FAIL 且有实质变更 → 字母槽 **commit**；集成分支 **push 只在 merge 槽**且须 [worktree-closeout.md](worktree-closeout.md) 转换表允许。仅 `Git：禁止 commit` 关闭。**非 Loop 会话**须用户明确要求才可 commit |

## 角色

| 角色 | 职责 |
|:-----|:-----|
| **人类** | 提供**当前模型** + **大致方向**；不指定具体任务；可选 `Git：禁止 commit` 暂停落地；裁决 blocking → [human-input.md](human-input.md) |
| **父 agent** | 调度、拆 wave、合成结论、更新 status；尽量不深入实现细节 |
| **子 agent** | 按 [playbook](agent-playbooks/) 读代码、改文件、跑测试、写文档 |
| **外部 CLI agent**（跨栈） | 父 agent 不在目标栈时：`claude -p`、`opencode run` 等（见 [models-and-delegation.md](models-and-delegation.md)） |

## 与 `AGENTS.md` 开发流程

Loop 按根 `AGENTS.md` 与项目开发入口的 [绑定](porting.md#项目侧绑定) 读取实际任务与文档规则。ProjectWiki 管需求、知识、生命周期和检查，Loop 管派工、冲突隔离、槽位恢复、独立验收和收口。

已授权且目标、边界、验收明确的普通任务可直接 `implement`，依据和验证可在已有任务记录或提交说明。重要风险、跨模块协调、交接或未定设计才先规划；应保留的设计取舍按项目规则写 ADR。无需同时创建 plan、roadmap 与 phase。任务来源枯竭时核对实际来源并记录停止原因，不为保活制造计划。已有 status / board 承载的调度恢复状态继续保留，不复制多份进度。

## 何时开 Loop

| 适合 | 不适合 |
|:-----|:-------|
| 已授权且目标、边界、验收明确 | 尚无方案/ADR 的架构抉择 |
| 回归测试、文档补齐、缺口修补 | 需频繁人类 UI 确认 |
| 父 agent + 子 agent 并行多轨 | 单文件 trivial bugfix（直接改即可） | 同质模板化工作却「每项一槽、每槽一 merge」 |

**调度粒度**：并行与占槽按**冲突域 + slice**，不是按 roadmap 枚举 ID 逐条拆 agent；见 [parallel-loop-waves.md](agent-playbooks/parallel-loop-waves.md)。

## 下一步

- 单轮怎么做 → [workflow.md](workflow.md)
- 选 IDE → [runtimes/INDEX.md](runtimes/INDEX.md)
- 复制哪条 prompt → [prompts.md](prompts.md)
