---
title: "Loop 运行时 — OpenCode"
type: guide
status: accepted
phase: N/A
updated: 2026-07-03
summary: "OpenCode Loop：会话内子 agent；禁止同栈 opencode run；换模型才可 CLI；-m 指定 provider/model。"
---

# OpenCode 运行时

周期推进用 **`/loop`**（若环境提供）或 **交互续聊**；间隔由 OpenCode 内 `/loop` 自带。本仓库只维护 [`loop-prompt.txt`](../loop-prompt.txt)。

## 同栈：已在 OpenCode 会话（Loop 父 agent）

| 任务 | 做法 |
|:-----|:-----|
| **写代码、烟测、挖 bug** | **当前会话内子 agent** 分工（与 Cursor→`Task`、CC→会话 同理） |
| **`opencode run`** | ❌ **禁止**（同栈重复起 CLI，抢 adb / 会话） |

**唯一例外 — 换用另一模型**：当前会话绑定模型 A，本轨**必须**用模型 B 时，可：

```bash
opencode run -m kimi-for-coding/k2p6 --dir "$ROOT" "…"
```

`-m` 须与**当前会话实际模型不同**；仍遵守全局 **adb 仅 1 个后台**。

启动父会话时选模型（非 `opencode run`）：

```bash
opencode -m deepseek/deepseek-v4-pro "$(git rev-parse --show-toplevel)"
opencode models kimi-for-coding   # 查 slug
```

## 跨栈：父 agent 不在 OpenCode

父 agent 在 **Cursor / Claude Code / Codex** 时，**默认仍用当前环境子 agent**（含烟测）。仅当 prompt **明文**要求跨栈 OpenCode，或当前环境无法跑 adb/shell 时，才：

```bash
opencode run -m deepseek/deepseek-v4-pro --dir "$ROOT" "$PROMPT"
```

不要在 prompt 里写「用 deepseek」代替 `-m`；模型由 **CLI `-m`** 指定。

## 模型：`-m provider/model`

```bash
opencode models
opencode models deepseek
opencode models kimi-for-coding
```

| Loop slug | `opencode -m` |
|:----------|:--------------|
| deepseek-v4-pro | `deepseek/deepseek-v4-pro` |
| kimi-k2.6 | `kimi-for-coding/k2p6` |

能力序见 [models.md](../models.md)。

### 何时写进 prompt、何时只写 CLI

| 场景 | 模型怎么定 | prompt 写 `当前模型：`？ |
|:-----|:-----------|:-------------------------|
| **OpenCode 父会话** | 启动 `opencode -m …` 或 TUI 内切换 | 可选；每轮复述实际 slug |
| **OpenCode 父会话 + 换模型轨** | `opencode run -m <另一 slug>` | 否 |
| **跨栈**（父不在 OpenCode） | 调用方 `-m` | 否 |

## 烟测（adb）

- **默认**：**当前环境子 agent**（OpenCode 内 = 会话分工，**不是** `opencode run`）
- 全局 **仅 1 个** adb 后台烟测（与 Singularity 共享设备）
- 辅助脚本 `scripts/opencode-adb-singularity.sh`（若环境提供）供**跨栈**调用；OpenCode 父会话内应直接跑 adb 步骤，勿再 exec 该脚本起第二条 `opencode run`

## 与 UA TUI

| | OpenCode 会话 / `opencode run`（跨栈） | `opencode` TUI + `--ua-grpc` |
|--|----------------------------------------|------------------------------|
| 引擎 | OpenCode + 配置的 slug | UniverseAgent 后端 |
| 用途 | Loop 开发 / 烟测 | 测 UA 引擎本身 |

详见 [models-and-delegation.md](../models-and-delegation.md)、[external-cli.md](../external-cli.md)。
