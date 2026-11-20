---
title: "Loop 运行时 — Antigravity"
type: guide
status: accepted
phase: N/A
updated: 2026-11-19
summary: "Antigravity Loop 运行时。Free/Plus 用 gemini-3.8-flash；Pro+ 日常用 Gemini 4 Hydrogen 或 Orchestrator。新会话须显式 --model。"
---

# Antigravity 运行时

Antigravity（`agy`）是 Google Antigravity AI-first 平台的终端 TUI/CLI 客户端。

## 模型绑定

启动时指定模型。2026-11-19 官网套餐见 [models.md](../models.md#antigravityagy)。`agy models` 是本机清单。

| 模型 | 谁有 | Loop |
|:-----|:-----|:-----|
| Gemini 3.8 Flash | 全部套餐，含 Free / Plus | 免费档实施默认。slug 仍可用 `gemini-3.8-flash`，本机只有分档 id 时改用 `agy models` 的那条 |
| Gemini 4 Hydrogen | Pro 付费 / Ultra / Enterprise | 官方执行档 |
| Orchestrator (Neon / Argon / Carbon) | 与对应规划模型相同 | 规划模型出计划，Hydrogen 改代码。`--effort` 无效 |
| Gemini 4 Neon / Carbon / Argon | 见官网表。Free / Plus 没有 | 推理档。须点名。不写代码。无选择时的新对话会默认 Neon |
| Gemini 3.1 Pro、3.7 / 3.6 Flash | 仅 Enterprise | 不要当默认 |

`agy -p` 必须带 `--model`。用户也可在 TUI 用 `/model` 切换。

### Prompt 声明规范

- **Loop Prompt** 中应写入 `当前模型：<slug>（Antigravity）`。
- 若 Prompt 未明确声明，首轮将读取配置文件 `~/.gemini/antigravity-cli/settings.json` 中的 `"model"` 字段，声明假设，并在每轮输出结尾复述。

---

## 交互模式 (TUI)

1. 在仓库根目录下直接运行 `agy` 启动交互式 TUI 会话。
2. 初始 Prompt 可通过 `@dev/loop/loop-prompt.txt` 文件内容，伴随当前模型及方向输入。
3. 退出 TUI：使用 `Ctrl+D` 两次或输入 `/exit`。
4. 恢复最近的会话：运行 `agy -c` 或 `agy --continue`。
5. 恢复指定 ID 的会话：运行 `agy --conversation <id>`。

---

## 非交互模式 (CLI / L3 委派)

跨栈或单次 headless → **[../cli/antigravity.md](../cli/antigravity.md)**。同栈用 `invoke_subagent`，勿再 `agy -p` → [../external-cli.md](../external-cli.md)。

---

## 子 Agent 委派与分工

Antigravity 原生支持子 Agent 的定义和调用：
- **子 Agent 机制**：父 Agent 可通过 `invoke_subagent` 启动子 Agent（如 `research` 或 `self` 自复制类型），运行指定的 Playbook。
- **环境继承**：子 Agent 会继承父 Agent 的配置和工作区上下文。

---

## 配置文件 (`settings.json`)

全局配置项位于 `~/.gemini/antigravity-cli/settings.json`：
- `"model"`: 默认模型。Free / Plus 用 `"gemini-3.8-flash"`。Pro+ 不要留空，否则新会话会落到 Neon；写成 Hydrogen 或 Orchestrator 的本机 id。
- `"toolPermission"`: 工具确认模式，建议在非交互 loop 中配合 `--dangerously-skip-permissions`。
- `"enableTerminalSandbox"`: 是否开启沙箱限制。
- `"allowNonWorkspaceAccess"`: 是否允许工作区以外的文件读写。
