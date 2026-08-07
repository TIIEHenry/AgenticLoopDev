---
title: "Claude Code CLI（claude）"
type: guide
status: accepted
phase: N/A
updated: 2026-08-08
summary: "Claude Code 非交互：bypassPermissions -p；无 --no-plan（勿用 permission-mode plan）；Opus 4.6 写作须 --model。"
---

# Claude Code CLI：`claude`

## 前置

```bash
which claude
claude --version
```

## 最小用法（非交互）

**默认**：`claude -p` **无需** `--model`（走 CLI 当前默认档，**不是** Opus 4.6）。**仅**要用 **Opus 4.6** 写作轨时，**必须**显式 `--model claude-opus-4-6`。

```bash
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
# 默认档（无需 --model）
claude --permission-mode bypassPermissions -p "$prompt"
# Opus 4.6 写作轨（须 loop 明文授权 + 必须 --model）
claude --permission-mode bypassPermissions -p --model claude-opus-4-6 "$prompt"
```

父 agent 已在 CC 会话内时：**不要**再起 `claude -p`（同栈门禁）；用当前会话或 `/model claude-opus-4-6` 切换。

## 常用参数

| 参数 | 说明 |
|:-----|:-----|
| `-p`, `--print` | 非交互输出 |
| `--permission-mode bypassPermissions` | 跳过工具权限确认（仅受信目录；Loop 非交互推荐） |
| `--permission-mode plan` | **进入**只读 Plan（**不是**「关掉 plan」）。实施/改码 **不要**用 |
| `--dangerously-skip-permissions` | 旧写法，等价 bypass；新 CLI 优先 `--permission-mode` |
| `--model <slug>` | 默认档**不必传**；**Opus 4.6** 写作轨**必须** `--model claude-opus-4-6`（须 loop prompt 明文授权） |
| `--agents <json>` | 自定义 agents |
| `--continue` | 续会话 |

> **无 `--no-plan`**：与 Grok Build 不同，`claude` 没有该旗标。Loop 改码用 `bypassPermissions` 即可；**禁止**误加 `--permission-mode plan`。Grok 侧须 `--no-plan` → [grok.md](grok.md)。

完整列表：`claude --help`。

## 写作轨（Opus 4.6）

**写作最强**档：`claude-opus-4-6`（长上下文变体 `claude-opus-4-6[1m]`）。能力定位：写作 5；架构 **> Composer**；代码 **< deepseek**；单价 **> Grok**。**须** loop prompt / 人类 **明文授权**；**禁止**写 prod 代码（Loop 硬禁）。

**调用**：Opus 4.6 **不是** CLI 默认档 → **必须** `--model claude-opus-4-6`（或 `[1m]` 变体）；普通 `claude -p` **不要**带 `--model`。

```bash
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
claude --permission-mode bypassPermissions -p --model claude-opus-4-6 "$prompt"
```

父 agent 在 **Cursor / OpenCode / Qoder** 等栈、本 tick 已授权写作轨时，用上述跨栈调用润色 `dev/plans/`、`docs/architecture/` 叙述段落（架构结论仍由 Grok / 强架构主笔）。父 agent **已在 Claude Code** 时：会话内 `/model claude-opus-4-6` 或启动 `claude --model claude-opus-4-6`；**不要**再起 `claude -p`（同栈门禁）。

## Loop 门禁

| 当前环境 | `claude -p` |
|:---------|:------------|
| **已在 Claude Code 会话** | ❌ 用会话 / `--agents` |
| **不在 Claude Code** | ✅ 跨栈按需（授权） |

详见 [../external-cli.md](../external-cli.md)、[../runtimes/claude-code.md](../runtimes/claude-code.md)。
