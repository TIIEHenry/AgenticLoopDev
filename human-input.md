---
title: "人类 Loop 输入约定"
type: guide
status: accepted
phase: N/A
updated: 2026-07-28
summary: "人类只给模型+方向；推荐 Sticky 调度不变量；每 tick 强制重读契约。"
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

另建议附带 **Sticky 调度不变量**（见下）——写进 `/loop` wake 的每轮 prompt，防长会话忘掉 `loop-prompt.txt`。

**OpenCode**：父会话用 **`opencode -m provider/model`** 启动（k3：`kimi-for-coding/k3`）；跨栈或须换另一模型轨才用 **`opencode run -m …`**。有 `-m` 时**不必**在 prompt 写 `当前模型：`。见 [runtimes/opencode.md](runtimes/opencode.md)、[cli/opencode.md](cli/opencode.md)。

**费用与选型** → [models.md](models.md)。默认低成本；**GPT 5.5、Opus** 须 prompt 明文；**Grok / kimi-k3** 默认可用。**实施阶段**固定当前环境模型，勿每 tick 重议选型。

**具体做什么** → 父 agent 每轮读 status / roadmap，经 Direction Discovery 选出 **exactly one** 可执行下一步。

## Sticky 调度不变量（推荐，全运行时）

长会话易漂：wake 变短、历史被实现噪音淹没。Sticky **只放不变量**，**不要**每 tick 整篇粘贴 `loop-prompt.txt`。

**推荐文案**（可原样放进 `/loop` 或各运行时 wake prompt，再跟「当前模型 / 方向」）：

```text
你是调度者，不亲自写 prod 代码。每 tick 开头必须重新 Read：dev/loop/loop-prompt.txt 与 dev/loop/execution-contract.md（不可凭记忆）。禁止 SwitchMode 进只读 Plan。禁止空转/等用户/当心跳结束：若无 exactly one 可执行下一步，立即委派 Direction Discovery（可并行 Wave 0），把 status/Next 当假设并用代码验证，勿盲信「已完成」。禁止删除本 loop。人类方向见本消息；细节以刚读的 loop-prompt 为准。
```

| 要 | 不要 |
|:---|:-----|
| 短 sticky + 每 tick **工具 Read** 契约文件 | 把 100+ 行 `loop-prompt` 粘进每轮 wake |
| status/Next 当**假设**，用代码验证 | 「忽略进度文档」导致重复劳动 |
| 无推荐 → 调度者立即启动 Direction Discovery 重分析 | 当心跳空转结束 |
| 「禁止删 loop」 | 把 **Cursor 专属**（`notify_on_output` / 替换 sleep）写进通用 sticky |

Cursor 专属调度（`notify_on_output`、替换旧 sleep）→ [runtimes/cursor.md](runtimes/cursor.md)。

## 方向 vs 任务（对比）

| ❌ 人类不写（任务） | ✅ 人类写（方向） |
|:-------------------|:-----------------|
| 「改 `dev/plans/foo.md` 第三节」 | 「按文档推进方案缺口」 |
| 「勾选 roadmap T3-2」 | 「优先 Singularity 客户端 parity」 |
| 「跑 `:core:test` 并修 failures」 | 「引擎稳定性 / 测试绿」 |
| 「用 GPT 5.5 写代码」 | 「当前模型：GPT 5.5（主架构）」— **仅首次方案/评估轨** |
| 「adb / 烟测」 | 「烟测轨」— **当前环境子 agent**（OpenCode 内勿 `opencode run`） |
| 「禁止自动提交」 | 「Git：禁止 commit」— 仅探索/只读 loop |

## 示例

```text
/loop 10m @dev/loop/loop-prompt.txt
你是调度者，不亲自写 prod 代码。每 tick 开头必须重新 Read：dev/loop/loop-prompt.txt 与 dev/loop/execution-contract.md（不可凭记忆）。禁止 SwitchMode 进只读 Plan。禁止空转/等用户/当心跳结束：若无 exactly one 可执行下一步，立即委派 Direction Discovery（可并行 Wave 0），把 status/Next 当假设并用代码验证，勿盲信「已完成」。禁止删除本 loop。人类方向见本消息；细节以刚读的 loop-prompt 为准。
当前模型：Composer。方向：按 status 与活跃 roadmap 推进，优先客户端缺口。
```

间隔 `5m` / `10m` 随意；**`loop-prompt.txt` 不变**。Sticky 文案见上节（可省略重复粘贴若运行时已把 sticky 写进 wake）。

```text
/loop 5m @dev/loop/loop-prompt.txt
当前模型：mimo-v2.5-pro（Claude Code）。方向：实施为主，不改架构方案正文。
```

（上例未带 sticky 时，agent 仍须按 [workflow.md](workflow.md) 每 tick 强制 Read 契约。）

烟测（**当前环境子 agent**；门禁见 [external-cli.md](external-cli.md)）：

```text
/loop 10m @dev/loop/loop-prompt.txt
当前模型：Composer。方向：Singularity adb 烟测轨；全局仅 1 个后台测试 agent。
```

贵模型 / Cursor 授权示例：

```text
当前模型：Grok。方向：按 status 推进方案与实施
本轨主架构文档授权：子 agent 可使用 model=gpt-5.5，仅用于 dev/plans/foo.md
禁止：GPT 5.5 / Opus 参与写代码
```

```text
Cursor 可用：本轨可用 agent -p --trust 写架构 doc
当前模型：mimo-v2.5-pro（Claude Code）
方向：架构 doc 由 Cursor CLI 主笔，本轨只做实施
```

## Agent 每轮自行决定

1. 读 **当前模型** + **方向**（理解范围与优先级，不当作任务列表）  
2. 读 `dev/progress/status.md`、`dev/roadmap/active/`、相关 plan  
3. **选 exactly one** 本轮 slice（与方向一致、有证据、可验证）  
4. 执行 → 单路验收 → 更新 status / roadmap → **Loop 会话**：门禁通过则自主 commit + 构建绿则 push（见 [workflow.md](workflow.md) § Git）  
5. 结尾输出「本轮选择」与「Next」——**Next 必填**且具体可执行；若无 → 调度者立即启动 Direction Discovery 重分析，不得空结束  

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
