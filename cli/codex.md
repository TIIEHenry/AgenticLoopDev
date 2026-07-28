---
title: "Codex CLI（codex exec）"
type: guide
status: accepted
phase: N/A
updated: 2026-07-28
summary: "Codex 非交互：codex exec / resume；本仓库架构主笔授权轨常用。"
---

# Codex CLI：`codex exec`

## 前置

```bash
which codex
codex --version
```

配置：`~/.codex/config.toml`（模型等）。

## 最小用法

```bash
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
codex exec "$prompt"
```

续会话：

```bash
codex exec resume --last
codex exec resume --last "继续：先读 dev/progress/status.md"
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

完整列表：`codex exec --help`。

## Loop 门禁

| 当前环境 | `codex exec` |
|:---------|:-------------|
| **已在 Codex 会话** | 避免无必要并行同栈 exec；优先 `resume` |
| **不在 Codex** | ✅ 跨栈；本仓库架构主笔见 `loop-prompt.txt` Model Authorization |

详见 [../external-cli.md](../external-cli.md)、[../runtimes/codex.md](../runtimes/codex.md)。
