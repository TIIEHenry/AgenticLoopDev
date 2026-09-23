---
title: "Claude Code CLI（claude）"
type: guide
status: accepted
phase: N/A
updated: 2026-09-23
summary: "Claude Code 非交互：bypassPermissions -p；无固定模型；无 --no-plan（勿用 permission-mode plan）。"
---

# Claude Code CLI：`claude`

## 前置

```bash
which claude
claude --version
```

## 最小用法（非交互）

Claude Code **没有固定模型**。`claude -p` **不传** `--model`，走 CLI 当前配置。只有本 tick 人类明文给出 slug 时才传 `--model <slug>`。

```bash
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
claude --permission-mode bypassPermissions -p "$prompt"
```

父 agent 已在 CC 会话内时：**不要**再起 `claude -p`（同栈门禁）；用当前会话。

## 常用参数

| 参数 | 说明 |
|:-----|:-----|
| `-p`, `--print` | 非交互输出 |
| `--permission-mode bypassPermissions` | 跳过工具权限确认（仅受信目录；Loop 非交互推荐） |
| `--permission-mode plan` | **进入**只读 Plan（**不是**「关掉 plan」）。实施/改码 **不要**用 |
| `--dangerously-skip-permissions` | 旧写法，等价 bypass；新 CLI 优先 `--permission-mode` |
| `--model <slug>` | 默认不传。仅本 tick 人类明文点名某 slug 时才传 |
| `--agents <json>` | 自定义 agents |
| `--continue` | 续会话 |

> **无 `--no-plan`**：与 Grok Build 不同，`claude` 没有该旗标。Loop 改码用 `bypassPermissions` 即可；**禁止**误加 `--permission-mode plan`。Grok 侧须 `--no-plan` → [grok.md](grok.md)。

完整列表：`claude --help`。

## Loop 门禁

| 当前环境 | `claude -p` |
|:---------|:------------|
| **已在 Claude Code 会话** | ❌ 用会话 / `--agents` |
| **不在 Claude Code** | ✅ 跨栈按需（授权） |

详见 [../external-cli.md](../external-cli.md)、[../runtimes/claude-code.md](../runtimes/claude-code.md)。
