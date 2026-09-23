---
title: "模型能力与委派策略"
type: guide
status: accepted
phase: N/A
updated: 2026-09-23
summary: "任务→运行时/委派；架构设计付费最优先，架构定格是 Opus 5.5（Fable/GPT 仅点名，无明文才降级 Grok 4.7）；kimi架构审须授权；gemini-3.8-flash 前端实施主力。"
---

# 模型能力与委派策略

Loop 父 agent 选「谁干活」时，先看**当前在哪个运行时**，再看**任务类型**与**是否跨环境**。

> **能力对比 / 费用硬门禁 / 方案主笔** → [models.md](models.md)。
> **人类写什么** → [human-input.md](human-input.md)。
> **跨栈 CLI 门禁** → [external-cli.md](external-cli.md)；**命令** → [cli/INDEX.md](cli/INDEX.md)。

## 费用与授权门禁（摘要）

**Fable 5.1、Opus 5.5、GPT 5.6**（含 Qoder **Ultimate**）：无本 tick 人类 **明文授权**不得使用。默认 `loop-prompt.txt` **不**授权。GPT 5.5 已彻底下线移除。细则与降级 → [models.md § 费用维度](models.md#费用维度硬门禁)。

**kimi 与 mimo 授权门禁**：**kimi-k3（中强架构审）与 mimo 2.6 pro / flash 均须明文授权**。

**架构设计付费最优先，架构定格是 Opus 5.5**：方案 / ADR / Arch-First 先考虑付费档。定格用 **Opus 5.5**（点名 Opus，或只授权付费/强架构且未点名另一档）。Fable 5.1、GPT 5.6（含 Qoder Ultimate）仅本 tick 点名该档时用。已点名的档不得改用 Grok。未明文不得擅自调用，降级 **Grok 4.7** 或经授权的 **kimi-k3**。审查义务本身不构成付费授权。想用付费档 → `HUMAN_DECISION_REQUIRED`。

**执行硬铁律**：**架构与审查模型（Fable 5.1、Opus 5.5、GPT 5.6、Grok 4.7、kimi-k3）坚决不做执行、禁止写业务代码**。

**Qoder GPT 5.6**：档位 **Ultimate**（`-m ultimate`）= GPT 5.6。**必须人类显式指定**（`-m ultimate` 和/或 prompt 写明）才可用；list 仅有 Ultimate **不算**授权。禁写代码 → [runtimes/qoder.md](runtimes/qoder.md)。

## Grok 委派：无付费授权时的降级（子 agent 优先，CLI 其次）

架构轨**未**获得付费档授权、需要 **Grok 4.7** 降级时，先选通道，再调命令：

| 优先级 | 条件 | 通道 |
|:-------|:-----|:-----|
| 1 | 当前运行时**子 agent 模型列表含 Grok** | 原生子 agent 传该 slug（Cursor：`Task` + 列表**最新** `cursor-grok-*`） |
| 2 | 列表无 Grok 且 `which grok` 成功 | Shell `grok --no-plan --permission-mode bypassPermissions --always-approve -p`（不硬编 `-m`，走本机 4.7 默认） |
| 3 | 否则有经授权的 kimi-k3 | 专属 `kimi` CLI 通道（`kimi -p`；只能用 kimi CLI 调用） |
| 4 | 都没有 | `HUMAN_DECISION_REQUIRED` |

**禁止**在已有 Grok 子 agent 档时默认 `grok -p`。独立审查 = **另一实例**（Task / Subagent / CLI 均可），不是「必须走 CLI 进程」。已在 Grok 交互会话 → 不要再起同目录 `grok -p`。

## 同栈内置，跨栈才 CLI

**当前父 agent 已在某运行时内时，同栈能力用内置委派，不要起同栈 CLI。** 完整表与 Cursor / Qoder / OpenCode / 烟测门禁 → [external-cli.md](external-cli.md)。

**Cursor 内**：可用不同 `subagent_type`。实施 **默认不传 `model`**（与父同模型）。架构 / Arch-First：**付费档最优先**（本 tick 已明文则走人类点名的路径；Cursor 不 Task 传贵价 `model`）。未授权且列表含 Grok 时才传该 Grok slug。Fable / Opus / GPT 不得写代码 → [models.md](models.md)。

**Qoder 内**：用 Subagent（`/agents`）；**不要**再起 `qodercli -p`（换另一 `-m` 除外）。

## 任务 → 运行时 / 委派

费用档与「默认用哪款模型」→ [models.md § 费用 × 任务](models.md#费用--任务矩阵速查)。下表只答**走哪条委派路径**：

| 任务 | 优先委派 |
|:-----|:---------|
| 主架构 / ADR（首次与修订） | **定格 Opus 5.5**（点名 Opus，或只授权付费且未点名另一档）。Fable / GPT 5.6（含 Qoder **`-m ultimate`**）仅点名该档。未授权才降级 **Grok 4.7**（子 agent 有档则 Task/Subagent；否则 `grok -p`）。**不做执行** |
| 方案多视角评估 | 并行 reviewer / plan-analyst（不写代码；mimo 2.6 pro 须授权） |
| **架构设计审查（Arch-First）** | **定格 Opus 5.5**。点名时才用 Fable / GPT 5.6。未授权才降级**独立 Grok 4.7**（子 agent 优先，CLI 其次）或 **kimi-k3**（须授权·只能用 kimi CLI）；**不做执行**；禁 Composer 单审 |
| 辅助方案 / 混合设计 | 当前环境（Composer）；**mimo 2.6 pro**（比 gemini 更强·须授权） |
| 方案写作、润色 | 架构结论走付费强架构档（已授权）；未授权才 Grok 4.7。叙述润色可用当前环境 Composer；顶级方案写作用 Opus 5.5 / Fable 5.1 |
| **前端代码实施** | **gemini-3.8-flash**（比 deepseek 更强，前端首选主力，极低成本高吞吐）；mimo 2.6 pro / flash（须授权） |
| **通用后端实施** | **deepseek-v4.1-flash**（略强于 Composer）→ `opencode run -m opencode-go/deepseek-v4.1-flash`；当前环境 Composer；mimo 2.6（须授权） |
| 挖 bug / 根因 | **Grok 4.7**（子 agent 优先，CLI 其次）或当前环境；贵模型须 prompt 授权 |
| adb / 烟测 | **当前环境子 agent** → [external-cli.md](external-cli.md) |

## 多视角评估（方案阶段）

**工程质量优先**前提下，**方案 / 架构首次起草与重大修订**鼓励多 agent **并行多视角**：

| ✅ 做法 | ❌ 不做 |
|:--------|:--------|
| 强架构主笔 + 并行 reviewer / plan-analyst 提质疑 | 弱模型各自改一版方案正文 |
| Review-Question-Resolve：问题清单 → 强模型改 doc | 为「好看」 spawn Opus+GPT+mimo 各写全文 |
| 主笔**付费最优先**（已明文则用 Fable / Opus 5.5 / GPT 5.6）；并行质疑可用中档。未授权不得擅自拉付费档 | 实施阶段用付费档或 Grok 写代码 |

**实施阶段**：固定当前环境模型 → [models.md § 实施阶段](models.md#实施阶段少纠结模型)。

## 验收：单路收口

**Overall Verification** 每轮仍要跑（见 [workflow.md](workflow.md)），但 **不要**为验收再开多路 reviewer 各写一份评审报告。

**Wave 3 维度评审**（architecture / tester / security）**仅** plan/ADR 首次或重大修订 tick；**实施 tick 跳过 Wave 3** → [parallel-loop-waves.md § Wave 3](agent-playbooks/parallel-loop-waves.md#wave-3--评审触发条件)。

| ✅ 验收做法 | ❌ 不做 |
|:------------|:--------|
| **当前 tick 父 agent**对照 Loop Goal、roadmap、测试、diff 做**单路** PASS/FAIL | 验收轨再 spawn 3+ 视角「再评一遍」 |
| 弱模型验收：只核对清单与证据，质疑项**反馈给强模型**改 doc | 验收用 Opus + GPT 各写总结 |
| 方案未闭合：记 blocking question，下轮强架构 + 多视角评估改 plan | 用多视角验收代替实施 |

## 技术授权示例

人类输入格式见 [human-input.md](human-input.md)。技术授权（非任务）示例：

```text
Grok 子 agent 可用：架构/doc/bug 优先 Task/Subagent 传 Grok slug（Cursor：最新 cursor-grok-*）
Grok CLI 可用（子 agent 无 Grok 档时）：grok -p --no-plan --permission-mode bypassPermissions --always-approve（不硬编 -m）
kimi 架构审可用：本轨架构审授权：kimi-k3（使用 kimi CLI 调用，禁走 opencode）
mimo 实施可用：本轨执行授权：mimo 2.6 pro
Cursor 可用：授权 agent -p 跑架构 doc（无 Grok 子 agent 且 grok CLI 不可用时）
本轨跨栈 OpenCode：父 agent 不在 OpenCode 且 prompt 明文时，`opencode run -m opencode-go/deepseek-v4.1-flash`
本轨跨栈 Qoder：父不在 Qoder 时，`qodercli -p --dangerously-skip-permissions -m performance`
```

## 相关

- [models.md](models.md) — 能力量化与费用
- [human-input.md](human-input.md) — 人类输入
- [runtimes/INDEX.md](runtimes/INDEX.md) — 运行时选型
- [runtimes/grok.md](runtimes/grok.md) — Grok CLI L2
- [runtimes/qoder.md](runtimes/qoder.md) — Qoder L2
- [external-cli.md](external-cli.md) — CLI 门禁
- [cli/INDEX.md](cli/INDEX.md) — CLI 命令
- [parallel-loop-waves.md](agent-playbooks/parallel-loop-waves.md)
