---
title: "Antigravity CLI（agy）"
type: guide
status: accepted
phase: N/A
updated: 2026-07-28
summary: "Antigravity 非交互：agy -p；同栈禁止再起 agy -p。"
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

## 常用参数

| 参数 | 说明 |
|:-----|:-----|
| `-p`, `--print` | 非交互，完成后退出（**必加**） |
| `--model <slug>` | 如 `gemini-3.5-flash`、`gemini-3.1-pro` |
| `--dangerously-skip-permissions` | 自动同意工具执行 |
| `-c`, `--continue` | 续最近会话 |
| `--conversation <id>` | 恢复指定会话 |
| `--sandbox` | 终端沙箱限制 |

完整列表：`agy --help`。

## Loop 门禁

| 当前环境 | `agy -p` |
|:---------|:---------|
| **Antigravity TUI 内** | ❌ 用 `invoke_subagent` |
| **不在 Antigravity** | ✅ 跨栈按需（授权） |

详见 [../external-cli.md](../external-cli.md)、[../runtimes/antigravity.md](../runtimes/antigravity.md)。
