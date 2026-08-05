---
title: "Antigravity CLI（agy）"
type: guide
status: accepted
phase: N/A
updated: 2026-08-03
summary: "Antigravity 非交互：agy -p；同栈禁止再起 agy -p；只读审计须强调禁 restore。"
---

# Antigravity CLI：`agy`

## 前置

```bash
which agy
agy --version
```

## 最小用法（非交互）

```bash
ROOT="$(git rev-parse --show-toplevel)"
agy --model gemini-3.5-flash \
  --dangerously-skip-permissions \
  -p "$prompt"
```

> **`--dangerously-skip-permissions` 会放开写文件与 shell。**  
> 「最小用法」≠ 只读。若任务只是审计 / 找 gap，**必须**用下文「只读审计」约束；否则子 agent 可能改码甚至 `git restore` 清掉他人 WIP。

## 只读审计（强制强调）

跨栈用 `agy -p` **只做审计**时，prompt **必须**显式包含下列硬约束（与 [AGENTS.md §并行开发](../../../AGENTS.md#并行开发agent-强制) / [worktrees.md](../worktrees.md) 工作区保护一致）：

```text
READ-ONLY AUDIT. You MUST NOT:
- edit, create, or delete any files
- apply patches or "fix then revert"
- run: git checkout / git restore / git stash / git clean / git reset --hard
  (or any command that discards, overwrites, or stashes existing worktree changes)

Only read source and print the requested markdown.
Propose fixes as text in the report — never apply them.
```

推荐再加一层运行时限制（能用则用）：

| 手段 | 说明 |
|:-----|:-----|
| `--sandbox` | 收紧终端能力（仍须在 prompt 写禁 restore） |
| `--mode plan` | 若本机 `agy` 支持，优先于可写改码模式 |
| 省略 `--dangerously-skip-permissions` | 交互审批更吵，但可挡部分写操作；headless 审计仍以 prompt 硬约束为准 |

审计与实施 **分开两次会话**：审计会话只出 findings；实施另起 `-p`，再允许改码（仍禁止 restore/stash 他人改动）。

## 常用参数

| 参数 | 说明 |
|:-----|:-----|
| `-p`, `--print` | 非交互，完成后退出（**必加**） |
| `--model <slug>` | 如 `gemini-3.5-flash`、`gemini-3.1-pro` |
| `--effort` | 部分模型必填：`low` / `medium` / `high` |
| `--dangerously-skip-permissions` | 自动同意工具执行（**可写**；审计须配只读 prompt） |
| `-c`, `--continue` | 续最近会话 |
| `--conversation <id>` | 恢复指定会话 |
| `--sandbox` | 终端沙箱限制 |
| `--mode` | 如 `plan` / `accept-edits`（以 `agy --help` 为准） |

完整列表：`agy --help`。

## Loop 门禁

| 当前环境 | `agy -p` |
|:---------|:---------|
| **Antigravity TUI 内** | ❌ 用 `invoke_subagent` |
| **不在 Antigravity** | ✅ 跨栈按需（授权） |

详见 [../external-cli.md](../external-cli.md)、[../runtimes/antigravity.md](../runtimes/antigravity.md)。
