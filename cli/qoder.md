---
title: "Qoder CLI（qodercli）"
type: guide
status: accepted
phase: N/A
updated: 2026-11-20
summary: "Qoder 非交互：qodercli -p。只登记档位，不写具体型号。顶档须显式指定且不写代码。同栈禁止。"
---

# Qoder CLI：`qodercli`

## 前置

```bash
which qodercli
qodercli --version
qodercli --list-models    # 须已 login。具体型号以这次输出为准，不写进仓库
# 登录：qodercli 内 /login，或 export QODER_PERSONAL_ACCESS_TOKEN=…
```

IDE 入口 `qoder` 打开图形界面，**不是**本页非交互 CLI。

## 最小用法（非交互）

```bash
ROOT="$(git rev-parse --show-toplevel)"
qodercli -p --dangerously-skip-permissions -m auto -w "$ROOT" "$prompt"
```

`-m` 用本机 list 里的非顶档。`auto` 只是档位名。旧档名 `performance` 不再当作现行档；list 里没有的名字不要传。

少审批交互父会话：

```bash
qodercli -m auto -w "$ROOT"
```

顶档**必须人类显式指定**（`-m ultimate` 或 prompt 写明顶档）。不写 prod 代码，也不把这个档写成其他 CLI 的某一代。未指定则不要加 `-m ultimate`。

```bash
qodercli -p --dangerously-skip-permissions -m ultimate -w "$ROOT" "$prompt"
```
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

## Loop 只登记档位

| 档 | Loop |
|:---|:-----|
| 非顶档 | 实施。名字以 `--list-models` 为准，仓库不抄具体型号 |
| 顶档 | 方案 / 架构 / 挖 bug。须人类点名。不写代码。不映射到其他 CLI 的某一代 |

见 [../models.md](../models.md)、[../runtimes/qoder.md](../runtimes/qoder.md)。

## Loop 门禁

| 当前环境 | `qodercli -p` |
|:---------|:--------------|
| **已在 Qoder 会话** | ❌ 用会话 / Subagent（`/agents`） |
| **Qoder 内须换另一模型** | ✅ `qodercli -p -m <与当前不同的 slug>` |
| **不在 Qoder** | ✅ 跨栈按需（授权） |

详见 [../external-cli.md](../external-cli.md)。
