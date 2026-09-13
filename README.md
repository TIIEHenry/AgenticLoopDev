---
title: "AgenticLoopDev — 跨项目通用的 Multi-Agent 自治研发 Loop 套件"
type: index
status: accepted
phase: N/A
updated: 2026-09-14
summary: "AgenticLoopDev: 跨项目通用、工业级自治的多 Agent 软件工程自动化循环套件。以纯契约解耦，支持任何语言与技术栈，提供严谨的父子调度、Worktree 物理工位隔离、真三路合并与全生命周期质量门禁。"
---

# AgenticLoopDev

> **面向 AI Coding Agent 的跨项目通用、工业级自治软件工程自动化开发循环套件**  
> *A Truly Project-Agnostic, Autonomous Multi-Agent Software Development Loop Suite.*

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Architecture: 3-Layer Model](https://img.shields.io/badge/Architecture-3--Layer%20Model-green.svg)](#系统架构三层模型)
[![Cross-Project: Verified](https://img.shields.io/badge/Cross--Project-Verified-brightgreen.svg)](#跨项目解耦设计)
[![Worktree: Multi-Slot Safe](https://img.shields.io/badge/Worktree-Multi--Slot%20Isolated-orange.svg)](#worktree-多工位池与人类工位隔离)

**AgenticLoopDev** 是一个将**软件工程严谨纪律**赋予 AI Coding Agent（如 Cursor、Claude Code、Grok CLI、Qoder、Codex、OpenCode 等）的自动化研发闭环系统。

它不是简单的提示词集合，而是一套**字节级可跨项目复用**的自治调度引擎。通过**语义层契约解耦**、**父子 Agent 职责隔离**、**Worktree 物理工位池**、**真三路无损合并**与**独立红蓝验收门禁**，让 AI 能够自主寻找高价值任务、起草架构方案、并行编写代码并保证工程质量，同时绝不冲掉人类正在进行的未提交工作。

---

## 目录

- [为什么需要 AgenticLoopDev？](#为什么需要-agenticloopdev)
- [跨项目解耦设计](#跨项目解耦设计)
  - [架构边界契约（SSOT 划分）](#架构边界契约ssot-划分)
  - [跨领域工程场景实战验证](#跨领域工程场景实战验证)
  - [多语言技术栈通用适配示例](#多语言技术栈通用适配示例)
- [系统架构：三层模型](#系统架构三层模型)
- [核心机制与工程纪律](#核心机制与工程纪律)
  - [1. 父子 Agent 协同与 MVT（最小可行路径）](#1-父子-agent-协同与-mvt最小可行路径)
  - [2. Worktree 多工位池与人类工位隔离](#2-worktree-多工位池与人类工位隔离)
  - [3. 真三路合并与“两边保留”（Keep Both Sides）](#3-真三路合并与两边保留keep-both-sides)
  - [4. 全生命周期质量门禁（Quality Gates）](#4-全生命周期质量门禁quality-gates)
  - [5. 模型分层与费用门禁](#5-模型分层与费用门禁)
- [开箱即用的 IDE Skills（含人类主动触发门禁）](#开箱即用的-ide-skills含人类主动触发门禁)
- [快速开始](#快速开始)
  - [接入方式 A: Git Submodule（推荐）](#接入方式-a-git-submodule推荐)
  - [接入方式 B: Rsync 镜像同步](#接入方式-b-rsync-镜像同步)
  - [消费项目脚手架初始化](#消费项目脚手架初始化)
  - [安装 Cursor Skills](#安装-cursor-skills)
  - [发起第一次自治循环](#发起第一次自治循环)
- [单轮 Tick 执行生命周期](#单轮-tick-执行生命周期)
- [不可逾越的红线（Hard Guardrails）](#不可逾越的红线hard-guardrails)
- [仓库目录导航](#仓库目录导航)
- [开源协议与贡献](#开源协议与贡献)

---

## 为什么需要 AgenticLoopDev？

在长期、复杂的真实生产开发中，完全放任单一 AI 对话式写代码通常会遭遇以下严重瓶颈：

| 常见 AI 研发痛点 | 传统 Coding Agent 表现 | AgenticLoopDev 的解法 |
|:-----------------|:----------------------|:----------------------|
| **上下文爆炸与偏航** | 调度 Agent 亲自读写大量业务代码，上下文迅速耗尽，失去全局规划能力。 | **调度即分发，父薄子厚**：父 Agent 严格只负责调度，业务代码编写与测试全部委派给子 Agent。 |
| **虚假完结与 Stub 欺诈** | 遇到硬骨头偷偷用 TODO/Stub 缩水实现，然后在聊天里“宣布完成”打勾。 | **契约实施 + 独立验收（OV）**：由独立的 Overall Verification Agent 审查源码与契约，严禁未经文档批准的任何缩水。 |
| **Git 事故冲掉人类改动** | AI 频繁执行 `git reset --hard`、`checkout` 或切分支，覆盖人类在工作区正在编辑的文件且不进 reflog。 | **物理工位隔离（Worktree Pool）**：人类常驻 `edit` 主工位，AI 并行进字母槽 `A-J`，集成进 `merge` 槽，机器门禁拦截越界操作。 |
| **合并吞代码** | 遇到合并冲突直接 `--ours` 或 `--theirs` 单侧覆盖，导致他人或先前的改动静默丢失。 | **强制真三路合并（两边保留）**：任何一方改动必须保留；两侧均修改须手工/语义解决冲突，合入前必须跑双向保留门禁脚本。 |
| **项目强绑定难以迁移** | Prompt 里充斥着具体仓库的模块名、Gradle 命令、构建规则，换个项目就得全盘推翻重写。 | **三层抽象与纯契约解耦**：套件内部零项目特例，通过标准任务源接口与项目构建门禁对接，一套规范通吃全部技术栈。 |

---

## 跨项目解耦设计

AgenticLoopDev 的核心设计准则是：**套件内部没有任何特定项目的硬编码（Zero Project-Specific Hardcoding）**。

### 架构边界契约（SSOT 划分）

套件通过明确的 **SSOT 边界** 划分，将通用调度能力与项目具体业务彻底分离：

```
┌─────────────────────────────────────────────────────────────┐
│                 AgenticLoopDev 套件内部（通用 SSOT）          │
│  dev/loop/ (loop-prompt.txt · playbooks · worktrees · ...)  │
│  - 纯通用规则：调度算法、优先级表、工位机制、门禁策略、Skills     │
│  - 字节级跨仓库同步（Git Submodule / Rsync 镜像）            │
└──────────────────────────────┬──────────────────────────────┘
                               │ 依赖抽象契约接口（约定相对路径）
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 消费项目侧（项目专属配置与任务源）               │
│  dev/progress/status.md          ── 迭代心跳与当次会话记录    │
│  dev/progress/health-gates.md   ── 项目专属构建与测试命令    │
│  dev/progress/deferred-gaps.md  ── 延期缺口 SSOT              │
│  dev/progress/research-queue.md ── 研究队列 SSOT              │
│  dev/roadmap/active/            ── 活跃任务清单 (Checkboxes)  │
│  dev/loop/.runtime/             ── 本地运行态（pid/lock，gitignore）│
└─────────────────────────────────────────────────────────────┘
```

### 跨领域工程场景实战验证

该套件已在多个不同架构领域、不同技术栈与开发模式的大型生产级工程中作为核心开发引擎落地运行，验证了其纯契约架构的强大通用性：

| 维度 | 实战场景 A：大型多模块底层系统/分布式引擎 | 实战场景 B：复杂跨平台客户端/大型历史源码移植工程 |
|:-----|:-----------------------------------------|:--------------------------------------------------|
| **项目形态** | 几十个模块的高并发后端系统、多平台编译架构与分布式集群 | 移植成熟桌面框架至移动端平台，涉及大量跨架构编译与原生绑定 |
| **典型技术栈** | 现代静态强类型语言 (Kotlin / Java / Rust / Go) + 多模块构建系统 | 混合多语言环境 (Java / C++ / 原生 Shell / 前端 DSL) + 复杂工具链 |
| **测试与门禁** | 单元测试、严格的多模块单向依赖门禁、架构分层防违规脚本 | 平台装配构建、原生动态链接库编译、UI 与交互状态回归测试 |
| **接入方式** | Git Submodule 挂载至 `dev/loop` | 跨项目字节同步镜像至 `dev/loop` |
| **共用资产** | **100% 共享**完全相同的 `loop-prompt.txt`、Playbooks 角色库、Worktree 调度与 Cursor Skills！ |

**结论**：无论是底层高性能服务端架构，还是顶层复杂的客户端移植工程，抑或是 Web 全栈应用，套件内部**不需要修改任何一行代码或脚本**。所有与具体项目相关的编译命令、质量门禁、开发阶段与任务规划，全部自然沉淀在项目侧的 `dev/progress/` 与 `dev/roadmap/` 中。

### 多语言技术栈通用适配示例

AgenticLoopDev 本身不依赖任何编程语言或构建系统。要接入新语言的项目，只需在项目侧 `dev/progress/health-gates.md` 中声明对应的构建与校验指令：

```markdown
<!-- Node.js / TypeScript 项目 -->
- 快速测试门禁: `npm test` 或 `pnpm vitest run`
- 聚焦检查门禁: `pnpm typecheck && pnpm lint`
- 全量质量门禁: `pnpm build && pnpm test:coverage`

<!-- Rust 项目 -->
- 快速测试门禁: `cargo test --lib`
- 聚焦检查门禁: `cargo check && cargo clippy -- -D warnings`
- 全量质量门禁: `cargo test --all-targets && cargo fmt --check`

<!-- Python 项目 -->
- 快速测试门禁: `pytest tests/unit/`
- 聚焦检查门禁: `ruff check . && mypy .`
- 全量质量门禁: `pytest --cov=. && ruff format --check .`

<!-- Go 项目 -->
- 快速测试门禁: `go test -short ./...`
- 聚焦检查门禁: `golangci-lint run`
- 全量质量门禁: `go test -race ./... && go build ./...`
```

---

## 系统架构：三层模型

AgenticLoopDev 采用清晰的三层模型，解耦业务语义、AI 运行时与外部 CLI 调用：

```
┌──────────────────────────────────────────────────────────────────────────┐
│ L1 语义层（平台与语言无关 · 纯通用契约）                                      │
│ workflow · playbooks · loop-prompt · execution-contract · worktree-pool   │
├──────────────────────────────────────────────────────────────────────────┤
│ L2 运行时适配层（AI IDE & 交互平台适配）                                     │
│ Cursor (/loop + Task) · Claude Code (--agents) · Qoder · Grok · OpenCode │
├──────────────────────────────────────────────────────────────────────────┤
│ L3 跨环境 CLI 委派层（跨模型与外部工具调用）                                  │
│ grok -p · claude -p · codex exec · opencode run · kimi --yolo           │
└──────────────────────────────────────────────────────────────────────────┘
```

- **换项目时**：L1、L2、L3 资产完全不变；仅需按约定初始化项目侧的 `dev/progress/`。
- **换 IDE / 模型时**：L1 业务契约完全不变；仅切换 L2 唤醒方式与 L3 委派命令。

---

## 核心机制与工程纪律

### 1. 父子 Agent 协同与 MVT（最小可行路径）

调度者（Parent Agent）与实施者（Subagent）严格分离：

```
                    ┌────────────────────────┐
                    │      人类输入方向       │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │      Parent Agent      │ ◄── 严格禁止直接修改生产源码！
                    │    (薄调度 / MVT 决策)  │
                    └─────┬──────┬─────┬─────┘
           优先级 1-3      │      │     │  优先级 4 (枯竭/失效)
      ┌───────────────────┘      │     └───────────────────┐
      ▼                          ▼                         ▼
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│  Implement   │          │     Plan     │          │  Discovery   │
│   (子实施)    │          │  (架构方案)   │          │ (全量探路)    │
└──────┬───────┘          └──────┬───────┘          └──────┬───────┘
       │                         │                         │
       └──────────────────┬──────┴─────────────────────────┘
                          │
               ┌──────────▼──────────┐
               │ Overall Verification│ ◄── 独立红蓝验收（不得由实施者自检）
               └──────────┬──────────┘
                          │ 通过 (PASS)
               ┌──────────▼──────────┐
               │     Commit Gate     │ ◄── 检查文档与代码同心提交、中文 Message
               └─────────────────────┘
```

- **任务源优先级（SSOT）**：
  1. 字母槽有正在推进的 `occupied` 任务 → 继续推进实施；
  2. 任务源有 open 项或上轮 Next 轻量确认有效 → 派发 Implementation / Plan；
  3. Research Queue 或 Deferred Gaps 有明确可推进项 → 推进该项；
  4. **仅当 1–3 均枯竭** 或任务失效时 → 才允许启动 Wave 0 全量 Direction Discovery。严禁在有明确任务时空转做全局分析！
- **调度即分发**：父 Agent 绝不改动任何生产业务源码（`*.kt`, `*.java`, `*.ts`, `*.py` 等）。发现代码需修改时，必须且只能 spawn 子 Agent 落地。

### 2. Worktree 多工位池与人类工位隔离

为解决多 Agent 并行冲突与误覆盖人类代码的灾难，设计了固定的 Worktree 物理槽位池：

```
/path/to/Repo/ (主工作区)  ─────────► [ 工位: edit 分支 ]   (人类固定工位，Agent 严禁占位)
$WT_ROOT/merge             ─────────► [ 工位: merge 槽 ]   (唯一集成槽，随时对齐 origin/main)
$WT_ROOT/A ~ J             ─────────► [ 工位: 字母槽 A-J ] (并行实施槽，独立分支，按需复用)
```

- **人类工位保护（`edit`）**：主工作区常驻 `edit` 分支，人类在其中写草稿、调试。任何 AI Loop 并行操作不得占用主工作区。对齐 `main`、切分支、`rebase`、`reset`、`clean` 等破坏性命令在主工作区一律触发安全门禁。
- **集成基线（`merge` 槽）**：所有完成的字母槽先汇总合入 `merge` 槽，在 `merge` 槽运行全量构建和门禁验证。验证通过后，方可由 `merge` 槽向主干同步。

### 3. 真三路合并与“两边保留”（Keep Both Sides）

- **严禁静默覆盖**：合入代码或同步 `main` 时，**绝对禁止**使用 `git checkout --ours / --theirs` 或 `git merge -X ours / theirs`。
- **两边保留原则**：仅单侧修改保留该侧；两侧均修改必须做真正的语义三路合并。
- **机器校验**：合并完成后必须通过 `scripts/check-merge-both-sides.sh` 校验，杜绝任何一方的工作成果被静默吞掉。

### 4. 全生命周期质量门禁（Quality Gates）

- **Arch-First 方案首发门禁**：重大改动、新问题点或架构调整前，必须先产出方案文档/ADR，并由中强架构模型（如 Grok / GPT-5.5 / Opus）进行独立审查，禁止“边写边凑”。
- **文档与代码同心提交**：严禁只提交代码不更文档。包含业务变更的提交必须同步更新行动层文档（`status.md`、roadmap checkboxes、相关 spec）。
- **独立总体验收（Overall Verification）**：由独立的子 Agent 对照任务目标、测试结果、代码实现、文档更新进行只读裁决，产出 `PASS` / `PARTIAL` / `FAIL` / `HUMAN_DECISION_REQUIRED`。

### 5. 模型分层与费用门禁

- **方案与架构档**：首发起草方案、重大重构、复杂 Debug 优先选用强推理/强架构模型（子 Agent Grok 优先，CLI 其次）。
- **实施与编码档**：常规写代码、修单测、勾 Checkbox 固定使用当前开发环境模型，禁止每轮无意义地随意切换模型。
- **超贵模型门禁**：对高资费模型实施严格的会话显式授权机制，防止在循环中不知不觉耗尽配额。

---

## 开箱即用的 IDE Skills（含人类主动触发门禁）

套件附带了标准化、跨项目可复用的 IDE 技能（支持 Cursor 与 Claude Code）：

| Skill | 触发机制 | 说明 |
|:------|:---------|:-----|
| [sync-docs-and-commit](skills/sync-docs-and-commit/SKILL.md) | `/sync-docs-and-commit` 或实施收尾语境 | 实施完成后的标准化收尾：界定本次主题范围、同步规格设计文档、更新进度状态、同主题一并暂存并生成规范中文 Message。 |
| [architecture-first-solution](skills/architecture-first-solution/SKILL.md) | **🔒 仅人类显式调用**<br>`@architecture-first-solution`<br>`/architecture-first-solution` | **架构优先方案设计**：从问题类别与系统设计模式切入根治，完成后调度独立架构模型审查。<br>**硬规则：配置 `disable-model-invocation: true`，禁止 Agent 在排障/写代码时自行触发！** |
| [multi-party-design-review](skills/multi-party-design-review/SKILL.md) | **🔒 仅人类显式调用**<br>`@multi-party-design-review`<br>`/multi-party-design-review`<br>口令「启动多方评审」 | **多方反复评审流水线**：多路并行候选方案 → 相对强综合 → 快速模型多视角交叉审查 → 执行方提问细化环。<br>**硬规则：配置 `disable-model-invocation: true`，禁止 Agent 因「觉得该评审」而擅自启动！** |

> ⚠️ **核心铁律：架构优先与多方评审技能的触发权限属于人类**  
> `architecture-first-solution` 和 `multi-party-design-review` 涉及较重的架构推演与多模型调度成本，属于高杠杆操作。两个技能的元数据均声明了 **`disable-model-invocation: true`**。在日常的 bugfix、编码或单测循环中，**Agent 绝对不允许自行判断并暗中启动这两个重型流水线，必须等待人类主动通过 `@`、斜杠命令或特定口令明确授权调用**。

通过安装脚本，Skills 可以作为薄指针或 Symlink 载入，**修改套件后无需重新安装**。

---

## 快速开始

### 接入方式 A: Git Submodule（推荐）

在你的项目根目录下：

```bash
# 添加 AgenticLoopDev 作为 submodule 到 dev/loop 目录
git submodule add git@github.com:TIIEHenry/AgenticLoopDev.git dev/loop
git submodule update --init --recursive
```

### 接入方式 B: Rsync 镜像同步

若不便使用 submodule，可以直接将套件克隆并同步到目标项目的 `dev/loop/`：

```bash
# 将套件整目录复制到消费项目
rsync -a --delete /path/to/AgenticLoopDev/ /path/to/YourProject/dev/loop/
```

### 消费项目脚手架初始化

在你的项目根目录创建以下项目侧约定文件（按你的项目实际情况填写，**不修改 `dev/loop/` 内的任何文件**）：

```bash
mkdir -p dev/progress dev/roadmap/active dev/loop/.runtime
```

#### 1. `dev/progress/health-gates.md`（项目构建门禁定义）
定义项目真实的构建与单测命令（示例）：
```markdown
# 质量门禁命令
- 快速单测: `npm test` 或 `./gradlew test` 或 `pytest` 或 `cargo test`
- 全量门禁: `npm run check` 或 `./gradlew check` 或 `cargo clippy`
```

#### 2. `dev/progress/status.md`（迭代状态与心跳）
```markdown
# 当前迭代状态
- 活动任务: 正在进行的 feature / bugfix
- 最近日志: 记录每次 loop tick 的改动与结论
```

#### 3. `dev/progress/deferred-gaps.md` & `research-queue.md`
- `deferred-gaps.md`: 记录无法立即解决、需延期修复的技术债与已知缺口。
- `research-queue.md`: 记录待调研与验证的候选技术方案。

#### 4. 项目接入导航（`AGENTS.md` 或 `CLAUDE.md`）
在项目根目录的开发向导或规则文件中增加一行导航（纯文本示例）：
```markdown
| 开发自动化 Loop (`dev/loop/INDEX.md`) | 启动契约: `/loop @dev/loop/loop-prompt.txt` |
```

### 安装 Cursor Skills

在套件根或消费项目的 `dev/loop` 下执行：

```bash
# 模式 1：推荐，为当前机器所有 Cursor 项目安装个人级薄指针
./dev/loop/scripts/install-cursor-skills.sh --personal

# 模式 2：为当前项目创建软链接（.cursor/skills/ -> dev/loop/skills/）
./dev/loop/scripts/install-cursor-skills.sh
```

### 发起第一次自治循环

在 Cursor Composer 或支持定时唤醒的 AI CLI 中运行：

```text
/loop 10m @dev/loop/loop-prompt.txt
当前模型：<模型名称，如 claude-sonnet / grok / gpt-4o>
方向：实现用户模块的基础登录与密码加密验证逻辑
```

Agent 将自动依据 `loop-prompt.txt` 展开 Boot 检查、读取任务源、按优先级委派子 Agent 编码与验收！

---

## 单轮 Tick 执行生命周期

每次唤醒执行的最小闭环：

```
[0. Boot 校验] ──► 工具强制读取 loop-prompt.txt 与 execution-contract.md
       │
[1. 状态加载] ──► 读取 status.md、两队列与 active roadmap
       │
[2. 优先级决策] ──► 匹配任务源优先级（若已有明确任务，严禁跑 Wave 0）
       │
[3. 派发实施] ──► 父 Agent 分配字母槽，调度 Implementation Agent 并行编写
       │
[4. 独立验收] ──► 调度 Overall Verification Agent 审查代码与真实单测运行结果
       │
[5. 提交门禁] ──► 调度 Commit Gate 检查改动范围，父 Agent 在对应槽位执行规范 commit
       │
[6. 关仓与合并] ──► 满足 closeout 转换条件时，经由 merge 槽无损合入并推送到主干
```

---

## 不可逾越的红线（Hard Guardrails）

为了保障研发过程的安全与稳定，AgenticLoopDev 设定了以下硬性禁令：

1. 🚫 **禁止父 Agent 亲自编写业务代码**：调度者亲自上手改 prod 源码将直接导致 Overall Verification 不予通过。
2. 🚫 **禁止自主修改套件自身**：在自主 Loop 运行期间，AI **严禁修改 `dev/loop/**` 下的任何文件**；套件的变更必须由人类审阅批准后统一从 SSOT 源推送。
3. 🚫 **禁止在人类工位（`edit`）做批量合并与分支切换**：保护人类正在编辑的工作区；一切并发作业必须在 Worktree 槽位中进行。
4. 🚫 **禁止单侧强制合并**：严禁使用 `--ours`/`--theirs` 抹杀冲突，必须两边保留。
5. 🚫 **禁止假完结与 Stub 糊弄**：严禁未经方案评审私自缩减实现需求，严禁用空方法/TODO 伪装完成勾选 Checkbox。
6. 🚫 **禁止 AI 自作主张偷跑重型审查技能**：带有 `disable-model-invocation: true` 的架构优先（`architecture-first-solution`）与多方评审（`multi-party-design-review`）技能必须由人类主动触发，禁止静默执行。

---

## 仓库目录导航

```text
dev/loop/
├── README.md                      # 本说明文档（开源入口）
├── INDEX.md                       # 套件全局详细文档索引
├── loop-prompt.txt                # 核心启动契约（全项目通用，跨平台唯一入口）
├── workflow.md                    # 单轮 Tick 标准工作流细节与步骤
├── execution-contract.md          # 执行契约 SSOT：MVT 判定、任务源优先级、委派证据
├── human-input.md                 # 人机协作契约：人类输入规范、Sticky 调度不变量
├── worktrees.md                   # Worktree 池管理：人类工位 edit、merge 槽与字母槽 A-J
├── worktree-closeout.md           # 关仓与合入时机转换表（P0~P7）
├── health-gates.md                # 质量门禁通用策略（调用时机、冷却机制、verify-only）
├── models.md                      # 模型能力矩阵与资费授权门禁
├── models-and-delegation.md       # 任务类型与运行时/委派映射
├── orchestration.md               # 编排体系：冲突域隔离与多 Agent 协同
├── porting.md                     # 跨项目移植、升级同步与目录边界规范
│
├── agent-playbooks/               # 子 Agent 角色执行手册库
│   ├── INDEX.md                   # Playbooks 角色索引
│   ├── parent-loop-orchestrator.md# 父调度 Agent 执行规范
│   ├── implementation-agent.md    # 实施 Agent 规范（代码编写与测试）
│   ├── overall-verification-agent.md # 独立总体验收 Agent 规范
│   ├── commit-gate-agent.md       # 提交门禁 Agent 规范
│   ├── plan-roadmap-agent.md      # 方案起草与 Roadmap 拆解 Agent 规范
│   ├── architecture-first-design.md # 架构优先设计与评审规范
│   ├── direction-discovery-agent.md # 探索与方向发现 Agent 规范
│   ├── parallel-loop-waves.md     # 并行波次划分与冲突域矩阵
│   ├── review-question-resolve-loop.md # 争议问题推进循环
│   └── subagent-loop-startup.md   # 子 Agent 启动自检公共规范
│
├── skills/                        # 跨平台 IDE Skills
│   ├── INDEX.md                   # 技能索引与安装指南
│   ├── sync-docs-and-commit/      # 规范收尾、文档同步与原子提交 Skill
│   ├── architecture-first-solution/ # 架构优先方案设计 Skill (人类显式触发)
│   └── multi-party-design-review/ # 多视角设计审查对抗 Skill (人类显式触发)
│
├── scripts/                       # 自动化辅助工具脚本
│   └── install-cursor-skills.sh   # Cursor Skills 一键安装脚本（支持 --personal）
│
├── runtimes/                      # 运行时平台适配指南（Cursor / Claude Code / Qoder 等）
└── cli/                           # 跨栈 CLI 调用指南（Grok / Claude / Codex / OpenCode 等）
```

---

## 开源协议与贡献

本项目采用 [Apache License 2.0](LICENSE) 许可协议开源。

欢迎提交 Issue 与 Pull Request！  
在提交针对 `dev/loop/` 套件的改进时，请务必确保：
- **不引入任何特定项目的专有命令或路径**；
- 保持与其他已有语言/技术栈项目的向下兼容性；
- 遵循现有的三层模型与契约隔离规范。
