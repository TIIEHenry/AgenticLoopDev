---
title: "Kimi Code CLI（kimi）"
type: guide
status: accepted
phase: N/A
updated: 2026-07-28
summary: "Kimi Code CLI（默认 k3）：交互推荐 kimi --yolo；非交互 kimi -p；前端优先。"
---

# Kimi Code CLI：`kimi`

官方文档：<https://moonshotai.github.io/kimi-code/>

**默认模型**：`kimi-code/k3`（`~/.kimi-code/config.toml` 的 `default_model`）。能力档见 [../models.md](../models.md)。

## 前置

```bash
which kimi
kimi --version
kimi doctor          # 校验 ~/.kimi-code 配置
# 未登录时：
kimi login
```

## 推荐：交互 + YOLO

Loop / 受信工作区批量改码时，**默认用 YOLO**，跳过常规工具审批（仍可能提问；Plan 退出审批不被 YOLO 跳过）：

```bash
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
kimi --yolo
# 短写：
kimi -y
```

| 参数 | 短写 | 说明 |
|:-----|:-----|:-----|
| `--yolo` | `-y` | 自动批准常规工具调用（写文件、跑 shell） |
| （隐藏别名） | `--yes` / `--auto-approve` | 同 `--yolo` |

会话内也可输入 `/yolo` 开关。仅在**信任的工作目录**使用。

### YOLO vs `--auto`

| 模式 | 行为 |
|:-----|:-----|
| **`--yolo`** | 自动批准常规工具；agent **仍可**向用户提问 |
| **`--auto`** | 更彻底无人值守：工具与提问均自动处理，**不问用户** |
| 二者 | **互斥**，不能同时传 |

```bash
kimi --auto          # 完全 AFK
kimi --continue --yolo   # 续会话并切到 YOLO
```

## 非交互：`kimi -p`

脚本 / 单次委派用 `-p`。**注意：`-p` 不能与 `--yolo` / `--auto` / `--plan` 同用**；非交互模式默认按 **auto** 权限跑工具。

```bash
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
kimi -p "$prompt"
kimi -m kimi-code/k3 -p "$prompt"
kimi -p "$prompt" --output-format stream-json
```

| 参数 | 说明 |
|:-----|:-----|
| `-p`, `--prompt` | 非交互跑一条 prompt，打印回复后退出 |
| `-m`, `--model` | 模型别名；本仓库默认 **`kimi-code/k3`**（见 `~/.kimi-code/config.toml`） |
| `--output-format text\|stream-json` | 仅配合 `-p`；程序解析用 `stream-json` |

## 其他常用

| 参数 / 命令 | 说明 |
|:------------|:-----|
| `-c`, `--continue` | 续本目录最近会话 |
| `-S`, `--session [id]` | 恢复会话（无 id 则交互挑选） |
| `--plan` | 以 Plan 模式启动 |
| `--add-dir <dir>` | 额外工作区目录（可重复） |
| `kimi provider list` | 列出已配置 provider |

完整列表：`kimi --help`。

## 能力与选型

kimi-k3 能力档（≈ Grok、前端优先等）→ [../models.md](../models.md)。

## Loop 门禁

| 当前环境 | `kimi` CLI |
|:---------|:-----------|
| **已在 Kimi 交互会话** | ❌ 不要再起同目录 `kimi -p`；会话内继续即可 |
| **不在 Kimi** | ✅ 交互 **`kimi --yolo`**；脚本 **`kimi -p`** |

| 入口 | slug |
|:-----|:-----|
| 本页 `kimi` | `kimi-code/k3` |
| OpenCode | **`kimi-for-coding/k3`** → [opencode.md](opencode.md) |

`k2p6` = 旧档。门禁全文 → [../external-cli.md](../external-cli.md)。
