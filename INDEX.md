---
title: "开发自动化 Loop 索引"
type: index
status: accepted
phase: N/A
updated: 2026-08-27
summary: "跨项目通用 Loop：不绑定消费仓库任务内容；任务源优先级 + 本 wake 续派；/loop 只保活；合入时机见 closeout 转换表；移植见 porting.md。"
---

# 开发自动化 Loop

> **套件定位**：`dev/loop/` 为**跨项目通用** Loop 套件（`loop-prompt.txt` + `agent-playbooks/` + 工作流文档）。**整目录复制**到其他仓库，不在套件内写某仓库的任务内容或模块名 → [porting.md](porting.md)。Loop 只调度「有没有明确可执行工作」；条目留在消费仓库的 `dev/progress/` / `dev/roadmap/`。  
> **`/loop` 只保活**；本 wake 续派。合入时机 → [worktree-closeout.md](worktree-closeout.md) 转换表。任务源优先级 → [execution-contract.md](execution-contract.md)。  
> **`dev/loop/` 修改须经人类同意**；Loop tick 中 agent **不得**自行改套件内文件。  
> **项目专属**（不进 `dev/loop/`）：`dev/progress/`（status、两队列、**health-gates 命令**）、根 `AGENTS.md` / `CLAUDE.md`、各仓库 `dev/roadmap/`。  
> **运行态目录**：`loop.pid`、lock、cache、logs 等本地运行态文件写到 `dev/loop/.runtime/`，并由套件内 `.gitignore` 忽略。  
> **Cursor**：`.cursor/rules/` 仅为 IDE 可选注入，**不是** loop 套件的一部分；SSOT 始终是 `dev/loop/`。  
> **Cursor skills（手动调用）**：套件内 [`skills/`](skills/INDEX.md) + [`scripts/install-cursor-skills.sh`](scripts/install-cursor-skills.sh) → 安装到项目 `.cursor/skills/`。

## 三层模型

```
┌─────────────────────────────────────────────────────────┐
│  L1 语义层（平台无关）                                     │
│  workflow · playbooks · prompts · status/roadmap        │
├─────────────────────────────────────────────────────────┤
│  L2 运行时（Cursor / **Grok CLI** / Claude Code / Qoder / Antigravity / Codex / OpenCode）│
│  模型声明（slug）、内置委派；Grok 子 agent 优先、CLI 其次；跨栈 CLI → models-and-delegation   │
├─────────────────────────────────────────────────────────┤
│  L3 跨环境 CLI（父 agent 不在目标栈时）                    │
│  **grok** / agent / claude / qodercli / agy / codex / opencode / kimi --yolo  │
└─────────────────────────────────────────────────────────┘
```

**换 IDE 时**：L1 基本不变；换 L2 适配文档；L3 按可用 CLI 选用。

## 文档地图

| 文档 | 层级 | 说明 |
|:-----|:-----|:-----|
| [porting.md](porting.md) | L1 | **移植与同步**：`rsync` 复制套件、**skills 一键安装**、项目侧清单 |
| [skills/INDEX.md](skills/INDEX.md) | L1→项目 | **可手动调用** Cursor skills（Arch-First、多方方案评审、sync-docs-and-commit） |
| [human-input.md](human-input.md) | L1 | **人类只给模型+方向**；**Sticky** 调度不变量；任务 agent 自选 |
| [models.md](models.md) | L1 | 能力对比**单表** + **费用门禁**（Opus/Opus 4.6/GPT 5.5/5.6/Ultimate 须 prompt 授权；**Opus 4.6=写作最强**·CC CLI；Arch-First ≠ 授权） |
| [models-and-delegation.md](models-and-delegation.md) | L1 | 任务→运行时/委派；跨栈门禁见 external-cli |
| [overview.md](overview.md) | L1 | **迭代原则**、角色、与 `AGENTS.md` 开发流程关系 |
| [workflow.md](workflow.md) | L1 | 单轮 tick 标准步骤、退出条件、文档门禁 |
| [execution-contract.md](execution-contract.md) | L1 | **MVT**、任务源优先级、本 wake 续派、委派证据 |
| [health-gates.md](health-gates.md) | L1 | **通用**：gate 冷却、verify-only 门禁 |
| [../progress/health-gates.md](../progress/health-gates.md) | 项目 | **本仓库**：集成编译与聚焦/grand gate 命令 |
| [orchestration.md](orchestration.md) | L1 | 父 agent 调度、子 agent 契约、并行 wave |
| [worktrees.md](worktrees.md) | L1 | Worktree 池：merge 固定槽、字母槽 A–G、**两边保留**真三路合并、合入前同步 main |
| [worktree-closeout.md](worktree-closeout.md) | L1 | **关仓 + 合入时机转换表**；P0–P7；字母槽对齐 merge HEAD |
| [prompts.md](prompts.md) | L1 | 唯一启动契约 [`loop-prompt.txt`](loop-prompt.txt)（全项目通用） |
| [agent-playbooks/](agent-playbooks/INDEX.md) | L1 | 子 agent playbook（与 loop-prompt 配套） |
| [runtimes/INDEX.md](runtimes/INDEX.md) | L2 | 运行时对比与选型 |
| [runtimes/grok.md](runtimes/grok.md) | L2 | **Grok CLI**；子 agent 无 Grok 档时的架构/doc/bug 通道；`grok -p` |
| [runtimes/cursor.md](runtimes/cursor.md) | L2 | Cursor `/loop`（**`notify_on_output` + 替换旧 loop**）、`Task` 子 agent |
| [runtimes/claude-code.md](runtimes/claude-code.md) | L2 | Claude Code 交互会话、`--agents`、mimo-v2.5-pro |
| [runtimes/qoder.md](runtimes/qoder.md) | L2 | Qoder；**Ultimate = GPT 5.6**（须人类显式指定） |
| [runtimes/antigravity.md](runtimes/antigravity.md) | L2 | Antigravity 交互/非交互、gemini-3.5-flash / 3.1-pro |
| [runtimes/codex.md](runtimes/codex.md) | L2 | Codex 交互 / `codex exec`、resume |
| [runtimes/opencode.md](runtimes/opencode.md) | L2 | OpenCode、`deepseek-v4-pro`、`opencode run` |
| [external-cli.md](external-cli.md) | L3 | **门禁**：同栈禁止、Cursor 可用、烟测 |
| [cli/INDEX.md](cli/INDEX.md) | L3 | **命令指南**：各栈参数与示例（含 [**Grok**](cli/grok.md)、[Qoder](cli/qoder.md)、[Kimi `--yolo`](cli/kimi.md)） |

## 同目录兄弟（可执行物）

| 路径 | 用途 |
|:-----|:-----|
| [agent-playbooks/](agent-playbooks/INDEX.md) | 子 agent 角色契约与并行 wave |
| [skills/](skills/INDEX.md) | Cursor skills SSOT；`./scripts/install-cursor-skills.sh` |
| [loop-prompt.txt](loop-prompt.txt) | Loop 启动契约（**全项目通用**） |
| [progress/status.md](../progress/status.md) | 每轮 tick 行动记录（动态） |
| [../roadmap/active/](../roadmap/active/INDEX.md) | 消费仓库活跃 phase 任务源（Loop 只问有无明确项；Discovery 仅优先级第 4 档） |
| [../progress/deferred-gaps.md](../progress/deferred-gaps.md) | Deferred Gaps **SSOT** |
| [../progress/research-queue.md](../progress/research-queue.md) | Research Queue **SSOT** |
| [../progress/health-gates.md](../progress/health-gates.md) | 本仓库测试 gate 命令（项目专属） |

## 相关

| 文档 | 说明 |
|:-----|:-----|
| [multi-agent-design-workflow.md](../../docs/guides/multi-agent-design-workflow.md) | **方案定稿前**的多 agent 探索（非 loop tick） |
| [cli/INDEX.md](cli/INDEX.md) | L3 CLI 命令指南 |
| [external-agent-cli.md](../../docs/guides/external-agent-cli.md) | 项目侧入口（指向 `cli/`） |
