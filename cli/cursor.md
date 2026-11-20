---
title: "Cursor CLI（agent）"
type: guide
status: accepted
phase: N/A
updated: 2026-11-19
summary: "Cursor 非交互 CLI：agent -p --trust。套餐内是 Grok 4.7/4.6/4.5 与 Composer 2.5。同栈禁止；跨栈须 Cursor 可用。"
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

## 模型（2026-11-19）

来源：[cursor.com/docs/models-and-pricing](https://cursor.com/docs/models-and-pricing)。

套餐内：**Grok 4.7、Grok 4.6、Grok 4.5、Composer 2.5**。Plus / Free 没有第三方，也没有 Auto。

实施用 Composer 2.5，不要默认 Fast。架构未授权时，IDE 里的 Task 传列表最新 Grok slug，不要为了架构去切聊天模型。Cursor 价目有 GPT-5.6 Sol / Terra / Luna，**没有 GPT-6**。Fable 现行档是 5.2。第三方都要 Premium 及以上的预付额度，并且仍须本 tick 点名。

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
