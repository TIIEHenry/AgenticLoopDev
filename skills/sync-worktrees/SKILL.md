---
name: sync-worktrees
description: >-
  Merges unique commits from the current workspace and every git worktree into
  the merge/integration slot, then fast-forwards all station branches to that
  SHA, while leaving each station's uncommitted files on that station's disk.
  Never reset, stash, restore, or commit WIP just to sync. Use when the user
  asks to 合并当前工作区和所有的worktree的修改、保留各自未提交的内容、
  合并 worktree、同步工位、同步分支、cascade、关仓对齐、把各槽和人类工位的提交合在一起、
  merge all worktrees, or to sync worktrees without losing WIP.
title: "Skill: sync-worktrees"
type: guide
status: accepted
phase: N/A
updated: 2026-09-19
summary: "Merge unique commits from the current workspace and all worktrees; keep each station's uncommitted files on disk."
---

# sync-worktrees

把**当前工作区（人类工位）+ 所有已注册 worktree** 里已经存在的提交合进集成槽，再让各工位分支跟到同一个 SHA。

**保留各自未提交的内容**：人类主工作区、merge 槽、字母槽、其它 worktree，未提交文件必须仍在**该工位磁盘上**。不能靠「已经写进某个 commit」交差。默认**不 push**。

脚本在本技能 `scripts/`。先解析路径再跑：

```bash
REPO="$(git rev-parse --show-toplevel)"
SCRIPT="$REPO/dev/loop/skills/sync-worktrees/scripts/sync_worktrees.py"
[[ -f "$SCRIPT" ]] || SCRIPT="$HOME/.cursor/skills/sync-worktrees/scripts/sync_worktrees.py"
python3 "$SCRIPT" inventory --json > /tmp/sync-worktrees-snap.json
python3 "$SCRIPT" inventory
python3 "$SCRIPT" plan
```

合入完成后：

```bash
python3 "$SCRIPT" cascade "$MERGE_SHA"
python3 "$SCRIPT" verify --snapshot /tmp/sync-worktrees-snap.json --expect-sha "$MERGE_SHA"
```

`cascade` 对**每个**工位只执行 `git merge --ff-only`。把各 tip 合进 merge 槽由你按 `plan` 做。

## 硬禁令

禁止用这些「对齐 / 腾干净」：`reset --hard` / `reset --keep` / `checkout --` / `checkout -B`（**任何工位**）/ `restore` / `stash` / `clean` / `merge -X ours|theirs` / 整文件 `checkout --ours|--theirs` / 用 rsync 复制 worktree。

禁止为同步而 `commit` 任何工位的 WIP。只合**已经存在的 commit**。未提交 hunk 不进 `MERGE_SHA`，结束后仍是该工位的本地修改。

对齐一律用**会失败的命令**。失败就停，该工位工作区原样留着。不要换 reset/stash 重试。

## 工位

| 角色 | 怎么认 | 已有 commit | 未提交修改 |
|:-----|:-------|:------------|:-----------|
| **human** | `git worktree list` 第一行（当前主工作区） | 合入该分支 HEAD | 留在该工作区 |
| **merge** | 路径名 `merge` 或分支 `loop/merge` | 合入发生在这里 | 留在工作区；合 tip 时不要 `git add -A` |
| **letter / other** | 其余已注册 worktree | 合入其 HEAD | 留在**该** worktree 工作区 |

没有 merge 槽：按 `plan` 的 `git worktree add` 建 `$WT_ROOT/merge`，**不要**在人类工位里做合入。

仓库若有 `dev/loop/worktrees.md`：冲突按「两边保留」。用户说了关仓且有 `dev/loop/worktree-closeout.md` 才从 merge 槽 push `main`。本技能默认只做本地合入 + 本地 cascade。

脏树要对齐 `main` 时，`worktrees.md` §6.1 要求先 commit 再 merge——那是**单槽开工对齐**，不是本技能。本技能是收集各工位已有提交，且**不**把未提交收成 commit。

## 流程

```
Sync-Worktrees:
- [ ] 1. inventory 快照（每个工位的脏 blob）
- [ ] 2. 任何工位都不要为同步去 commit / stash
- [ ] 3. fetch；在 merge 槽用 git merge（禁止 rebase）依次合 tips
- [ ] 4. 钉 MERGE_SHA；cascade --ff-only 到每一个工位
- [ ] 5. verify：每个工位快照脏内容仍在磁盘上
```

### 1. 盘点

在**任意**已注册 checkout 里跑 `inventory`。记下**每个**工位的分支、HEAD、脏路径。只读，不 merge。

### 2. 脏树原样留着

不把 WIP 收成 commit。人类脏、字母槽脏、merge 槽脏，都带着做后面的 merge / ff-only。

### 3. 在 merge 槽合入

`plan` 里的 tip 已按 HEAD 去重。顺序：先 `origin/main`（若有独有提交），再独有提交少的工位。

每条都在 merge 槽：

```bash
git -C "$MERGE" merge --no-edit "$TIP"
```

必须用 **merge 不是 rebase**：源 HEAD 必须仍是结果的祖先，后面 ff-only 才能带着各工位脏树走。

merge 槽自己有未提交修改时：照样 `merge`；git 因重叠脏路径拒绝 → 停，**不要** stash/commit 腾干净。产生 merge commit 时只 add 冲突/合并路径，禁止 `git add -A` / `git add .`。

冲突：**真三路**，相对 merge-base 两侧意图都进结果。禁止整文件选边。若有 `scripts/check-merge-both-sides.sh`，合完就跑。解不了：停在冲突状态或 `merge --abort`（仅 merge 槽、尚未动其它工位时），该 tip 留在原分支，其余 tip 可继续。

### 4. Cascade

```bash
MERGE_SHA="$(git -C "$MERGE" rev-parse HEAD)"
python3 "$SCRIPT" cascade "$MERGE_SHA"
```

每个工位（含人类、字母槽、merge）都留在原分支，只 ff-only。脚本对「HEAD 不是 MERGE_SHA 祖先」或「脏路径与进站文件重叠」会 **FAIL 并原样留下**。不要对干净字母槽 `checkout -B` 来「跟 SHA」。

### 5. 验收

`verify` 必须确认：

- 能 ff 的工位 HEAD == `$MERGE_SHA`；不能 ff 的有书面原因，且该工位相对快照未丢内容
- 快照里**每一个工位**的脏 blob 仍在**该工位磁盘上**（内容哈希不变）。「已经在 HEAD 里」不算保住未提交修改
- 未对任何工位 `checkout -B` / `reset` / `stash` / `restore` / `clean`

然后用几行报告：合进了哪些 tip、`MERGE_SHA`、谁 ff 成功、谁跳过、**各工位**脏文件是否还在。

## 与关仓的界限

本技能 = **本地**收集已有提交 + 同步分支 + **所有工位保 WIP**。不是 Loop P0–P7 全文：不改 `status.md`、不默认 push、不 commit 各槽在途改动、不动已有 stash（只在 inventory 里报条数）。用户明确说关仓 / 推 `main` 时，再读 `dev/loop/worktree-closeout.md`。

## 触发例子

- 「合并当前工作区和所有的 worktree 的修改，但是保留各自未提交的内容」
- 「把所有 worktree 和人类工位的提交合到一起，同步分支，别丢改动」
- 「cascade 各槽到同一 SHA」
- `/sync-worktrees`
