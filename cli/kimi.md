---
title: "Kimi Code CLI（kimi）"
type: guide
status: accepted
phase: N/A
updated: 2026-11-19
summary: "Kimi Code CLI。架构审现行旗舰 k3.1-pro，须授权且不写代码；k3-256k 与 kimi-for-coding 须授权后可执行。"
---

# Kimi Code CLI：`kimi`

官方文档：<https://www.kimi.com/code/docs/en/>

**架构审**：`k3.1-pro`（CLI 别名按惯例 `kimi-code/k3.1-pro`，以登录后写入的 `config.toml` 为准）。`k3` 仍可用。**须本 tick 明文授权，不写业务代码。**

**执行**（也须授权）：`k3-256k`、`kimi-for-coding`（K2.8 Preview）、`kimi-for-coding-highspeed`。没有授权就不要用 Kimi 写代码。

能力档见 [../models.md](../models.md#kimi-code)。

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
kimi -m kimi-code/k3.1-pro -p "$prompt"
kimi -p "$prompt" --output-format stream-json
```

| 参数 | 说明 |
|:-----|:-----|
| `-p`, `--prompt` | 非交互跑一条 prompt，打印回复后退出 |
| `-m`, `--model` | 模型别名。架构审 `kimi-code/k3.1-pro` 或 `kimi-code/k3`；执行档见上文。键名以本机 config 为准 |
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

K3.1 Pro / k3：架构审，须授权，不写代码。`k3-256k` 与 `kimi-for-coding`：须授权后可执行。→ [../models.md](../models.md)。

## Loop 门禁

| 当前环境 | `kimi` CLI |
|:---------|:-----------|
| **架构审查 / Arch-First** | ✅ 授权后用 `k3.1-pro` 或 `k3` 跑 `kimi -p`；**不写代码** |
| **实施改代码** | 仅当本 tick 授权了 `k3-256k` 或 `kimi-for-coding`。K3.1 Pro / k3 禁止写代码 |
| **已在 Kimi 交互会话** | ❌ 不要再起同目录 `kimi -p`；会话内继续即可 |

### 调用通道约束（硬规则）

- **唯一通道**：K3.1 Pro 与 k3 **只能用专属 `kimi` CLI（`kimi -p`）调用**。执行档同样走这个 CLI。
- **严禁间接调用**：**严禁**通过 OpenCode（如 `opencode run -m .../k3`）或其它运行时代调 Kimi。
- **没有 2.6**：现行旗舰是 K3.1 Pro，上一档是 k3。不要写成 kimi 2.6。

门禁全文 → [../external-cli.md](../external-cli.md)。
