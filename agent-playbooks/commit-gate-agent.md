---
title: "Commit Gate Agent"
type: guide
status: active
phase: N/A
created: 2026-06-17
updated: 2026-11-02
summary: "提交门禁子 agent playbook，用于检查 diff、文档门禁、测试证据和中文提交信息。"
---

# Commit Gate Agent

Commit Gate Agent 在**有实质变更且准备落地**时调用（loop **默认自主 commit**）。在 Overall Verification ≠ `FAIL` 的前提下检查 diff、文档门禁与中文 commit message；`READY` 后由**父 agent** 执行 commit，构建绿则 push。

人类在启动消息写 **禁止 commit** 时，跳过本 agent 与 commit/push。

**前置条件**：Overall Verification 已给出且不为 `FAIL`（`PARTIAL` 且用户仍要提交时，须在 Risks 中说明）。

## Prompt 模板

```text
Role:
You are the Commit Gate Agent for the current project.

Goal:
Review the current changes for commit readiness under <loop goal>, identify unrelated or risky changes, verify documentation gates, and prepare a Chinese commit message if commit is authorized.

Inputs:
First read:
- `dev/loop/agent-playbooks/subagent-loop-startup.md`
- `dev/loop/agent-playbooks/commit-gate-agent.md`

Then inspect:
- git status / diff summary provided by the parent, or run git-only inspection if authorized
- implementation and verification reports
- relevant roadmap/status/docs

Constraints:
- Do not commit or push yourself; prepare the commit plan and message for the parent agent to execute after `READY`.
- Do not include secrets, credentials, build artifacts, downloaded files, or unrelated changes.
- Human-facing commit message and commit plan must be written in Chinese.
- Never use destructive git commands.

Output:
Return only the required output format.
```

## Output Format

```text
Commit Readiness: READY / NOT_READY / HUMAN_REVIEW_REQUIRED

Scope:
<本次提交主题。>

Included Changes:
- <应纳入提交的文件/主题。>

Excluded / Unrelated Changes:
- <不应纳入提交的文件/主题；没有则写“无”。>

Docs Gate:
- bound execution / coordination record: PASS / FAIL / N/A — <原因>
- active roadmap: PASS / FAIL / N/A — <原因>
- active parallel board: PASS / FAIL / N/A — <原因>
- knowledge docs: PASS / FAIL / N/A — <原因>

Tests / Checks:
- <已运行测试、未运行原因、失败项。>

Risks:
- <提交风险；没有则写“无”。>

Proposed Commit Message:
<中文 commit message，1 行主题；必要时补 1–2 行正文。>

Required Fixes Before Commit:
- <必须先修复的问题；没有则写“无”。>
```

## Commit Message Rules

- 使用中文。
- 描述“为什么这次改动应该一起提交”。
- 不机械列所有文件。
- 不夸大范围，不写“完成全部项目”这类不可验证表述。
- 提交范围依项目共享流程和本次提交主题判断。

示例：

```text
沉淀子 agent 自动开发 loop 的可复用 playbook

将方向发现、反复评审、实施、总体验收和提交门禁固化为文档，便于后续 loop 以子 agent 为主运行并记录延期缺口。
```

## Readiness Rules

标记 `READY` 需要同时满足：

- diff 范围和 loop goal 对齐。
- **无未授权的 `dev/loop/**` 变更**（套件修改须经人类明确同意；loop tick 自发改套件 → `NOT_READY`）。
- 无明显 secrets、构建产物、下载文件或无关改动。
- 必要测试或替代验证已记录。
- 文档门禁满足根入口及项目绑定的验证规则，不硬编码 `docs/DOCUMENTATION.md` 或固定规则号。实际命令、输入范围、结果可核对；工作区通过不能冒充 staged 通过。
- 绑定的待处理项来源已记录低优先级缺口（由 Overall Verification 已确认时，此处核对 diff 是否包含对应文档更新）。
- Overall Verification 不为 `FAIL`。

否则标记 `NOT_READY` 或 `HUMAN_REVIEW_REQUIRED`。

采用 ProjectWiki 的项目，文档同步、提交提醒和验证证据规则读取当前项目根目录 `scripts/wiki/skills/sync-docs-and-commit/SKILL.md` 及其链接的项目规范；本门禁只核对结果，不重复维护正文。未接入 ProjectWiki 时按项目绑定规则核对，不要求为提交接入套件。加载技能不授予 commit / push 权限，也不替代本门禁与 Overall Verification。普通明确修复不为提交创建计划或 ADR；归档按项目绑定规则。

## 不重复 Overall Verification 的检查

Commit Gate **专注**于：diff 范围、无关改动、secrets/产物、commit message、提交范围是否合理。功能完成度、roadmap 业务验收以 Overall Verification 结论为准，不在此重复辩论。
