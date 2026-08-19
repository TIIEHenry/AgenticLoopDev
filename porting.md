---
title: "Loop 套件移植与同步"
type: guide
status: accepted
phase: N/A
updated: 2026-08-19
summary: "Loop 套件移植与同步；worktree 对齐用 git（见 worktrees §6）；关仓见 worktree-closeout；skills 一键安装。"
---

# Loop 套件移植与同步

> **原则**：`dev/loop/` 是**跨项目通用、字节级可同步**的 Loop SSOT。  
> **边界**：下文 `rsync` **仅**用于 `dev/loop/` 套件跨仓库复制。**worktree / `main` 对齐**一律用 git → [worktrees.md §6](worktrees.md#6-git-同步按需)；**禁止** rsync 对齐 worktree。
> **禁止**在 `dev/loop/` 内写某仓库名、模块名、Gradle 命令、worktree 历史路径等项目特例。  
> **`dev/loop/` 内任何修改须经人类明确同意**；Loop tick 中 agent **不得**自行改套件（见下文「套件治理」）。  
> 项目差异只写在 **`dev/loop/` 之外**（见下文「项目侧清单」）。
> **运行态隔离**：`loop.pid`、lock、cache、logs 等本地运行态文件写到 `dev/loop/.runtime/`，并通过套件内 `.gitignore` 忽略。

## 套件治理

| 规则 | 说明 |
|:-----|:-----|
| **人类改套件** | 维护者显式要求改 `dev/loop/`（或人类自己编辑）→ 允许；改完后 `rsync` 到各消费者仓库 |
| **Loop tick 禁止改套件** | 父 agent 与各子 agent **不得**在自主 loop 中修改 `dev/loop/**` |
| **需求进项目外** | 想改 loop 规则、playbook、worktree 策略 → 记入 `status.md` / 人类会话，**等人类**改 SSOT 后再 `rsync` |
| **验收** | 本轮 diff 含未授权 `dev/loop/` 变更 → Overall Verification **FAIL**；Commit Gate **NOT_READY** |

## 套件边界

| 在 `dev/loop/` 内（通用，可原样复制） | 在 `dev/loop/` 外（项目专属） |
|:-------------------------------------|:------------------------------|
| `loop-prompt.txt`、playbook、workflow | `dev/progress/status.md` |
| `worktrees.md`、`worktree-closeout.md`（池 + 关仓，无项目名） | `dev/progress/deferred-gaps.md` |
| `health-gates.md`（**何时跑** gate） | `dev/progress/research-queue.md` |
| `models.md`、`runtimes/`、`cli/`、`orchestration.md` | `dev/progress/health-gates.md`（**具体命令**） |
| `skills/`、`scripts/install-cursor-skills.sh` | `.cursor/skills/`（**安装产物**，可手动调用） |
| | `dev/roadmap/`、根 `AGENTS.md` / `CLAUDE.md` 入口链接 |
| | `dev/loop/.runtime/`（`loop.pid`、lock、cache、logs 等运行态目录） |
| | `.cursor/rules/`（可选，非套件一部分） |

文档中的 `../progress/` 链接是**相对路径约定**：复制 `dev/loop/` 后，目标仓库须有对应的 `dev/progress/` 文件。

`dev/loop/.runtime/` 是套件工作树内的本地运行态目录，应由套件内 `.gitignore` 忽略；不要把 pid/log 混入套件正文文件。

## 首次移植（新仓库）

### 1. 复制套件

在**维护 SSOT 的源仓库**执行（将 `SourceRepo` 换为实际路径）：

```bash
SRC="$(git -C /path/to/SourceRepo rev-parse --show-toplevel)"
DEST="$(git -C /path/to/TargetRepo rev-parse --show-toplevel)"

rsync -a --delete "$SRC/dev/loop/" "$DEST/dev/loop/"
```

- **`--delete`**：目标侧多出来的旧文件会被删掉，保持与源一致。  
- **不要**在复制后改 `dev/loop/` 里的项目特例；有需求应改源仓库再同步。

### 2. 初始化项目侧文件（若不存在）

在目标仓库创建（内容按项目填写，**不放进 `dev/loop/`**）：

| 文件 | 用途 |
|:-----|:-----|
| `dev/progress/deferred-gaps.md` | P2/P3 延期缺口 SSOT（空表 + 维护规则即可） |
| `dev/progress/research-queue.md` | 待研究队列 SSOT |
| `dev/progress/health-gates.md` | 集成编译命令、聚焦/grand gate 具体命令 |
| `dev/progress/status.md` | 迭代进度（通常已有） |
| `dev/loop/.gitignore` | 忽略 `.runtime/` 运行态目录 |

格式契约见复制过来的 [`agent-playbooks/subagent-loop-startup.md`](agent-playbooks/subagent-loop-startup.md)。

建议同时创建本地运行态目录约定：

```bash
mkdir -p dev/loop/.runtime
```

套件内 `.gitignore` 应包含：

```gitignore
.runtime/
```

### 3. 接入口文档

在目标仓库 `AGENTS.md`（或 `CLAUDE.md`）增加一行导航即可，例如：

```markdown
| [开发自动化 Loop](dev/loop/INDEX.md) | `/loop @dev/loop/loop-prompt.txt` |
```

**不要**在 `AGENTS.md` 里重复 playbook 全文；只链到 `dev/loop/`。

### 4. 安装 Cursor skills（可选，推荐）

一键安装**只建指向套件 SSOT 的 symlink/指针**，不复制正文；loop 更新后**无需重装**。

```bash
# 本机所有 Cursor 项目（薄指针 → @dev/loop/skills/.../SKILL.md）
./dev/loop/scripts/install-cursor-skills.sh --personal

# 当前消费者仓库（symlink → dev/loop/skills/<name>）
./dev/loop/scripts/install-cursor-skills.sh

# 任意仓库
/path/to/AgenticLoopDev/scripts/install-cursor-skills.sh /path/to/AnyRepo
```

也可直接 `@dev/loop/skills/<name>/SKILL.md`。详见 [skills/INDEX.md](skills/INDEX.md)。

### 5. 移除目标仓库旧 loop 资产

移植后**删除**（或不再维护）与套件重复的旧路径，避免双 SSOT：

| 典型旧路径 | 处理 |
|:-----------|:-----|
| `dev/agent-playbooks/` | 删除整目录 |
| `dev/prompts/autonomous-subagent-loop*.txt` | 删除 |
| `dev/prompts/loop-payload-*.json` | 删除 |
| `dev/plans/loop-worktree-parallel.md` 等 | 删除 |
| `.cursor/rules/loop-iteration.mdc` | 删除（可选；非必需） |
| `.cursor/rules/parallel-worktree-gate.mdc` | 删除（可选） |

将文档里指向旧路径的链接改为 `dev/loop/…`（**在 `dev/loop/` 外改**，不在套件内写项目名）。

### 6. 验证

```bash
# 目标仓库根
test -f dev/loop/loop-prompt.txt
test -f dev/loop/INDEX.md
test -f dev/loop/skills/INDEX.md
test -f dev/progress/health-gates.md
test -f dev/progress/deferred-gaps.md
test -f dev/progress/research-queue.md
# 若已安装 skills：
test -f .cursor/skills/sync-docs-and-commit/SKILL.md
```

启动：

```text
/loop 10m @dev/loop/loop-prompt.txt
当前模型：<slug>（<运行时>）
方向：<大致方向，非任务清单>
```

## 日常同步（套件升级）

当源仓库更新 `dev/loop/` 后，对已有目标仓库**重复同一条 rsync**：

```bash
SRC="$(git -C /path/to/SourceRepo rev-parse --show-toplevel)"
for DEST in /path/to/RepoA /path/to/RepoB; do
  rsync -a --delete "$SRC/dev/loop/" "$DEST/dev/loop/"
done
```

同步后：

1. **不要**手改各目标仓库的 `dev/loop/`（特例应反馈到源仓库统一改）。  
2. 检查 `dev/progress/health-gates.md` 是否仍满足本项目构建（**项目侧**，不参与 rsync）。  
3. 在目标仓库跑一轮 smoke：读 `status.md` → Direction Discovery → 无报错即可。

## 禁止事项

| 禁止 | 原因 |
|:-----|:-----|
| 在 `dev/loop/` 写仓库名、模块表、Gradle 命令 | 破坏字节同步 |
| 目标仓库单独 fork 一份 playbook | 双 SSOT |
| 在 `dev/loop/` 留「本仓库」小节 | 应写在 `dev/progress/` |
| rsync 时不加 `--delete` | 旧文件残留，与源不一致 |
| 在 `dev/loop/` 内修改 playbook、契约、worktree 规则 | Loop tick 中 agent 自行改 `dev/loop/`（**须人类同意**） |
| 用 stub/redirect 长期保留旧 `agent-playbooks/` | 应删旧目录，只保留 `dev/loop/` |
| 人类未授权时 commit `dev/loop/` 变更 | 套件变更须人类发起并审阅后再 `rsync`、再 commit |

## 多仓库维护建议

- **单一 SSOT 源**：在一个仓库维护 `dev/loop/`（改 playbook、worktrees 规则等），其余仓库只 rsync。  
- **变更流程**：改源 → rsync 全部消费者 → 各仓库单独 commit（`dev/loop/` 与 `dev/progress/` 可同 commit，但勿混 unrelated 代码）。  
- **项目构建命令变更**：只改该仓库 `dev/progress/health-gates.md`，**不**改 `dev/loop/health-gates.md` 的策略正文（除非策略本身要升级，则在源仓库改后 rsync）。

## 相关

- [INDEX.md](INDEX.md) — 套件索引  
- [prompts.md](prompts.md) — `loop-prompt.txt` 用法  
- [worktrees.md](worktrees.md) — worktree 池（通用）  
- [worktree-closeout.md](worktree-closeout.md) — 并行关仓 
- [health-gates.md](health-gates.md) — gate 策略（通用）；命令在 `dev/progress/health-gates.md`
