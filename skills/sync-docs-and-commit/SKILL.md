---
name: sync-docs-and-commit
description: >-
  Close out implementation work by syncing necessary design/spec docs, updating
  plan document status when a plan was followed, refreshing action-layer progress
  when the repo has one, then creating a scoped git commit that includes all
  theme-related paths together. Portable across projects. Use when finishing a
  task, closing a session, the user asks to sync docs and commit, update plan
  status and commit, or run a documentation gate before commit.
---

# Sync Docs and Commit

**跨项目通用。** 实施收尾：按需同步设计文档 → 更新方案状态（若有）→ 更新行动层（若有）→ **本次主题相关改动一并暂存并提交**。

本 skill 被调用即视为用户授权完成本主题 commit；**默认不 push**，除非用户另行要求。遵守用户 git 安全协议；若仓库另有文档规范，一并遵守。

## When to apply

- 功能/修复实施完成，准备收尾
- 用户说：同步文档并提交、更新方案状态、commit 前文档门禁、收尾提交
- 刚做完有对应方案文档的实现

## Workflow

```
Sync-Docs-Commit Progress:
- [ ] 1. Scope the theme (Included / Excluded)
- [ ] 2. Sync design docs (if necessary)
- [ ] 3. Update plan status (if a plan was used)
- [ ] 4. Update action layer (if the repo has one)
- [ ] 5. Commit (all Included paths together)
- [ ] 6. Verify git status
```

### 1. Scope the theme

并行跑：`git status` · `git diff` · `git diff --cached` · `git log -5 --oneline`

| Included（本次主题 — **一并提交**） | Excluded（明确的其他主题 WIP） |
|:-------------------------------------|:-------------------------------|
| 实现代码、测试、本主题新文件 | 与本主题无关的路径 |
| 本主题跟进的 plan / ADR / review | 其他功能的 WIP 文件 |
| 本主题同步过的设计/规格 doc | |
| 行动层（若有） | |

**一并提交（硬规则）**：凡判定为本次主题的路径，**同一 commit 全部 `git add`**——代码 + 测试 + plan + 设计文档 + 行动层 **不拆成多次 commit**，也不先交代码、文档「下次再补」。

**同文件既有本主题又有其他 WIP**：

1. 默认：**整文件进 Included 一并提交**。
2. 仅当附带改动明显是另一大主题且体积/风险大 → **停止**（`HUMAN_DECISION_REQUIRED`）。
3. **禁止**为摘 hunk 而半文件提交，除非用户明确要求拆分。

**Trivial 例外**：单行 typo / 纯测试断言 / 无行为变化 → 可跳过步骤 2–4，直接步骤 5；须标注 trivial。

### 2. Sync design docs — if necessary

先看仓库实际文档布局（`docs/`、`*/docs/`、`AGENTS.md` 导航），**不要假设**固定 monorepo 结构。

| 变更性质 | 动作 |
|:---------|:-----|
| 用户可见行为 / UX / 对外接口 / 降级策略变了 | 更新对应设计/规格文档（通常 1–2 份） |
| 工具 / 协议 / 跨模块契约 | 更新相关 INDEX 或协议 doc；必要时 ADR（另轨） |
| 仅内部 refactor / 命名 / 测试 | **通常不必**改设计文档 |
| 文档目录新增/移动 | 更新相关 INDEX；若项目有文档健康检查则跑之 |
| 无行为/契约变化 | 跳过；收尾写「无需同步设计文档」 |

带 frontmatter 的 `.md`：更新 `updated: YYYY-MM-DD`（今天）。无 frontmatter → 不硬加。

本步改出的文件 **并入 Included**，与代码同 commit。

**禁止**：为「显得完整」而改无关 spec；过时文档只迁 archive（若项目有此约定），不删除。

### 3. Update plan status — if a plan was used

若本轮跟随了明确方案路径（常见：`dev/plans/`、`docs/plans/`、ADR 目录——**以仓库实际为准**）：

1. 勾选已完成项  
2. 对齐 frontmatter `status`（若有：完成 → `implemented`/`completed`；部分 → `in_progress`/`partially_completed`）  
3. 更新 `updated`  
4. 同步看板/roadmap 对应项（**仅当仓库存在**）  

无方案 → 跳过，收尾写「无方案文档」。方案与实施宜分 commit。本步改动并入 Included。

### 4. Action layer（有则更新，无则跳过）

**探测**（存在才做，路径名因项目而异）：

| 常见约定（Loop 移植项目） | 其他项目 |
|:--------------------------|:---------|
| `dev/progress/status.md` | 根 `CHANGELOG` / `PROGRESS.md` / 无行动层 |
| `dev/roadmap/active/` | GitHub Issues / 无 roadmap |
| `dev/parallel/active/` | 无则跳过 |

非 trivial 且存在行动层时：

- [ ] 写入 Completed / Current Session 摘要  
- [ ] 保持进度文件简短（若项目有行数上限则遵守）  
- [ ] 勾选本轮对应 checkbox（若有）  
- [ ] 对齐本次 plan/spec 的 `updated` / `status`  

本步改动并入 Included。**无行动层** → 只做 scope + 按需 docs + commit，收尾注明「无行动层」。

### 5. Commit

1. 再确认 `git status` / `diff` / `log`  
2. **一次** `git add` **全部** Included（相关文件一并）— **禁止**漏同主题 docs/plan/status；**禁止**有明确 Excluded 时 `git add -A` / `git add .`  
3. **禁止**对 Excluded 做 `restore` / `stash` / `reset` / `checkout`  
4. 1–2 句 message（why 优先；对齐近期 log）  
5. HEREDOC 提交；hook 失败则修复后**新建** commit  
6. **不要 push**，除非用户明确要求  

### 6. Verify

```bash
git status
```

```
设计文档: 已同步 <paths> | 无需同步（理由）
方案状态: <plan> → <status> | 无方案
行动层: 已更新 <path> | 无行动层
Commit: <short-hash> <subject>
Included: <N> paths（代码+文档一并）
工作区: 仍保留未提交 WIP（如有）…
```

## Anti-patterns

- 假设所有仓库都有 `dev/progress/` 硬改不存在的路径  
- 同主题拆成「只交代码 / 只交文档」  
- 为摘 hunk 而半文件提交（除非用户要求）  
- `git add .` 卷进**明确无关**的其他主题 WIP  
- 为干净而 stash/restore Excluded  
- 无行为变化却大面积改 spec  
- 未经要求就 push / amend / `--no-verify`  

## Relation to other skills

- 刚用 `architecture-first-solution` 定案 → 实施完成后用本 skill 收尾  
- 审查类 skill 不替代文档门禁  
