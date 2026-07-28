---
title: "开发 Loop 提示词"
type: guide
status: accepted
phase: N/A
updated: 2026-07-03
summary: "唯一启动契约 loop-prompt.txt（全项目通用）；定时间隔因环境而异。"
---

# Loop 提示词

全项目**只有一个** Loop 启动契约（**跨仓库通用**，不绑定单一产品名）：

**[`loop-prompt.txt`](loop-prompt.txt)**

- **所有项目 / 运行时共用**同一文件；项目专属约束见仓库根 `AGENTS.md` / `CLAUDE.md` 与 `dev/progress/status.md`
- **定时间隔**由各运行时自带的 `/loop`（或等价命令）配置，**不**另建 `-3m` / `-10m` 提示词文件
- 人类每轮只补充 **当前模型** + **方向** → [human-input.md](human-input.md)

## 启动示例

### Cursor

```text
/loop 10m @dev/loop/loop-prompt.txt
当前模型：Composer。方向：按 status 与 roadmap 推进。
```

间隔 `5m` / `10m` / `30m` 随意；**提示词文件不变**。

### Claude Code / Codex（首条）

粘贴 `dev/loop/loop-prompt.txt` 全文，再跟一行：

```text
当前模型：mimo-v2.5-pro（Claude Code）
方向：实施为主，不改架构方案正文
```

续聊：「继续下一轮，先读 status，在方向内自选一项。」

各运行时的 `/loop`（或等价）会自带间隔与唤醒说明；本仓库只维护 **`loop-prompt.txt`** 契约。

## 人类不要写进 Loop 的

具体任务、checkbox id、改哪个文件 — 见 [human-input.md](human-input.md)。

技术授权（模型档、`Cursor 可用` 等）可写在方向同一消息里，见 [models.md](models.md)。

## 维护

- 改 Loop 契约 → 只改 **`loop-prompt.txt`**，并同步 `parent-loop-orchestrator.md` 与 `parallel-loop-waves.md`（若 wave 规则变更）
- 改单轮步骤 → [workflow.md](workflow.md)
- 旧路径 `dev/prompts/*.txt` 已废弃
