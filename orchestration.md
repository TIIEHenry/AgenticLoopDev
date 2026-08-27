---
title: "开发 Loop 编排"
type: guide
status: accepted
phase: N/A
updated: 2026-08-27
summary: "父 agent 调度（不绑定消费仓库任务内容）；任务源优先级；本 wake 续派；关仓见 closeout 转换表。"
---

# Loop 编排

## Playbook 入口

可执行契约在 **[agent-playbooks/](agent-playbooks/INDEX.md)** 与 **[execution-contract.md](execution-contract.md)**（父 agent MVT），不在此重复全文。

| Playbook | 用途 |
|:---------|:-----|
| [parent-loop-orchestrator.md](agent-playbooks/parent-loop-orchestrator.md) | 顶层 Loop Goal / Success Criteria |
| [parallel-loop-waves.md](agent-playbooks/parallel-loop-waves.md) | Wave 0 发现并行、**冲突域 / slice 粒度**、Wave 2 多 slice、Wave 3 评审 |
| [subagent-loop-startup.md](agent-playbooks/subagent-loop-startup.md) | **每个子 agent 必读** |
| direction / plan / implementation / review / overall-verification / commit-gate | 按轮次选用 |

## 默认顺序

```
Parent 接收 Goal（/loop 只保活）
  → 方向决策（execution-contract 优先级表；有明确任务禁 Discovery/Wave 0）
  → Plan 或 Implementation（冲突域不交可多 slice；同域仅 1 写者；本 wake 派出）
  → Overall Verification（每轮必跑，实施 tick 单路）
  → Commit Gate → 字母槽本地 commit
  → 本波终态 → 同 wake [worktree-closeout.md](worktree-closeout.md)（转换表）
  → Parent Gate（停止条件见 execution-contract；禁止把未委派工作写成 Next 等下一轮 /loop）
```

## 运行时如何「派生子 agent」

| 运行时 | 机制 | 文档 |
|:-------|:-----|:-----|
| Cursor | IDE 内 `Task` 工具，`run_in_background` | [runtimes/cursor.md](runtimes/cursor.md) |
| Claude Code | `--agents` 自定义 agent；或会话内手动分工 | [runtimes/claude-code.md](runtimes/claude-code.md) |
| Codex | 多会话 / `codex exec` 分工；无统一 Task 工具 | [runtimes/codex.md](runtimes/codex.md) |
| 任意 | 外部 CLI 起独立进程 | [external-cli.md](external-cli.md) |

**原则**：子 agent 先读 `subagent-loop-startup.md` + 角色 playbook；父 agent 保持薄上下文。

**迭代原则**（工程质量优先、并行、隔离测试、不阻塞主轨）→ [overview.md § 迭代原则](overview.md#迭代原则)。

## 模型与委派

能力量化 → [models.md](models.md)。委派规则 → [models-and-delegation.md](models-and-delegation.md)。方案阶段可多视角评估；验收单路收口。

## 隔离环境测试

长耗时、易抢资源的验证**不阻塞**主轨：

| 类型 | 做法 |
|:-----|:-----|
| **adb / 烟测** | 子 agent + `run_in_background`；全局仅 1 后台 |
| **全量 build / instrumented** | 独立子 agent 或空闲字母槽 |
| **并行 slice 编码** | `$WT_ROOT/{A..G}/`；合入走 **merge 槽** |

`WT_ROOT` 不存在时 agent **须** `mkdir -p` 并按 [worktrees.md](worktrees.md) 初始化 **merge 槽**与字母池，**禁止**因目录缺失跳过 worktree。

主轨父 agent 继续本 wake 的剩余明确 slice 或关仓；等待结果时读子 agent 回报即可（同一会话续派，不等下一轮 `/loop`）。

## 并行硬约束

摘自 [parallel-loop-waves.md](agent-playbooks/parallel-loop-waves.md)：

- 读/评审尽量并行；**写路径 per-slice 串行**（文件集不重叠）  
- 同 tick 最多 **3** 个独立 slice 并行实施  
- 实施与 Overall Verification **不能**同一子 agent  
- **Wave 3 维度评审**仅 plan/ADR 首次或重大修订；实施 tick 只跑 Overall Verification → [parallel-loop-waves.md § Wave 3](agent-playbooks/parallel-loop-waves.md#wave-3--评审触发条件)

## 多 worktree 并行

目录约定、**merge 固定槽**、字母池 `A`…`G`、合并与同步、**两边保留** → **[worktrees.md](worktrees.md)**（§5 仅无并行兄弟；§5.1–5.2）。  
合入**时机**与波次关仓 → **[worktree-closeout.md](worktree-closeout.md)** 转换表。
