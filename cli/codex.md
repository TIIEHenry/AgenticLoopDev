---
title: "Codex CLI（codex exec）"
type: guide
status: accepted
phase: N/A
updated: 2026-11-20
summary: "Codex 非交互：codex exec / resume。日常模型 gpt-6.2-sol；Astra 只做点名后的方案或挖 bug。"
---

# Codex CLI：`codex exec`

## 前置

```bash
which codex
codex --version
```

配置：`~/.codex/config.toml`。官网现行示例是 `model = "gpt-6.2-sol"`。目录与退役名单 → [../models.md](../models.md#codex)。

## 最小用法

```bash
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
codex exec "$prompt"
```

续会话：

```bash
codex exec resume --last
codex exec resume --last "继续：先读 AGENTS.md 指向的项目开发入口及绑定的任务/协调记录；未采用的旧来源不读、不建"
```

也可把 loop 契约喂进去：

```bash
codex exec "$(cat "$ROOT/dev/loop/loop-prompt.txt")"
```

## 常用参数

| 参数 | 说明 |
|:-----|:-----|
| `exec [PROMPT]` | 非交互跑一轮；`-` 或 stdin 可读 prompt |
| `-m`, `--model <MODEL>` | 覆盖模型 |
| `-c`, `--config key=value` | 覆盖 config.toml |
| `exec resume --last` | 续最近会话 |
| `-i`, `--image <FILE>` | 附加图片 |

完整列表：`codex exec --help`。交互会话用 `/model` 看本账号实际有的 id。

## 模型（2026-11-19）

来源：[learn.chatgpt.com/docs/models](https://learn.chatgpt.com/docs/models)。

| 用途 | 命令 |
|:-----|:-----|
| 日常编码（官方推荐） | `codex exec -m gpt-6.2-sol` |
| 写作 / 看图 / 电脑操作 | `codex -m gpt-6.1-terra`（CLI 0.159.0+） |
| 最难的端到端工作 | GPT-6.2 Astra。id 以 `/model` 为准。**须本 tick 点名，不写代码** |

ChatGPT 登录的 Codex 里，`gpt-5.5` 已于 2026-10-14 退役。Loop 不选它。父会话已经是 `gpt-6.2-sol` 时，按当前环境写代码；不要自行改去 Astra。

## Loop 门禁

| 当前环境 | `codex exec` |
|:---------|:-------------|
| **已在 Codex 会话** | 避免无必要并行同栈 exec；优先 `resume` |
| **不在 Codex** | ✅ 跨栈；本仓库架构主笔见 `loop-prompt.txt` Model Authorization |

详见 [../external-cli.md](../external-cli.md)、[../runtimes/codex.md](../runtimes/codex.md)。
