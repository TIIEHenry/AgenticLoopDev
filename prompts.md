---
title: "开发 Loop 提示词"
type: guide
status: accepted
phase: N/A
updated: 2026-08-27
summary: "唯一启动契约 loop-prompt.txt；/loop 只保活；Sticky 见 human-input；每 tick Boot 重读。"
---

# Loop 提示词

全项目**只有一个** Loop 启动契约（**跨仓库通用**，不绑定单一产品名）：

**[`loop-prompt.txt`](loop-prompt.txt)**

- **所有项目 / 运行时共用**同一文件；项目专属约束见仓库根 `AGENTS.md` / `CLAUDE.md` 与 `dev/progress/status.md`
- **定时间隔**由各运行时自带的 `/loop`（或等价命令）配置，**只保活**，不是「每到点只派一批」的调度量子；本 wake 须按 [execution-contract.md](execution-contract.md) 续派
- 人类每轮只补充 **当前模型** + **方向**；推荐附带 **Sticky** → [human-input.md](human-input.md)
- **每 tick** 父 agent 须工具 Read 本文件 + [execution-contract.md](execution-contract.md)（不可凭记忆）

## 启动示例

见 [human-input.md](human-input.md)（含 Sticky + `/loop` 完整示例）。此处只强调：**契约文件始终是 `loop-prompt.txt`**。

## 人类不要写进 Loop 的

具体任务、checkbox id、改哪个文件 — 见 [human-input.md](human-input.md)。  
技术授权（`Cursor 可用`、贵模型明文等）写在同一消息里 → [human-input.md](human-input.md)、[models.md](models.md)、[external-cli.md](external-cli.md)。  
Cursor 专属（`notify_on_output`、替换 sleep）→ [runtimes/cursor.md](runtimes/cursor.md)，**勿**写进通用 Sticky。

## 维护

- 改 Loop 契约 → 只改 **`loop-prompt.txt`**，并同步 `parent-loop-orchestrator.md` 与 `parallel-loop-waves.md`（若 wave 规则变更）
- 改单轮步骤 → [workflow.md](workflow.md)
- 旧路径 `dev/prompts/*.txt` 已废弃
