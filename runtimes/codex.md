---
title: "Loop 运行时 — Codex"
type: guide
status: accepted
phase: N/A
updated: 2026-07-03
summary: "在 Codex 中运行开发 Loop：/loop 或交互会话、codex exec resume。"
---

# Codex 运行时

用 **`/loop`**（若环境提供）或 **交互续聊** 推进。间隔与唤醒由 Codex 内 `/loop` 自带；本仓库只维护 [`loop-prompt.txt`](../loop-prompt.txt)。

## 交互会话

```bash
cd /path/to/repo
codex
```

首条 prompt：`@dev/loop/loop-prompt.txt` + 模型与方向。每轮用自然语言要求按 [workflow.md](../workflow.md) 继续。

续聊：

```bash
codex resume --last
# 或
codex exec resume --last
```

## `/loop`（若环境提供）

```text
/loop 10m @dev/loop/loop-prompt.txt
当前模型：<slug>
方向：按 status 推进。
```

## 单次 `codex exec`（跨栈 / CI）

命令与参数 → **[../cli/codex.md](../cli/codex.md)**。同栈优先 `exec resume`，门禁 → [../external-cli.md](../external-cli.md)。

## 子 agent / 分工

| 方式 | 说明 |
|:-----|:-----|
| **同会话分阶段** | 父 agent 在 Codex 内切换角色（首选） |
| **`codex exec resume`** | 延续会话，勿无必要并行多个 exec |
| **跨栈** | 仅 prompt 授权；烟测用当前环境子 agent |

见 [models-and-delegation.md](../models-and-delegation.md)。

## 配置

- 项目级：`codex` 读取工作区与 `AGENTS.md` 惯例（以本地 `codex doctor` 为准）  
- 全局：`~/.codex/config.toml`（`-c key=value` 覆盖）  

## 选型

| 适合 Codex loop | 不太适合 |
|:----------------|:---------|
| `/loop` 或交互续聊推进 tick | 强依赖 IDE 内并行 6 路 wave |
| 单次 `codex exec` / CI slice | 频繁人工点选 UI |
| `codex apply` 落地 patch | 复杂 adb 多会话（用当前环境子 agent） |

更多 CLI → [../cli/INDEX.md](../cli/INDEX.md)、[../external-cli.md](../external-cli.md)。
