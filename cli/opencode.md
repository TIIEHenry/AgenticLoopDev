---
title: "OpenCode CLI（opencode run）"
type: guide
status: accepted
phase: N/A
updated: 2026-07-28
summary: "OpenCode 非交互：opencode run -m；同栈禁止；换模型例外。"
---

# OpenCode CLI：`opencode run`

## 前置

```bash
which opencode
opencode --version
opencode models                 # 查 provider/model
```

## 最小用法（非交互）

```bash
ROOT="$(git rev-parse --show-toplevel)"
opencode run -m kimi-for-coding/k3 --dir "$ROOT" "$prompt"
# 旧档（勿与 k3 混用）：
# opencode run -m kimi-for-coding/k2p6 --dir "$ROOT" "$prompt"
```

启动 **TUI 父会话**（非 `run`）：

```bash
opencode -m kimi-for-coding/k3
```

## 常用参数

| 参数 | 说明 |
|:-----|:-----|
| `message..` | 任务描述 |
| `--dir <path>` | 仓库根 |
| `-m`, `--model` | `provider/model` |
| `--title <name>` | 会话标题 |
| `-f`, `--file` | 附加文件 |
| `--format json` | JSON 事件流 |
| `--auto` | 自动批准未显式拒绝的权限（危险） |
| `-c`, `--continue` | 续最近会话 |

完整列表：`opencode run --help`。

## Loop 能力档对照（常见 `-m`）

| 能力档模型 | 典型 `-m` |
|:-----------|:----------|
| **kimi-k3** | **`kimi-for-coding/k3`**（或 `kimi-for-coding/k3-256k`） |
| kimi-k2.6（旧） | `kimi-for-coding/k2p6` |
| deepseek-v4-pro | `deepseek/deepseek-v4-pro` |

独立 Kimi Code CLI（同 k3）见 [kimi.md](kimi.md)。

见 [../models.md](../models.md)、[../runtimes/opencode.md](../runtimes/opencode.md)。

## Loop 门禁

| 当前环境 | `opencode run` |
|:---------|:---------------|
| **OpenCode 会话内** | ❌ 禁止（用会话子 agent） |
| **OpenCode 内须换另一模型** | ✅ `opencode run -m <与当前不同的 slug>` |
| **不在 OpenCode** | ✅ 跨栈按需；烟测仍优先当前环境子 agent |

详见 [../external-cli.md](../external-cli.md)。
