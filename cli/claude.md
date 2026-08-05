---
title: "Claude Code CLI（claude）"
type: guide
status: accepted
phase: N/A
updated: 2026-08-05
summary: "Claude Code 非交互：claude --permission-mode bypassPermissions -p；同栈禁止再起 claude -p。"
---

# Claude Code CLI：`claude`

## 前置

```bash
which claude
claude --version
```

## 最小用法（非交互）

```bash
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
claude --permission-mode bypassPermissions -p "$prompt"
```

## 常用参数

| 参数 | 说明 |
|:-----|:-----|
| `-p`, `--print` | 非交互输出 |
| `--permission-mode bypassPermissions` | 跳过工具权限确认（仅受信目录；Loop 非交互推荐） |
| `--dangerously-skip-permissions` | 旧写法，等价 bypass；新 CLI 优先 `--permission-mode` |
| `--model <slug>` | 指定模型（如 `mimo-v2.5-pro`） |
| `--agents <json>` | 自定义 agents |
| `--continue` | 续会话 |

完整列表：`claude --help`。

## Loop 门禁

| 当前环境 | `claude -p` |
|:---------|:------------|
| **已在 Claude Code 会话** | ❌ 用会话 / `--agents` |
| **不在 Claude Code** | ✅ 跨栈按需（授权） |

详见 [../external-cli.md](../external-cli.md)、[../runtimes/claude-code.md](../runtimes/claude-code.md)。
