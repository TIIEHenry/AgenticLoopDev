---
title: "Qoder CLI（qodercli）"
type: guide
status: accepted
phase: N/A
updated: 2026-07-29
summary: "Qoder 非交互：qodercli -p；Ultimate=GPT 5.6（须显式指定）；同栈禁止。"
---

# Qoder CLI：`qodercli`

## 前置

```bash
which qodercli
qodercli --version
qodercli --list-models    # 须已 login；本仓库约定 Ultimate = GPT 5.6
# 登录：qodercli 内 /login，或 export QODER_PERSONAL_ACCESS_TOKEN=…
```

IDE 入口 `qoder` 打开图形界面，**不是**本页非交互 CLI。

## 最小用法（非交互）

```bash
ROOT="$(git rev-parse --show-toplevel)"
qodercli -p --dangerously-skip-permissions -m performance -w "$ROOT" "$prompt"
```

少审批交互父会话：

```bash
qodercli -m performance -w "$ROOT"
# 或（若版本支持）：qodercli --yolo -m performance
```

**Ultimate = GPT 5.6**（**必须人类显式指定**：`-m ultimate` 和/或 prompt 写明 Ultimate/GPT 5.6；**禁止**写 prod 代码；未指定则勿用）：

```bash
qodercli -p --dangerously-skip-permissions -m ultimate -w "$ROOT" "$prompt"
```

跨栈调用时：人类未写明 Ultimate/GPT 5.6 → **禁止**自行加 `-m ultimate`。
## 常用参数

| 参数 | 说明 |
|:-----|:-----|
| `-p`, `--print` | 非交互输出后退出 |
| `-m`, `--model` | 模型：档位名 / Frontier 名；Custom 用 modelID |
| `-w`, `--cwd` | 工作目录（仓库根） |
| `--dangerously-skip-permissions` | 跳过权限确认（受信目录） |
| `--yolo` | 部分版本等价少审批（以 `--help` 为准） |
| `--permission-mode` | `default` / `accept_edits` / `bypass_permissions` / `dont_ask` / `auto` |
| `-c`, `--continue` | 续最近会话 |
| `-r`, `--resume` | 按 id 恢复 |
| `--agent` / `--agents` | 指定或注册 Subagent |
| `--list-models` | 打印当前账号可用模型 |
| `-o`, `--output-format` | `text` / `json` / `stream-json` |
| `--worktree [name]` | 在独立 git worktree 启动 |

完整列表：`qodercli --help`。环境变量：`QODER_MODEL`、`QODER_WORKING_DIR`、`QODER_PERSONAL_ACCESS_TOKEN` 等。

## Loop 能力档对照（常见 `-m`）

| 能力档 / 用途 | 典型 `-m` |
|:--------------|:----------|
| 实施（默认友好） | `performance`、`efficient`、`auto` |
| **GPT 5.6（强架构）** | **`ultimate`**（list 显示 `Ultimate`；**须人类显式指定**；禁写代码） |
| **kimi-k3** | 以 `--list-models` 为准（常见 `kimi-k3`） |
| deepseek-v4-pro | `deepseek-v4-pro`（以 list 为准） |

见 [../models.md](../models.md)、[../runtimes/qoder.md](../runtimes/qoder.md)。

## Loop 门禁

| 当前环境 | `qodercli -p` |
|:---------|:--------------|
| **已在 Qoder 会话** | ❌ 用会话 / Subagent（`/agents`） |
| **Qoder 内须换另一模型** | ✅ `qodercli -p -m <与当前不同的 slug>` |
| **不在 Qoder** | ✅ 跨栈按需（授权） |

详见 [../external-cli.md](../external-cli.md)。
