---
name: sync-docs-and-commit
description: >-
  Close out implementation work by syncing necessary design/spec docs, updating
  plan document status when a plan was followed, refreshing action-layer progress
  (status/roadmap), then creating a scoped git commit. Use when finishing a
  task, closing a session, the user asks to sync docs and commit, update plan
  status and commit, or run documentation gate before commit.
---

# Sync Docs and Commit

实施收尾技能：按需同步设计文档 → 更新方案状态（若有方案）→ 更新行动层 → **仅暂存本次主题**并提交。

若仓库有文档规范（如 `docs/DOCUMENTATION.md`），遵守其提交前文档门禁；并遵守用户 git 安全协议。本 skill 被调用即视为用户授权完成本主题 commit；**默认不 push**，除非用户另行要求。

## When to apply

- 功能/修复实施完成，准备收尾
- 用户说：同步文档并提交、更新方案状态、commit 前文档门禁、收尾提交
- 刚做完有对应 `dev/plans/` 方案的实现

## Workflow

```
Sync-Docs-Commit Progress:
- [ ] 1. Scope the theme (Included / Excluded)
- [ ] 2. Sync design docs (if necessary)
- [ ] 3. Update plan status (if a plan was used)
- [ ] 4. Update action layer (status / roadmap / frontmatter)
- [ ] 5. Commit (scoped add only)
- [ ] 6. Verify git status
```

### 1. Scope the theme

并行跑：`git status` · `git diff` · `git diff --cached` · `git log -5 --oneline`

| Included（本次主题） | Excluded（其他 WIP，禁止 add / restore / stash） |
|:---------------------|:-----------------------------------------------|
| … | … |

若同一文件混有无关 WIP → **停止**，请用户拆分（`HUMAN_DECISION_REQUIRED`）。

**Trivial 例外**：单行 typo / 纯测试断言 / 无行为变化 → 可跳过步骤 2–4，直接步骤 5；须标注 trivial。

### 2. Sync design docs — if necessary

| 变更性质 | 动作 |
|:---------|:-----|
| 用户可见行为 / UX / 对外接口 / 降级策略变了 | 更新对应 `docs/` 或模块 docs（通常 1–2 份） |
| 工具 / 协议 / 跨模块契约 | 更新工具 INDEX 或协议 doc；必要时 ADR（另轨） |
| 仅内部 refactor / 命名 / 测试 | **通常不必**改设计文档 |
| 文档目录新增/移动 | 更新 INDEX；若项目有文档健康检查则跑之 |
| 无行为/契约变化 | 跳过；收尾写「无需同步设计文档」 |

编辑过的每个带 frontmatter 的 `.md`：更新 `updated: YYYY-MM-DD`（今天）。

**禁止**：为「显得完整」而改无关 spec；过时文档只迁 archive，不删除。

### 3. Update plan status — if a plan was used

若跟随了 `dev/plans/<topic>.md`（或会话明确方案路径）：

1. 勾选已完成 checkbox / 阶段项  
2. 对齐 frontmatter `status`（完成 → `implemented`/`completed`；部分 → `in_progress`/`partially_completed`）  
3. 更新 `updated`  
4. 同步 roadmap / parallel 对应项（若有）  

无方案 → 跳过，收尾写「无方案文档」。  
方案与实施仍宜**分 commit**；本 skill 默认做实施主题提交；若仅有未提交方案改动则按方案 commit。

### 4. Action layer（最小清单）

非 trivial 实施 commit 必做（路径按项目约定，常见如下）：

- [ ] `dev/progress/status.md`：写入 Completed 或 Current Session 摘要  
- [ ] `status.md` 保持短（项目若有行数上限则遵守；超出迁 archive）  
- [ ] 活跃 `dev/roadmap/active/` 对应 checkbox 已勾（如有）  
- [ ] 活跃 `dev/parallel/active/` 已更新（如有）  
- [ ] 本次 plan / spec 的 `updated` 与 `status` 已对齐  

无 `dev/progress/` 的仓库 → 跳过进度文件，仅做 scope + commit。

### 5. Commit

1. 再确认 `git status` / `diff` / `log`  
2. **仅** `git add <path…>` Included — **禁止**有无关 WIP 时 `git add -A` / `git add .`  
3. **禁止**对 Excluded 做 `restore` / `stash` / `reset` / `checkout`  
4. 1–2 句 message（why 优先；对齐近期 log）  
5. HEREDOC 提交：

```bash
git commit -m "$(cat <<'EOF'
<message>

EOF
)"
```

6. hook 失败 → **修复后新建 commit**（勿随意 amend）  
7. **不要 push**，除非用户明确要求  

### 6. Verify

```bash
git status
```

```
设计文档: 已同步 <paths> | 无需同步（理由）
方案状态: <plan> → <status> | 无方案
Commit: <short-hash> <subject>
工作区: 仍保留未提交 WIP（如有）…
```

## Anti-patterns

- 代码已改、文档「下次再补」仍 commit  
- `git add .` 卷进其他主题 WIP  
- 为干净而 stash/restore 他人改动  
- 无行为变化却大面积改 spec  
- 方案未完成却标 `completed` / `implemented`  
- 未经要求就 push / amend / `--no-verify`  

## Relation to other skills

- 刚用 `architecture-first-solution` 定案 → 实施完成后用本 skill 收尾  
- 审查类 skill 不替代本 skill 的文档门禁  
