---
title: "Cursor CLI（agent）"
type: guide
status: accepted
phase: N/A
updated: 2026-07-28
summary: "Cursor 非交互 CLI：agent -p --trust；同栈禁止；跨栈须 Cursor 可用。"
---

# Cursor CLI：`agent`

## 前置

```bash
which agent
agent --version
```

认证：`CURSOR_API_KEY` 或 `agent --api-key …`。

## 最小用法（非交互）

```bash
ROOT="$(git rev-parse --show-toplevel)"
agent -p --trust --workspace "$ROOT" "$prompt"
```

## 常用参数

| 参数 | 说明 |
|:-----|:-----|
| `-p`, `--print` | 非交互/脚本模式（**必加**） |
| `--trust` | 信任工作区，减少 headless 确认 |
| `--workspace <path>` | 工作区根（默认 cwd） |
| `--model <id>` | 指定模型 |
| `--mode plan` / `--mode ask` | 只读规划或问答 |
| `-f`, `--force` / `--yolo` | 自动允许命令（谨慎；`--yolo` = `--force`） |
| `--output-format text\|json\|stream-json` | 机器可读输出（仅 `-p`） |
| `--continue` / `--resume` | 续会话 |

完整列表：`agent --help`。

## Loop 门禁

| 当前环境 | `agent -p` |
|:---------|:-----------|
| **Cursor IDE 内** | ❌ 用 `Task` |
| **非 Cursor** | ❌ 默认禁止 |
| **非 Cursor** + prompt **「Cursor 可用」** | ✅ |

详见 [../external-cli.md](../external-cli.md)。

## 典型用途

- 补全 `dev/plans/`、`docs/architecture/`  
- 架构疑难、差距分析  
- **不要**默认用于 adb 烟测（优先当前环境子 agent / OpenCode）
