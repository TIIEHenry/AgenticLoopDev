---
title: "Loop 运行时 — Antigravity"
type: guide
status: accepted
phase: N/A
updated: 2026-07-06
summary: "Antigravity Loop 运行时：基于 agy 客户端，可交互续聊或非交互单次运行；支持 gemini-3.5-flash 与 gemini-3.1-pro。"
---

# Antigravity 运行时

Antigravity（`agy`）是 Google Antigravity AI-first 平台的终端 TUI/CLI 客户端。

## 模型绑定

Antigravity 运行时在启动或配置文件中指定模型。主要支持以下两个模型：

| Loop 标识 (Slug) | 模型全称 | 建议定位 | 费用档 |
|:---|:---|:---|:---|
| `gemini-3.5-flash` | Gemini 3.5 Flash | 实施与代码编写、库及 App 研究、高效率/低成本任务 | **极低** |
| `gemini-3.1-pro` | Gemini 3.1 Pro | 复杂 Debug 根因分析、一般架构设计与方案审查 | **中** |

用户可在启动时使用 `--model <slug>` 参数指定模型，或在 TUI 中使用 `/model` 命令切换。

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

用于父 Agent 跨栈委派或单次 headless 运行（非周期 Loop）：

```bash
ROOT="$(git rev-parse --show-toplevel)"
agy --model gemini-3.5-flash \
    --dangerously-skip-permissions \
    -p "$(cat "$ROOT/dev/loop/loop-prompt.txt")
    
当前模型：gemini-3.5-flash（Antigravity）
方向：更新 dev/progress/status.md 状态，进行局部代码实现"
```

### 常用参数

| 参数 | 说明 |
|:---|:---|
| `-p`, `--print` | 非交互/脚本输出模式，运行单次 Prompt 后自动退出。 |
| `--model <slug>` | 临时指定当前会话的模型（`gemini-3.5-flash` 或 `gemini-3.1-pro`）。 |
| `--dangerously-skip-permissions` | 自动批准所有工具执行权限（文件读写、指令运行等），适合自动化 Loop。 |
| `--sandbox` | 在受限的沙箱环境中运行终端指令，提高安全性。 |
| `--add-dir <path>` | 向当前工作区追加一个或多个目录路径（可多次指定）。 |

---

## 子 Agent 委派与分工

Antigravity 原生支持子 Agent 的定义和调用：
- **子 Agent 机制**：父 Agent 可通过 `invoke_subagent` 启动子 Agent（如 `research` 或 `self` 自复制类型），运行指定的 Playbook。
- **环境继承**：子 Agent 会继承父 Agent 的配置和工作区上下文。

---

## 配置文件 (`settings.json`)

全局配置项位于 `~/.gemini/antigravity-cli/settings.json`：
- `"model"`: 默认使用的模型（如 `"gemini-3.5-flash"`）。
- `"toolPermission"`: 工具确认模式，建议在非交互 loop 中配合 `--dangerously-skip-permissions`。
- `"enableTerminalSandbox"`: 是否开启沙箱限制。
- `"allowNonWorkspaceAccess"`: 是否允许工作区以外的文件读写。
