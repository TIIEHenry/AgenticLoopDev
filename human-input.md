---
title: "人类 Loop 输入约定"
type: guide
status: accepted
phase: N/A
updated: 2026-07-09
summary: "人类在 loop 中只给当前模型与大致方向；与 dev/loop/loop-prompt.txt 配合使用。"
---

# 人类 Loop 输入约定

启动契约见 **[`loop-prompt.txt`](loop-prompt.txt)**（全运行时唯一）。人类在**同一条消息**里另起两行补充：

## 原则

人类 **不** 在 loop 提示词里指定「本轮做什么具体任务」（不写 checkbox id、不改哪份 plan、不列实施步骤）。

人类 **只** 提供：

| 输入 | 必填 | 说明 |
|:-----|:-----|:-----|
| **当前模型** | CC/Codex **必填**；Cursor 推荐；**OpenCode 有 `-m` 则不必写** | Claude Code：`当前模型：mimo-v2.5-pro（Claude Code）`；OpenCode：用 `-m deepseek/deepseek-v4-pro` |
| **大致方向** | 是 | 一两句话的**轨道/优先级/范围**，不是任务清单 |

**OpenCode**：父会话用 **`opencode -m provider/model`** 启动；跨栈或须换另一模型轨才用 **`opencode run -m …`**。有 `-m` 时**不必**在 prompt 写 `当前模型：`。见 [runtimes/opencode.md](runtimes/opencode.md)。

**费用**（便宜 → 贵）：`mimo < kimi-k2.6 < Composer < Grok < deepseek << GPT << Opus`。默认低成本；**GPT 5.5、Opus** 须 prompt 明文；**Grok** 默认可用（Cursor）。**实施阶段**固定当前环境模型，勿每 tick 重议选型。见 [overview § 迭代原则](overview.md#迭代原则)、[models.md](models.md)。

**具体做什么** → 父 agent 每轮读 `dev/progress/status.md`、roadmap、playbook，经 **Direction Discovery**（或等价自主选任务）选出 **exactly one** 可执行下一步。

## 方向 vs 任务（对比）

| ❌ 人类不写（任务） | ✅ 人类写（方向） |
|:-------------------|:-----------------|
| 「改 `dev/plans/foo.md` 第三节」 | 「按文档推进方案缺口」 |
| 「勾选 roadmap T3-2」 | 「优先 Singularity 客户端 parity」 |
| 「跑 `:core:test` 并修 failures」 | 「引擎稳定性 / 测试绿」 |
| 「用 GPT 5.5 写代码」 | 「当前模型：GPT 5.5（主架构）」— **仅首次方案/评估轨** |
| 「adb / 烟测」 | 「烟测轨」— **当前环境子 agent**（OpenCode 内勿 `opencode run`） |
| 「禁止自动提交」 | 「Git：禁止 commit」— 仅探索/只读 loop |

## 示例（Cursor）

```text
/loop 10m @dev/loop/loop-prompt.txt
当前模型：Composer。方向：按 status 与活跃 roadmap 推进，优先客户端缺口。
```

间隔 `5m` / `10m` 随意；**`loop-prompt.txt` 不变**。

```text
/loop 5m @dev/loop/loop-prompt.txt
当前模型：mimo-v2.5-pro（Claude Code）。方向：实施为主，不改架构方案正文。
```

烟测（**当前环境子 agent**；OpenCode 父会话内**禁止**再起 `opencode run`）：

```text
/loop 10m @dev/loop/loop-prompt.txt
当前模型：Composer。方向：Singularity adb 烟测轨；全局仅 1 个后台测试 agent。
```

## Agent 每轮自行决定

1. 读 **当前模型** + **方向**（理解范围与优先级，不当作任务列表）  
2. 读 `dev/progress/status.md`、`dev/roadmap/active/`、相关 plan  
3. **选 exactly one** 本轮 slice（与方向一致、有证据、可验证）  
4. 执行 → 单路验收 → 更新 status / roadmap → **Loop 会话**：门禁通过则自主 commit + 构建绿则 push（见 [workflow.md](workflow.md) § Git）  
5. 结尾输出「本轮选择」与「Next」——**Next 必填**；若无具体项则重跑 Direction Discovery，不得空结束  

方向**过宽**时：按 status 的 Next、roadmap 依赖、P0/P1 自行收窄；**不过宽**时不向人类索要具体任务（除非 `HUMAN_DECISION_REQUIRED`）。

## 例外

| 情况 | 说明 |
|:-----|:-----|
| **模型/授权明文** | `GPT 5.5 主架构`、`Cursor 可用`、`Git：禁止 commit` 等，见 [models.md](models.md)、[external-cli.md](external-cli.md) |
| **HUMAN_DECISION_REQUIRED** | 架构 blocking 时暂停，向人类要**裁决**而非要「帮我选任务」 |

## 相关

- [prompts.md](prompts.md) — 如何用 `loop-prompt.txt`  
- [workflow.md](workflow.md) — tick 步骤  
- [loop-prompt.txt](loop-prompt.txt) — 自主选任务契约  
