---
title: "模型能力与委派策略"
type: guide
status: accepted
phase: N/A
updated: 2026-11-19
summary: "任务→运行时/委派。架构定格仍是 Opus 5.5；未授权降级 Grok 4.7。Codex 日常 gpt-6.2-sol；Cursor 实施 Composer 2.5；Kimi 架构审 K3.1 Pro；AGY 执行档看套餐。"
---

# 模型能力与委派策略

Loop 父 agent 选「谁干活」时，先看**当前在哪个运行时**，再看**任务类型**与**是否跨环境**。

> **能力对比 / 费用硬门禁 / 方案主笔** → [models.md](models.md)。
> **人类写什么** → [human-input.md](human-input.md)。
> **跨栈 CLI 门禁** → [external-cli.md](external-cli.md)；**命令** → [cli/INDEX.md](cli/INDEX.md)。

## 费用与授权门禁（摘要）

**Fable 5.2 / 5.1、Opus 5.5、GPT-6.2 Astra、GPT-5.6 Sol / Terra、Gemini 4 Neon / Carbon / Argon**，以及 Qoder 顶档：无本 tick 人类 **明文授权**不得使用。Qoder 顶档不映射到上面任一具体型号。默认 `loop-prompt.txt` **不**授权。细则 → [models.md](models.md)。

**Kimi 与 mimo**：**K3.1 Pro / k3** 做架构审，须授权且不写代码。`k3-256k` 与 `kimi-for-coding` 须授权后可以执行。mimo 2.6 仍须授权。

**架构设计付费最优先，架构定格是 Opus 5.5**。Fable 5.2、GPT-6.2 Astra、GPT-5.6 Sol、Gemini 4 推理档仅点名该档。已点名的档不得改用 Grok。未明文则降级 **Grok 4.7**，或已授权的 **K3.1 Pro / k3**。想用付费档 → `HUMAN_DECISION_REQUIRED`。

**执行硬铁律**：Fable、Opus、GPT-6.2 Astra、GPT-5.6 Sol/Terra、Gemini 4 Neon/Carbon/Argon、Grok 4.7、K3.1 Pro、k3 **禁止写业务代码**。

**Qoder**：只登记档位。顶档须人类显式指定，不写代码，也不写成其他 CLI 的某一代。实施档以 `--list-models` 为准 → [runtimes/qoder.md](runtimes/qoder.md)。

## Grok 委派：无付费授权时的降级（子 agent 优先，CLI 其次）

架构轨**未**获得付费档授权、需要 **Grok 4.7** 降级时，先选通道，再调命令：

| 优先级 | 条件 | 通道 |
|:-------|:-----|:-----|
| 1 | 当前运行时**子 agent 模型列表含 Grok** | 原生子 agent 传该 slug（Cursor：`Task` + 列表里**版本最新**的 Grok，`grok-4.7-*` 或 `cursor-grok-*`） |
| 2 | 列表无 Grok 且 `which grok` 成功 | Shell `grok --no-plan --permission-mode bypassPermissions --always-approve -p`（不硬编 `-m`，走本机 4.7 默认） |
| 3 | 否则有经授权的 K3.1 Pro / k3 | 专属 `kimi` CLI（`kimi -p`；只能用 kimi CLI） |
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
| 主架构 / ADR（首次与修订） | **定格 Opus 5.5**。Fable 5.2、GPT-6.2 Astra、GPT-5.6 Sol、Gemini 4 Neon、Qoder **`-m ultimate`** 仅点名该档。未授权才降级 **Grok 4.7**。**不做执行** |
| 方案多视角评估 | 并行 reviewer / plan-analyst（不写代码；mimo 与 Kimi 执行档须授权） |
| **架构设计审查（Arch-First）** | **定格 Opus 5.5**。点名时才用 Fable 5.2 / Astra / GPT-5.6 Sol / Gemini 4 Neon。未授权才降级**独立 Grok 4.7**，或已授权的 **K3.1 Pro / k3**。**不做执行**。禁 Composer / Hydrogen 单审 |
| 辅助方案 / 混合设计 | 当前环境（Composer 2.5）；**mimo 2.6 pro**（须授权） |
| 方案写作、润色 | 架构结论走已授权的付费档；未授权才 Grok 4.7。叙述润色用 Composer 2.5 |
| **前端 / AGY Free、Plus** | **gemini-3.8-flash**。`agy -p` 必须带 `--model` |
| **AGY Pro+ 日常实施** | **Gemini 4 Hydrogen** 或 **Orchestrator**。Neon 不执行 |
| **通用后端实施** | **deepseek-v4.1-flash** → `opencode run -m opencode-go/deepseek-v4.1-flash`；Cursor **Composer 2.5** |
| **Codex 父会话** | 已绑定 slug。日常 `gpt-6.2-sol` 可以写代码。Astra 只做方案 / 挖 bug |
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
Grok 子 agent 可用：架构/doc/bug 优先 Task/Subagent 传列表最新 Grok slug（grok-4.7-* 或 cursor-grok-*）
Grok CLI 可用（子 agent 无 Grok 档时）：grok -p --no-plan --permission-mode bypassPermissions --always-approve（不硬编 -m）
kimi 架构审可用：本轨架构审授权：k3.1-pro（使用 kimi CLI，禁走 opencode；k3 仍可用）
kimi 执行可用：本轨执行授权：kimi-for-coding
mimo 实施可用：本轨执行授权：mimo 2.6 pro
Cursor 可用：授权 agent -p 跑架构 doc（无 Grok 子 agent 且 grok CLI 不可用时）
本轨跨栈 OpenCode：父 agent 不在 OpenCode 且 prompt 明文时，`opencode run -m opencode-go/deepseek-v4.1-flash`
本轨跨栈 Qoder：父不在 Qoder 时，`qodercli -p --dangerously-skip-permissions -m <list 中的非顶档>`
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
