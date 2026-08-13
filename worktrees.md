---
title: "Loop 并行 Worktree"
type: guide
status: accepted
phase: N/A
updated: 2026-08-12
summary: "主工作区=人类工位（常驻 edit 分支，同步类 git 命令须人类确认）+ A–G + merge；集成基线在 merge 槽；合入真三路两边保留；对齐 main 仅用 git（禁 rsync）且用 merge --ff-only（禁 reset --hard）；合入前 commit、禁 restore/stash 丢 WIP。"
---

# Loop 并行 Worktree

> **关联**：[orchestration.md](orchestration.md) · [parallel-loop-waves.md](agent-playbooks/parallel-loop-waves.md)  
> **原则**：worktree = **复用型工位**；多槽位 ≠ 必须同时跑多个 agent。  
> **项目专属**：集成编译命令写在各仓库 `dev/progress/health-gates.md` 或 `AGENTS.md`；**不在本文**列项目特例。

## 槽位分工（核心）

| 类型 | 路径 | 是否固定语义 | 用途 |
|:-----|:-----|:-------------|:-----|
| **主工作区（人类工位）** | 仓库根，常驻 **`edit`** 分支 | **是** | 人类做分析、写文档、调试；人机协作会话默认在此。**loop 并行作业不得占用** |
| **合并槽** | `$WT_ROOT/merge` | **是** — 全文唯一固定职责槽 | 合并字母槽（及其他来源）的提交；**须随时对齐 `main`** |
| **字母槽** | `$WT_ROOT/A` … `$WT_ROOT/G` | 否 — 与模块/roadmap **无关** | 并行 slice 编码；父 agent 按空闲槽分配，用完可复用 |
| **短周期 slice** | `.worktrees/<名>/`（gitignore） | 否 | 单 parallel board 内 ≤3 coder，用完可拆 |

**规则**：

- **`edit`** 与 **`merge`** 两个名称与职责写死在本文；`A`…`G` **不**绑定模块，当前 slice 归属记在 `status.md` / parallel board。
- 字母槽上的提交**默认不直接 push `main`**；经 **merge 槽**做集成合并与编译验证后再进 `main`。
- **merge 槽须及时同步 `main`**：任一字母槽准备合入前、以及 `main` 在其他路径前进后，merge 槽必须先 `git fetch` 并对齐最新 `origin/main`（`rebase` 或 `merge`，团队统一一种）。

### 人类工位 `edit`（主工作区）

主工作区常驻 `edit` 分支，是人类的固定工位——在这里读代码、写文档、跑调试，工作区里长期带着未提交的在途内容。

| 谁 | 在工位上可以做什么 |
|:--|:--|
| **人类 + 协作中的 agent** | 随意读写文件、`add` / `commit` / `push`、跑构建与测试。**无任何权限打扰** |
| **loop 并行 agent** | 不要来。字母槽与 merge 槽是它们的地盘 |
| **任何人** | 切分支 / `merge` / `rebase` / `reset` / `pull` / `clean` / `stash` **须人类确认**——见下方门禁 |

**为什么单独立规矩**：loop 并行时最频繁的动作就是「对齐 `main`」和「合入字母槽」。这些命令一旦落到工位上，会把人正在写的东西冲掉，而且已跟踪文件的修改被覆盖后**不进 reflog、找不回来**（§6.1 有实证）。`edit` 这个名字本身就是给 agent 的信号：这不是集成基线，别在这里做同步。

**机器门禁**（参考实现 [`.cursor/hooks/guard-shell.py`](../../.cursor/hooks/guard-shell.py)，各仓库按自己的 hook 机制落地）：在 `beforeShellExecution` 上判定——**目标仓库检出在 `edit`** 时，同步/切换类 git 命令返回 `ask` 转人工确认；`status` / `log` / `diff` / `add` / `commit` / `push` / `worktree` 与构建命令一律放行。

两个实现要点：

- 判定看**目标仓库的分支**，不是会话 cwd——事故形态是 `cd <主工作区> && git merge ...`，只看 cwd 会漏。
- 工位上**无条件 ask**，不要因为「树是干净的」就放行：干净只说明此刻没东西丢，不代表这次切分支是人要的。

字母槽与 merge 槽不受此闸门影响，那里照常按「有无实际损失」判丢弃类命令。

**集成基线在哪**：不再是主工作区，而是 `$WT_ROOT/merge`。字母槽 → merge 槽 → `main` 的流程（§5）不变，只是最后一步的复跑与 push 也在 merge 槽做，不回主工作区。

## 两条泳道（开发与验证解耦）

| 泳道 | 职责 | 是否阻塞其他泳道 |
|:-----|:-----|:-----------------|
| **开发泳道** | 字母槽编码、stub、新 slice | 否 |
| **验证泳道** | 长测、烟测、回归、记 gap | 否（并行进行） |

- 单条验收 FAIL **不冻结**其他 slice；FAIL 须写入 `deferred-gaps.md` / status。
- 验证 FAIL **不等于**开发停工；但**红基线**不得占用新字母槽或宣称 PASS。

## 目录约定

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
WT_ROOT="$(dirname "$REPO_ROOT")/$(basename "$REPO_ROOT")-WorkTrees"
# 例：/path/MyRepo → /path/MyRepo-WorkTrees/
```

| 项 | 规则 |
|----|------|
| **根路径** | 上式公式；所有池内 worktree **必须**在 `$WT_ROOT/` 下 |
| **复用** | 槽位长期保留；禁止 `../Repo-feat-*`、`.claude/worktrees/*` 等 ad-hoc 路径 |
| **主仓库** | 保留 `main` 集成基线 |
| **远程分支** | worktree **禁止**创建远程分支；合入 `main` 后按各仓库 `AGENTS.md` push |
| **上限** | **1** merge + **7** 字母槽（`A`…`G`）+ 主工作区 = 最多 **9** 检出；禁止第 8 个字母槽或第二个 merge |

## 硬门禁：创建 worktree 前基线须绿

在 `git worktree add` **之前**，基线提交（通常 `main` HEAD）必须满足：

1. 主仓库工作区干净（`git status --porcelain` 为空）；
2. 位于集成分支（通常 `main`）；
3. 该仓库**集成编译命令** exit code = 0（见 `dev/progress/health-gates.md` 或 `AGENTS.md`）；
4. （建议）`dev/progress/status.md` 与当前 `main` HEAD 对齐。

**基线未绿时禁止**：占用字母槽并宣称并行开发已启动。仅允许在 merge 槽（若已存在且仅用于修编译）修基线。

合并进 `main` 后，**必须**在 merge 槽复跑集成编译全绿，才允许基于新 HEAD 占用下一批字母槽。

## Worktree 池：初始化、先查后建

> **Agent 义务**：需要 worktree 时，**不得**因 `WT_ROOT` 不存在而跳过；须 `mkdir -p` 并按本节复用固定路径。

### 1. 初始化根目录（仅建根）

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
WT_ROOT="$(dirname "$REPO_ROOT")/$(basename "$REPO_ROOT")-WorkTrees"
mkdir -p "$WT_ROOT"
```

只创建**空根目录**；`merge` 与字母槽在过门禁后按需 `add`。

### 2. 初始化 merge 槽（固定，优先于字母槽）

合并轨专用；**全仓只此一个**：

```bash
cd "$REPO_ROOT"
# merge 未注册时（先过基线绿门禁）：
git worktree add "$WT_ROOT/merge" main
# 或：git worktree add "$WT_ROOT/merge" -b loop/merge main
```

**merge 槽同步 `main`（必做，且须及时）**：

```bash
cd "$WT_ROOT/merge"
git fetch origin
git checkout main
git pull --rebase origin main    # 或 merge，与团队约定一致
# 集成编译绿后再合并其他槽的提交
```

触发同步的时机（**任一即须执行**）：

| 时机 | 说明 |
|:-----|:-----|
| 准备合入任一字母槽的提交前 | merge 槽必须先对齐最新 `main` |
| `main` 在主工作区或其他路径有新提交后 | merge 槽在下一合并操作前必须 fetch + 对齐 |
| 合并产生冲突后 | 在 merge 槽解决；不得让字母槽长期漂移 `main` |

### 3. 字母槽 `A` … `G`

- 路径 `$WT_ROOT/<字母>`，分支 `loop/<字母>`（与模块无关）。
- 父 agent 在 status / parallel board 记录「槽 X → slice Y」；slice 结束释放槽位给下一任务复用。
- **禁止** `git worktree remove` 常规拆除字母槽；保持目录，下轮 `rebase main` 或 `checkout -B` 复用。

### 4. 先查后建（任何 `add` 之前必做）

```bash
git worktree list
ls -la "$WT_ROOT" 2>/dev/null || true
```

决策顺序：

| # | 条件 | 动作 |
|:--|:-----|:-----|
| 1 | 目标路径**已注册**且工作区干净 | **复用** → fetch → 对齐 `main` → 集成编译绿 → 编码或合并 |
| 2 | 已注册、有 WIP | commit / stash（stash 须用户确认）或换空闲字母槽 |
| 3 | 目录在、未注册 | `git worktree prune` 后，对**同一路径**重新 `add` |
| 4 | 未注册、未达上限、基线绿 | `git worktree add "$WT_ROOT/<槽>" …` |
| 5 | 字母槽全占用 | **FAIL** — 先合并收尾或复用，禁止池外路径 |

字母槽开工前：

```bash
cd "$WT_ROOT/<字母>"
git fetch origin
git checkout -B loop/<字母> origin/main
# 集成编译绿后再编码
```

### 5. 合并流程（字母槽 → merge 槽 → main）

```text
loop/A ──┐
loop/B ──┼──→  merge 槽（对齐 main）──→ main ──→ 集成编译绿
loop/C ──┘              ↑
                   随时 fetch + 对齐 main
```

1. **merge 槽**先同步 `main`（§2）。优先让字母槽先 `rebase origin/main`，再合入 merge 槽，减小冲突面。
2. 将字母槽分支合入 merge 槽（`merge` / `cherry-pick`，团队统一）；**冲突消解必须遵守 §5.1 两边保留**。
3. 跑 **两边保留门禁**（§5.2）+ 相关 `*ContentOnly*` / `*ArchTest*`（若有）+ merge 槽集成编译绿。
4. 在 merge 槽 push 前 rebase 到 `main`，由 merge 槽推 `main`。**不要**绕回主工作区做这一步——那是人类工位。
5. merge 槽复跑集成编译；字母槽 `rebase main` 后继续或释放。

同 tick 并行实施仍受 [parallel-loop-waves](agent-playbooks/parallel-loop-waves.md) **≤3 slice** 与文件冲突矩阵约束。

### 5.1 两边保留（合并 / 同步硬不变量）

> **实证**：`94c1fe639`（`sync origin/main into loop/merge` · 口号「keep both」）曾整文件取对侧，丢掉 loop 侧 `DeepThinkBlock` content-only，并带回已删除的旧 UI 块。历史里仍有修复 commit，**树内容已丢**。

**「两边保留」的唯一定义**：相对 `merge-base(ours, theirs)` —

| 情况 | 结果必须 |
|:-----|:---------|
| **仅 ours** 相对 base 有改 | 保留 **ours**（禁止用 theirs 整文件盖掉） |
| **仅 theirs** 相对 base 有改 | 保留 **theirs**（禁止用 ours 整文件盖掉） |
| **两侧都有改** | **真三路合并**：冲突标记逐段消解，**两侧意图都进结果**；结果 **不得** 整文件 ≡ ours 或 ≡ theirs |

**禁止**：

- `git checkout --ours/--theirs -- <path>` **整文件**选边（单文件确认对侧完全无独有改动除外，须在 status 写明）
- `git merge -X ours` / `-X theirs` 作为默认策略
- 提交说明写「keep both」但未做三路合并、也未跑 §5.2 门禁
- 把「并排留下两份旧+新实现」当成 keep both（会制造重复控件 / 死代码；那是失败的合并）

**允许**：对无冲突的路径由 git 自动合并；仅对冲突 hunk 人工合成；合成后用 §5.2 脚本验证。

同步 `main` 进 merge 槽（§2）与合入字母槽，**同一套不变量**。

### 5.2 两边保留门禁（合并完成后、宣称合入成功前）

在 **merge 结果提交**（或未提交的 merge 工作区）上，对刚合并的两父（`HEAD^1` / `HEAD^2`，或显式传入）跑：

```bash
# 仓库根；MERGE_RESULT 默认 HEAD（须为二父母 merge commit）或当前 index
bash scripts/check-merge-both-sides.sh
# 或：bash scripts/check-merge-both-sides.sh <merge-commit>
# 或：bash scripts/check-merge-both-sides.sh <ours> <theirs> <result>
```

脚本对每个相对 base 有改的路径检查：

1. 仅一侧改动 → result 不得等于对侧整文件  
2. 两侧都改 → result 不得整文件等于任一侧（须为合成）

失败 → **FAIL**：不得 push `main`、不得勾合入完成、不得宣称 Overall Verification PASS。  
另跑与冲突文件相关的架构/内容不变量测试（例：`DeepThinkBlockContentOnlyArchTest`）。

### 6. Git 同步（按需）

> **术语**：本文「同步 / 对齐 main / 同步 worktree」**一律指 git**，**禁止**用 `rsync` 复制仓库或 worktree 目录来对齐 HEAD（`rsync` 仅用于 [porting.md](porting.md) 的 `dev/loop/` **套件**跨仓库复制，与 worktree 无关）。

| 时机 | 操作 |
|:-----|:-----|
| 占槽 / 复用槽开工前 | `git fetch`；基于最新 `main`（或 `origin/main`，见 §6.1） |
| **merge 槽** | 见 §2 — 比其他槽更频繁对齐 `main` |
| `main` 在其他路径前进后 | 各字母槽 **git merge/rebase** `main` HEAD（§6.1）；**禁 rsync** |
| `git push` 被拒 | `git pull --rebase origin main` → 集成编译复绿 → 再 push |
| 其他 loop tick | 不主动 pull |

**禁止** force push 默认分支。

#### 6.1 `main` 前进后 → 各槽对齐（不丢修改）

| 槽位状态 | 动作 |
|:---------|:-----|
| **有未提交 WIP** | **先 commit**（本 slice 范围）；**禁止**为对齐而 `reset --hard` / `checkout --` / `restore` / `stash` / `clean` |
| **已提交、工作区干净** | `git merge <main-HEAD>` 或 `git rebase <main-HEAD>`（团队统一一种） |
| **merge 槽** | 必须先对齐 `main`，再合字母槽提交（§2） |

> **对齐一律用会失败的命令，不用会静默销毁的命令。**「与 `origin/main` 一致」应写成 `git merge --ff-only origin/main`：本地有未 push 提交或脏树时它**报错退出**，让你看见并处理。`git reset --hard origin/main` 表达的是「无论本地有什么都抹掉」——它丢弃的**已跟踪文件修改不进 reflog，无法找回**，且会连同其他会话尚未 push 的提交一起消失。
>
> **实证（2026-08-12）**：merge 编排在**主工作区**（非 `$WT_ROOT/merge`）执行 `cd <主工作区> && git reset --hard origin/main && git merge --no-ff <槽 tip>`，抹掉了另一会话刚提交未 push 的性能审查报告（经 reflog cherry-pick 找回），并永久销毁了第三个会话对 3 个已跟踪文件约 145 行的未提交改动。该命令旁附的注释只校验了未跟踪 junk 文件仍在——**风险模型漏掉了已跟踪文件的 WIP 与他人的本地提交**。机器门禁见 `.cursor/hooks/guard-shell.py`（仅在确有未 push 提交 / 脏树 / 未跟踪文件时拒绝，干净仓放行）。

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
MAIN_HEAD="$(git -C "$REPO_ROOT" rev-parse main)"
cd "$WT_ROOT/<槽>"
# 未提交改动须先 commit；禁止 rsync；禁止 restore/stash 他人或未纳入 slice 的 WIP
git merge "$MAIN_HEAD" --no-edit   # 或：git rebase "$MAIN_HEAD"
```

- **本地 `main` 领先 `origin/main`**（未 push）：用 **`git rev-parse main`**（上式），**不要**只 `pull origin/main` 而漏掉本地 commit。  
- **`git checkout -B loop/<字母> origin/main`**：仅当**旧 slice 已合入、槽释放复用**时可用；**禁止**在有未合入提交或脏工作区时用此命令「对齐」（会丢 work）。

#### 6.2 merge 槽 → `main` 后 → 其余槽 follow

`main` 在 merge 槽或主工作区前进后，其余字母槽在下一编码前须执行 §6.1（git merge/rebase `main` HEAD），**不得** rsync、**不得**用文件复制冒充同步。

## 短周期 `.worktrees/` slice

用于单次 parallel board，**不**替代 `$WT_ROOT` 池：

```bash
mkdir -p .worktrees
git worktree add .worktrees/<slice名> -b feat/<topic> HEAD
```

- 基于 feature 分支**已提交** HEAD；每 coder **独占**文件集  
- 合并后经 merge 槽进 `main`；完成后可 `git worktree remove`

## Agent 角色检查清单

### 父 agent

- [ ] 集成编译已绿（记录命令与 exit code）
- [ ] `git worktree list` + `ls "$WT_ROOT"`；无根则 `mkdir -p`
- [ ] **merge 槽**存在；合入前已同步 `main`
- [ ] 字母槽用空闲 `A`…`G`；禁止池外路径或超上限
- [ ] 开发 / 验证分派到不同槽或子 agent（若并行）
- [ ] 合并/同步后跑 §5.2 `check-merge-both-sides.sh`；冲突按 §5.1 真三路合并

### 实施 agent

- [ ] 已读本文 + [subagent-loop-startup.md](agent-playbooks/subagent-loop-startup.md)
- [ ] 无编译门禁证据 → **拒绝开工**
- [ ] 仅使用 `$WT_ROOT/merge` 或 `$WT_ROOT/{A..G}` 或 `.worktrees/`
- [ ] 输出附集成编译结果
- [ ] 工作区保护：**禁止** `git checkout --` / `git restore` / `git stash` / `git clean` 回退、覆盖或暂存任何已有改动（含其他 Agent / 开发者未提交的在途修改）；只新增或编辑本任务需要的文件与代码行（见 [AGENTS.md §并行开发](../../AGENTS.md#并行开发agent-强制)）

### Overall Verification agent

- [ ] 验收基于集成编译全绿的提交
- [ ] merge 槽若落后于 `main` 仍宣称合入完成 → **FAIL**
- [ ] 本轮含 merge/同步 → `check-merge-both-sides.sh` 必须 PASS；口号「keep both」而无门禁证据 → **FAIL**

## 违规处理

| 违规 | 裁决 |
|:-----|:-----|
| 基线未绿占用字母槽 | **FAIL**，优先修编译 |
| 池外或 ad-hoc 路径 `add` | **FAIL**，改用固定路径 |
| 字母槽满仍 `add` 或未复用 | **FAIL** |
| 未经 merge 槽（或团队约定路径）直接推字母槽到 `main` | **FAIL** |
| 用 `rsync` / 文件复制对齐 worktree 或 `main` | **FAIL** — 须 git merge/rebase（§6） |
| 为对齐 `main` 而 `reset --hard` / `restore` / `stash` / `clean` 丢弃 WIP | **FAIL** — 须先 commit 本 slice；对齐用 `git merge --ff-only origin/main`（§6.1） |
| 回退 / 覆盖 / 暂存他人未提交改动（`git reset --hard`、`git checkout --`、`git restore`、`git stash`、`git clean`） | **FAIL**，须恢复被回退的改动并复验 |
| 在**主工作区**（而非 `$WT_ROOT/merge`）执行 merge 槽的对齐与合并 | **FAIL** — 主工作区是人类工位（`edit`），承载在途改动，见 §人类工位 与 §6.1 实证 |
| loop 并行 slice 占用主工作区，或把主工作区切离 `edit` 分支 | **FAIL** |
| merge 槽未对齐 `main` 即合并 | **FAIL** |
| 合并后未复跑集成编译 | **PARTIAL**，阻塞下一批槽位 |
| 整文件 `--ours`/`--theirs` 或 `-X ours/theirs` 丢掉对侧独有改动 | **FAIL**，按 §5.1 重做合并 |
| 「keep both」未跑 §5.2 / 结果整文件等于单侧 | **FAIL** |
| 历史有修复 commit、树内容被后续 merge 盖回旧实现 | **FAIL**（回归）；登记 deferred-gap，不得勾完成 |

## 相关

- [human-input.md](human-input.md) — 人类只给方向  
- [health-gates.md](health-gates.md) — gate 策略；具体命令在各仓库 `dev/progress/health-gates.md`  
- [orchestration.md](orchestration.md) — 并行 wave 与隔离测试  
- [`scripts/check-merge-both-sides.sh`](../../scripts/check-merge-both-sides.sh) — 两边保留机器门禁  
- [AGENTS.md §禁止行为](../../AGENTS.md#禁止行为) — 合并/同步前核对范围  
