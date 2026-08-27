---
title: "Loop 并行 Worktree 收尾"
type: guide
status: accepted
phase: N/A
created: 2026-08-19
updated: 2026-08-27
summary: "关仓编排 + 槽位转换表（何时合入）；无交叉并行本波终态才进 merge；§5 仅无并行兄弟；每冲突域合入 ≤1 次/波次收口。"
---

# Loop 并行 Worktree 收尾

> **几何 / 两边保留 / 禁事项** → [worktrees.md](worktrees.md)（SSOT）。本文只写**关仓编排**。  
> **原则**：先落地已经能合的；再清抽屉；最后全池跟同一棵**已验证**的树。  
> **人类工位 `edit` 不参加本流程**；只通知，禁止代它对齐。  
> **不设新角色**：父 agent 调度；不引入独立 Lifecycle Agent。槽位状态写在 `status.md` / parallel board，与 `git worktree list` 对照。

## 槽位状态（关仓用）

写在 `status.md` 或 parallel board，**禁止**只存在于聊天。释放 / 宣称结束时必须与磁盘一致。

| 状态 | 含义 | 允许的下一步 |
|:-----|:-----|:-------------|
| `idle` | 字母槽干净，HEAD == 最近一次关仓的 `MERGE_SHA`（或新占槽前的 `origin/main`） | 占槽开工 |
| `occupied` | 本波仍有未合入提交或脏树 | P1 收口；禁止 `checkout -B` |
| `merge-queued` | 本槽 tip 已 commit，等待进 merge 槽 | P2 或 P4 串行合入 |
| `blocked` | 不合入 / FAIL；WIP 保留 | 保持占用；升级人类 |
| `parked` | **仅 merge 槽**：在集成分支上、干净、无 `MERGE_HEAD`、HEAD == 已 push 远程集成分支 | 下一波合入前再同步 |

**本波成员**：Wave 2 派出时冻结的槽/slice 集合。存在 `merge-queued` 时 **禁止新占字母槽** 扩大本波。

### 转换表（不变量 1 SSOT · 何时允许合入）

[worktrees.md §5](worktrees.md#5-合并流程字母槽--merge-槽--main) 只写**怎么合**。**何时允许合**只以本表为准。

| From | Event | Guard | To / 动作 | 禁止 |
|:-----|:------|:------|:----------|:-----|
| `occupied` | Wave 4 本地 commit | 本 slice 可合入 | `merge-queued` | 进 merge 槽 / 推集成分支 |
| `occupied` | 不合入 | 书面原因 | `blocked` | `checkout -B` |
| 任一字母槽 `merge-queued` | 本波仍有 `occupied` | — | 保持 queued | §5 或 P2 把单槽合进集成分支 |
| 冻结本波 | 均为 `merge-queued` 或书面 `blocked`（无 `occupied`） | **本 wake**（含后台回报后续轮） | 跑全文 P0–P7 | 写成 Next、等下一轮 `/loop` |
| `idle` | 新占槽 | 无未关仓的 `merge-queued` 本波 | `occupied` | 本波未终态时另开一波 |
| 任意 | 想提前关仓 | **仅人类本 tick 明文**关仓/中止 | P0–P7 | 父 agent「显式关仓」抢跑 |

无并行兄弟（其余字母槽均为 `idle`，或从未开多槽）：日常合入可走 §5，不必全文 P0–P7；**不得**把一次 §5 写成并行 wave 结束。

## 何时跑

| 触发 | 是否跑全文 P0–P7 |
|:-----|:-----------------|
| 转换表：冻结本波无 `occupied`（均为 `merge-queued` 或书面 `blocked`） | **是**（本 wake，不等下一轮 `/loop`） |
| 人类本 tick 明文「并行收尾 / 关仓 / 中止」 | **是** |
| 无并行兄弟的单槽合入 | **否** — 走 [worktrees.md §5](worktrees.md#5-合并流程字母槽--merge-槽--main)（须满足 §5 文首 Guard） |
| 某槽 `blocked` | **否**（该槽）— 其余 queued 仍可按转换表关仓 |

宣称「wave 完成 / 槽已释放 / 并行作业结束」之前，必须跑完本文且 Overall Verification ≠ `FAIL`。

## 不变量

1. **范围有界**：P1 只把**当前在途 slice** 收到可合入提交。不开新 gap、不扩主题。stash 有价值产物同样：变成可合入 commit，或占槽标明未完成 — **不在关仓波开新功能轨**。
2. **并行只到字母槽**：P1 / P3 可多槽并行。**进 merge 槽必须串行**（P2、P4、P5）。**每冲突域每 tick 合入集成线 ≤1 次**（见 [parallel-loop-waves.md](agent-playbooks/parallel-loop-waves.md)）。
3. **字母槽不推 `main`**：关仓期间 `main` 的合入与 push **只在 merge 槽**。日常 Wave 4 只在字母槽本地 commit，见 [parallel-loop-waves.md](agent-playbooks/parallel-loop-waves.md)。
4. **审计 stash ≠ 用 stash 对齐**：禁止为对齐 / 腾工作区而 `stash` / `stash clear`。只处理**已经存在**的 stash。
5. **跟 SHA 不跟飘移的远程**：P5 push 之后钉  
   `MERGE_SHA=$(git -C "$WT_ROOT/merge" rev-parse HEAD)`  
   字母槽对齐 **`$MERGE_SHA`**（merge 槽当时 HEAD），不要各自 `pull origin/main`。
6. **两边保留**：P2 / P4 / P5 凡 merge 一律 [worktrees.md §5.1–5.2](worktrees.md#51-两边保留合并--同步硬不变量)。

## 角色

| 谁 | 做什么 |
|:---|:-------|
| **父 agent** | 调度 P0–P7；串行操作 merge 槽；钉 `MERGE_SHA`；写 status / 通知 `edit`。不在字母槽写 prod。 |
| **各字母槽实施 agent** | P1 收口、P3 stash 分类；本槽 commit。不宣布 wave 完成。 |
| **Overall Verification** | 对照本文检查单独立裁决；不得与实施同一实例。 |
| **Commit Gate** | 各槽 P1/P3 提交前、以及 merge 槽推 `main` 前检查范围与中文 message。 |

不另设「收尾子 agent」角色。

## 阶段

```text
P0 盘点（父）
  → P1 各字母槽并行：在途改动收口并提交
  → P2 merge 槽串行：合入 P1 提交 + 两边保留 + 集成编译
  → P3 各槽并行：stash 审计（有价值→提交；过时→记录后 drop）
  → P4 merge 槽串行：合入 P3 新提交 + 两边保留 + 集成编译
  → P5 merge 槽：合入 main → 编译绿 → push origin
  → P6 merge ff 到该 main；字母槽对齐 MERGE_SHA
  → P7 行动层 + 通知人类工位
```

P2 与 P4 **禁止合成一次大合并**（硬不变量）：stash 考古失败不得绑死已经能上的 P1。合入算法相同，**批次必须分开**。

### P0 — 盘点

在 merge 槽与各占用槽记录（写入 `status.md` 或 parallel board）：

- 占用字母槽、分支 tip、工作区是否脏、`stash list` 条数
- 谁声称可合入 / 谁阻塞
- merge 槽是否干净、是否已对齐 `origin/main`（未对齐则先按 [worktrees.md §2](worktrees.md#2-初始化-merge-槽固定优先于字母槽) 同步，禁止 `reset --hard`）

`edit`：只读 `git status`，**零** merge/pull/rebase。

### P1 — 并行收口提交

每个占用且有在途改动的字母槽：

1. 把当前 slice 做到可合入（聚焦测试按该 slice；文档门禁按主题）。
2. Commit Gate → 本槽 **commit**（中文 message）。**不 push `main`。**
3. 禁止为「先干净再合」而新建 stash。合不了 → 占槽 + status 写阻塞，跳过该槽的 P2。

无脏树、已有 tip 可合入的槽：P1 记 `already-committed`，进入 P2 队列。

### P2 — 合入 merge（串行）

对 P1 队列中每个 tip，在 **merge 槽**：

1. 已对齐最新 `main`。
2. 优先让该字母槽 `rebase`/`merge` 当前 merge 槽 HEAD，减小冲突面。
3. `merge` 或 `cherry-pick` 进 merge 槽；冲突按两边保留消解。
4. `bash scripts/check-merge-both-sides.sh` + 集成编译绿。

失败：该 tip 不进 P5；槽保持占用。已成功合入的其它 tip 可继续。

### P3 — stash 审计（并行）

每槽（含 merge 槽若有 stash）对 `git stash list` **逐条**：

| 分类 | 动作 |
|:-----|:-----|
| **高价值** | 相对当前 HEAD 有独有改动、尚未在 P1/P2 树上、非 secrets / 构建产物 / 重复 diff → `stash apply`（不要 `pop` 直到已 commit）→ 收成可合入 commit → 进 P4 队列 |
| **过时** | 已包含在 HEAD、或纯噪声 → `stash drop` **该条**，status 写原因 |
| **不确定 / 无 message / 像他人 slice** | **不 drop**；占槽或 `HUMAN_DECISION_REQUIRED` |

禁止 `git stash clear`。有价值但本 tick 合不完 → commit 已成型部分或保持 apply 后的工作区并占槽；**禁止**丢回匿名 stash 当长期工位。

### P4 — 再合 merge（串行）

同 P2，仅处理 P3 新提交。无 P3 产物则记 `skipped-no-stash-commits`。

### P5 — merge → main → push

仅 merge 槽：

1. 将 merge 槽当前集成结果合入 / ff 到 `main`（与 [worktrees.md §5](worktrees.md#5-合并流程字母槽--merge-槽--main) 一致）。
2. 两边保留（若产生 merge commit）+ 集成编译全绿。
3. **从此槽** `git push origin main`。构建红 → 不 push，status 记原因。

禁止回到主工作区做本步。

### P6 — cascade 对齐

```bash
# merge 槽停车：与已 push 的 main 同一 SHA（ff-only）
cd "$WT_ROOT/merge"
git fetch origin
git merge --ff-only origin/main
MERGE_SHA="$(git rev-parse HEAD)"

# 字母槽跟 MERGE_SHA — 不要跟「现在的 origin/main」另拉一次
```

| 槽位状态 | 动作 |
|:---------|:-----|
| 已合入、工作区干净、本波释放 | `git checkout -B loop/<字母> "$MERGE_SHA"`；status 记 `idle`。目录不拆。 |
| 仍占用（未合入或 P3 留活） | 有未提交改动则先本 slice commit；再 `git merge "$MERGE_SHA"`。**禁止** `checkout -B`。 |
| merge 槽 | 停在 `main`（或与 `main` 同 SHA）、干净、无 `MERGE_HEAD` |
| `edit` | **不执行**；P7 通知 |

短周期 `.worktrees/<名>/`：已合入后可 `git worktree remove`（池内字母槽禁止常规拆除）。

### P7 — 行动层与人类工位

- `status.md` 槽位表与 `git worktree list` 一致（idle / 占用+原因）。
- 本波 parallel board 勾完或 `active/` → `archive/`。看板仍 active 但 P5 已 push → 收尾 **FAIL**。
- roadmap / deferred-gaps 与实际合入对齐。
- Final Output 写：`main` 已到 `<MERGE_SHA>`；人类工位请自行确认后对齐。**loop 代 `edit` merge/pull → FAIL。**

## Overall Verification（关仓）

除常规完成度外，关仓 tick 必须核对：

- [ ] P1 范围无新主题；未合入槽有书面阻塞
- [ ] `main` 由 merge 槽 push；字母槽无直推 `main`
- [ ] stash：无 `clear`；drop 均有原因；不确定条仍在
- [ ] `MERGE_SHA` 已记录；merge 槽 HEAD == 已 push `origin/main`
- [ ] 释放槽干净且在 `$MERGE_SHA`；占用槽未 `checkout -B`
- [ ] 人类已通知；未改 `edit` 上的同步类 git
- [ ] 槽表 / 看板 / status 与磁盘一致（`idle` / `occupied` / `merge-queued` / `blocked` / merge=`parked`）

任一项失败 → 不得宣称 wave 完成。

## 与日常 wave 划界

| | 日常实施 | 本文关仓 |
|:--|:---------|:---------|
| Wave 4 | 字母槽 **本地 commit**；不推集成分支 | — |
| 合入集成分支 + push | **仅**无并行兄弟且 §5 Guard 成立 | **P5 独占**（本波终态，本 wake） |
| stash | 禁止用 stash 对齐 | P3 **只审计已有** stash |

## 违规（补充 [worktrees.md](worktrees.md)）

| 违规 | 裁决 |
|:-----|:-----|
| 宣称 wave 完成但未跑 P0–P7 | **FAIL** |
| 关仓中字母槽直推 `main` | **FAIL** |
| 为对齐新建 stash / `stash clear` | **FAIL** |
| 字母槽跟 `origin/main` 而不跟 `MERGE_SHA` | **FAIL**（与已验证树脱钩） |
| 在 `edit` 上代人类 cascade | **FAIL** |
| 本波仍有 `occupied` 却单槽合入集成分支 / 宣称 wave 完成 | **FAIL** |
| 有未关仓 `merge-queued` 时新占字母槽扩波 | **FAIL** |

## 架构审查

- **审查**：Grok CLI `grok-4.6`（`num_turns=3`）**Approve with changes**（2026-08-19）。
- **并入**：上表槽位状态；P2/P4 分批升为硬不变量；`edit` 零 cascade。
- **并入（2026-08-27）**：转换表为合入时机 SSOT；删父显式关仓；本 wake 关仓。调度优先级见 [execution-contract.md](execution-contract.md)，本文不复制。
- **拒绝（会推翻已选设计或膨胀套件）**：独立 WorktreeLifecycle Agent；合并 P2/P4；字母槽关仓强制 `worktree remove`（池要复用）；本批新增 `check-worktree-lifecycle.sh` / 新 ADR。

## 相关

- [worktrees.md](worktrees.md) — 池、§5 日常合入、两边保留  
- [parallel-loop-waves.md](agent-playbooks/parallel-loop-waves.md) — Wave 4 本地 commit  
- [orchestration.md](orchestration.md) — 父 agent 调度  
- [overall-verification-agent.md](agent-playbooks/overall-verification-agent.md)  
