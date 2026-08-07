---
title: "OpenCode CLI（opencode run）"
type: guide
status: accepted
phase: N/A
updated: 2026-08-07
summary: "OpenCode 非交互：opencode run -m；deepseek-v4-flash 编码轨；同栈禁止；换模型例外。"
---

# OpenCode CLI：`opencode run`

## 前置

```bash
which opencode
opencode --version
opencode auth list              # 已登录 provider（本机含 OpenCode Go）
opencode models opencode-go     # 本仓库 deepseek-v4-flash 所在 provider
opencode models                 # 全部 provider/model
```

## Provider：`opencode-go`（本仓库默认）

`opencode models` 会列出**多个** provider 下的同名模型，**不要混用**：

| provider | 典型 slug | 何时用 |
|:---------|:----------|:-------|
| **`opencode-go`** | **`opencode-go/deepseek-v4-flash`** | **Loop 默认** — OpenCode Go 订阅（`opencode auth list` → `OpenCode Go`） |
| `deepseek` | `deepseek/deepseek-v4-flash` | 直连 DeepSeek API 凭证；**≠** opencode-go |
| `kimi-for-coding` | `kimi-for-coding/k3` | Kimi Code 独立凭证；亦可 `opencode-go/kimi-k3` |

**配置位置**（本机实测）：

| 路径 | 内容 |
|:-----|:-----|
| `~/.config/opencode/opencode.json` | 全局权限（`*: allow` 等）；**无**默认 model |
| `<repo>/opencode.json` | 项目 MCP + 权限；**无** provider 覆盖 |
| `~/.local/share/opencode/auth.json` | 已登录 provider 凭证 |

查本机 opencode-go 模型：`opencode models opencode-go`（含 `deepseek-v4-flash`、`deepseek-v4-pro`、`kimi-k3` 等）。

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

| 能力档模型 | 典型 `-m` | 说明 |
|:-----------|:----------|:-----|
| **kimi-k3** | **`kimi-for-coding/k3`**（或 `kimi-for-coding/k3-256k`） | 前端优先 |
| **deepseek-v4-flash** | **`opencode-go/deepseek-v4-flash`** | 编码 **略强于 Composer**；单价 **> Composer**；**慢于 Composer**；偏通用后端改码 |
| kimi-k2.6（旧） | `kimi-for-coding/k2p6` | 勿与 k3 混用 |
| deepseek-v4-pro | `opencode-go/deepseek-v4-pro` | 架构弱；单价高于 v4-flash |

### deepseek-v4-flash（编码加强轨）

父 agent **不在 OpenCode** 或须换模型轨时，可用：

```bash
ROOT="$(git rev-parse --show-toplevel)"
opencode run -m opencode-go/deepseek-v4-flash --dir "$ROOT" "$prompt"
```

| 对比 Composer | v4-flash |
|:--------------|:---------|
| 编码能力 | **略强** |
| 费用 | **更高** |
| 速度 | **更慢** |
| 架构主笔 | ❌ 不主笔方案/ADR |

TUI 父会话：`opencode -m opencode-go/deepseek-v4-flash`。

独立 Kimi Code CLI（同 k3）见 [kimi.md](kimi.md)。

见 [../models.md](../models.md)、[../runtimes/opencode.md](../runtimes/opencode.md)。

## Loop 门禁

| 当前环境 | `opencode run` |
|:---------|:---------------|
| **OpenCode 会话内** | ❌ 禁止（用会话子 agent） |
| **OpenCode 内须换另一模型** | ✅ `opencode run -m <与当前不同的 slug>` |
| **不在 OpenCode** | ✅ 跨栈按需；烟测仍优先当前环境子 agent |

详见 [../external-cli.md](../external-cli.md)。
