---
title: "Loop 模型能力量化"
type: guide
status: accepted
phase: N/A
updated: 2026-08-04
summary: "各模型能力对比（单表）与费用门禁；高费用模型须 loop prompt 明文授权；Arch-First 不授权贵价。"
---

# 模型能力量化

> **用途**：Loop 父 agent 选型、方案主笔归属、弱模型如何配合强模型。  
> **总原则**：**工程质量优先，兼顾费用** — 见 [overview.md § 迭代原则](overview.md#迭代原则)。  
> **非绝对 benchmark**：表内数字为项目实践中的**相对档位**，随产品更新可改本文。  
> **费用门禁**：**Opus、GPT 5.5、GPT 5.6**（含 Qoder **Ultimate**）属高/极高费用档 — **无人类显式指定 / loop prompt 明文授权不得使用**（含 Task `model`、IDE 停在贵档、`--list-models` 仅有 Ultimate、自发「觉得需要更强」、**Arch-First / 架构审查「要更强」**）。  
> **硬规则**：**架构审查 / Arch-First /「相对强」综合 ≠ 贵价授权**。未明文时审查默认 **Grok / kimi-k3**；想用贵价 → `HUMAN_DECISION_REQUIRED`。  
> **Qoder**：Ultimate = GPT 5.6；**必须**人类写 `-m ultimate` 或 prompt 写明 `Ultimate`/`GPT 5.6` 才可用；默认实施按 `performance` 等非 Ultimate 档。  
> **委派流程**见 [models-and-delegation.md](models-and-delegation.md)。

## 能力对比（单表）

相对档位：**1 = 弱 … 5 = 强**；**费用友好：5 = 最省 … 1 = 最贵**。`—` = 禁止该用途。

| 模型 | 架构 | 写作 | 代码性价比 | 挖 bug | 费用友好 | prompt 授权 | 备注 |
|:-----|:---:|:---:|:----------:|:---:|:--------:|:-----------:|:-----|
| Opus | 5 | 4 | **—** | 5 | 1 | **必须** | 贵；默认可不用 |
| **GPT 5.6** | 4.2 | 3 | **—** | 4.2 | 2 | **必须** | 强于 5.5；**Qoder `ultimate`** / Codex；**非** Cursor 可派档；禁写代码 |
| GPT 5.5 | 4 | 3 | **—** | 4 | 2 | **必须** | 架构强于 Grok；Codex 迁移轨常见；禁写代码 |
| Grok | 3.7 | 4 | 3.5 | 3.5 | 2.5 | 否 | Cursor **架构 / ADR / 挖 bug 默认**；**快于** kimi-k3 |
| **kimi-k3** | 3.7 | 3.5 | 4 | 3.5 | 3 | 否 | 架构/挖 bug **≈ Grok**；代码 **≈ Grok**（略弱 GPT）；**慢于 Grok**；成本 **< Grok**；**前端优先** |
| gemini-3.1-pro | 3.5 | 4 | 4 | 4 | 3 | 否 | Antigravity 强推理 |
| Composer | 3 | 5 | 4 | 3 | 3 | 否 | **写作最强**；Cursor 实施常绑；**快于 Auto** |
| **Auto** | 2.7 | 4 | 3.5 | 2.7 | 3.5 | 否 | Cursor 路由档；能力 **略弱于 Composer**；**更便宜**；**更慢** |
| mimo-v2.5-pro | 3 | 2 | 5 | 3 | 5 | 否 | CC 常见；代码性价比最高档 |
| deepseek-v4-pro | 2 | 3 | 3 | 3 | 2 | 否 | OpenCode / Qoder Frontier 常见；单价高于 Grok |
| gemini-3.5-flash | 2 | 3 | 5 | 3 | 5 | 否 | Antigravity 默认；偏实施 |
| kimi-k2.6 | 1 | 3 | 4.5 | 2 | 4 | 否 | **旧档**（OpenCode `k2p6` 等）；架构弱，勿与 **k3** 混用 |

**费用相对单价**（左更便宜；`<<` = 非线性加价）：

```
mimo ≈ gemini-3.5-flash < kimi-k2.6 < Auto < Composer ≈ gemini-3.1-pro ≈ kimi-k3 < Grok < deepseek << GPT 5.5 ≈ GPT 5.6 << Opus
```

**能力档**（方案主笔规则用上表「架构」列归档）：

| 档 | 模型 | 费用档 |
|:---|:-----|:-------|
| **强架构** | Opus、GPT 5.6、GPT 5.5 | **高 / 极高** — **须 prompt 授权** |
| **中强架构** | Grok、**kimi-k3** | 中（kimi-k3 **< Grok**；均 **< deepseek**） |
| **中架构** | Composer、gemini-3.1-pro、**Auto** | 中（Auto **略弱于** Composer，更省、更慢） |
| **弱架构** | mimo-v2.5-pro、deepseek-v4-pro、gemini-3.5-flash | 极低～中高；**不主笔**含架构设计的方案全文 |
| **极弱架构** | kimi-k2.6（旧） | 低；**禁止**主笔含架构权衡的方案 |

## 人类输入与模型声明

人类只写**当前模型 + 方向**（不写具体任务）→ **[human-input.md](human-input.md)**。  
能力档按**实际绑定模型**查上表；OpenCode / Kimi slug → [cli/opencode.md](cli/opencode.md)、[cli/kimi.md](cli/kimi.md)。

## 费用维度（硬门禁）

费用与能力**独立**：架构更强 ≠ 可以默认用。Loop 以**成本可控**为默认，贵模型是**显式 opt-in**。

### 费用档

相对单价见 [能力对比](#能力对比单表)。档位如下：

| 费用档 | 模型 | 默认可用？ | 授权方式 |
|:-------|:-----|:----------|:---------|
| **极低** | mimo-v2.5-pro、gemini-3.5-flash | ✅ | Claude Code / Antigravity 默认等 |
| **低** | kimi-k2.6（旧） | ✅ | OpenCode `-m kimi-for-coding/k2p6` 等 |
| **中** | **Auto**、Composer、gemini-3.1-pro、**kimi-k3** | ✅ | Cursor（Auto **< Composer 单价**，更慢）；Antigravity；Kimi / OpenCode k3 |
| **中（略高）** | Grok | ✅ | Cursor 指定（`当前模型：Grok`）；**低于 deepseek**；**快于** kimi-k3 |
| **中高** | deepseek-v4-pro | ✅ | OpenCode `-m deepseek/deepseek-v4-pro`；Qoder Frontier 等 |
| **高** | GPT 5.5、**GPT 5.6** | ❌ | loop prompt **明文** |
| **极高** | Opus | ❌ | loop prompt **明文** |

### 什么算「prompt 明文授权」

以下**至少满足一条**，否则 **禁止** 使用 GPT 5.5 / GPT 5.6 / Opus（父 agent、子 agent、跨栈 CLI 均适用）：

| ✅ 有效授权 | 示例 |
|:------------|:-----|
| 人类 `当前模型：` 写明贵模型 | `当前模型：Ultimate / GPT 5.6（Qoder · 主架构）`；`当前模型：GPT 5.5（主架构）` |
| Loop Goal / [`loop-prompt.txt`](loop-prompt.txt) 或人类消息写明 | `本轨主架构授权：model=ultimate`（Qoder）或 `model=gpt-5.6` |

| ❌ 不算授权 | 说明 |
|:------------|:-----|
| Agent 自行判断「任务太难」 | → `HUMAN_DECISION_REQUIRED`，不得偷偷换模型 |
| **Arch-First / 架构审查「需要更强模型」** | **不算**授权。审查义务只要 ≥中强（默认 **Grok / kimi-k3**）；**禁止**因此 spawn GPT 5.5/5.6、Opus、Qoder Ultimate（含 Task `model=`、跨栈 CLI）。想用贵价 → `HUMAN_DECISION_REQUIRED` |
| 多方评审「综合/审查用强架构」 | **不算**贵价授权。「相对强」= Grok 等中强；≠ GPT / Opus / Ultimate |
| 子 agent 默认「架构任务」 | 无父级明文仍用 Composer / 当前环境默认实施档 |
| 历史 tick 曾授权 | 每轮 / 每轨重新声明；未写则过期 |
| 用户未切换但 IDE / list 停在 Opus、Ultimate、GPT | loop **仍不得**用该贵档，除非本 tick prompt / `-m` **显式**写明 |
| Qoder `--list-models` 只有 Ultimate | **不算**授权；未显式指定则按 `performance`（或人类写明的其它档） |

### 无授权时的降级

| 原本想用 | 无授权时改为 |
|:---------|:-------------|
| GPT 5.5 / GPT 5.6 / Opus 主笔方案 | **Grok** 主笔；复杂处记 blocking question |
| Task `model=gpt-5.6` / `gpt-5.5` / `opus` / `ultimate` | **不传贵价 `model`**（同父；Cursor 架构轨默认 Grok）。Arch-First 审查例外只允许传**中强**（如 Grok），**不含**贵价 |
| Arch-First 审查想用贵价 | **Grok / kimi-k3** 审查；贵价须另获明文，否则 `HUMAN_DECISION_REQUIRED` |
| Opus / GPT 挖 bug | **Grok** 或 **kimi-k3**（或 Composer / mimo / deepseek 等更低档） |
| GPT / Opus 写代码 | **禁止**（有授权也不行 — 见上表「代码性价比」列） |

### 费用 × 任务矩阵（速查）

| 任务 | 默认（低/中费用） | 高费用（须明文） |
|:-----|:------------------|:-----------------|
| 架构 / ADR 主笔 | **Grok** 或 **kimi-k3**（同档） | GPT 5.6、GPT 5.5、Opus |
| 方案写作润色 | **Grok**（叙述亦可 Composer） | GPT（可选，仍须明文） |
| 大量改代码 | **当前环境模型**（见下）；**前端优先 kimi-k3** | ❌ 永不 GPT / Opus |
| 挖 bug / 根因 | **Grok / kimi-k3** 及以下（Composer、mimo、deepseek…） | GPT、Opus（须明文） |
| 方案多视角评估 | 并行 reviewer / plan-analyst（费用可控） | 贵模型仅评估轨、不写代码 |
| **架构设计审查（Arch-First）** | **Grok / kimi-k3**（默认）；**禁止** Composer 单审；**审查义务 ≠ 贵价授权** | GPT、Opus、Ultimate（**仅**本 tick/本轨明文；否则不得拉） |
| 验收（Overall Verification） | 当前 tick **单路**收口 | ❌ 不为验收 spawn 贵模型或多份报告 |


## 方案文档：谁写、谁只提问

写 `dev/plans/`、`docs/architecture/`、ADR 等**含架构设计**的方案时：

### 首次起草：优先强架构

**第一次**创建某主题的方案 / ADR / 架构 doc（尚无 accepted 正文）时：

| 优先级 | 模型 | 条件 |
|:-------|:-----|:-----|
| 1 | **GPT 5.6、GPT 5.5、Opus** | loop prompt **明文授权** |
| 2 | **Grok**、**kimi-k3** | **默认主笔**（同档）；**无须**贵模型授权 |
| 3 | **Composer** | 非 Cursor / 无法用 Grok·k3 时的降级主笔 |
| 4 | 弱档（mimo、deepseek、kimi-k2.6 旧） | **不主笔**；可并行多视角**只提问题** |

已有定稿后的修订：按当前模型档分工（见下）；重大架构变更仍建议强架构主笔 + 多视角评估。

### 当前模型 = 强架构（Opus / GPT 5.6 / GPT 5.5）

> **前置条件**：loop prompt 已**明文授权**本 tick / 本轨使用 Opus 或 GPT（见 [费用维度](#费用维度硬门禁)）。无授权不得进入本节主笔角色。

- **你主笔**：直接起草、修改方案文档  
- 可吸收他人（人类、弱模型）反馈的问题与疑惑，**由你改文档**  
- 写作叙述可按上表「写作」列拆轨润色（Composer / Grok 写作更强时：架构段落自写，叙述轨另委——仅 prompt 授权时）

### 当前模型 = 中强架构（Grok / kimi-k3）

- **默认你主笔**：架构 / ADR / 方案文档（无贵模型授权时的**默认主笔**）  
- kimi-k3 定位见 [能力对比](#能力对比单表) 备注；若本轮另有 **GPT / Opus 主笔**，退为实施/评审辅助，**不抢改同一方案文件**

### 当前模型 = 中架构（Composer / Auto，且无更强模型在同轮主笔）

- **Composer**：非 Cursor / 无法用 Grok·k3 时，或 Cursor 实施/写作主笔  
- **Auto**：Cursor 省费用实施档；能力略弱于 Composer，适合成本敏感改码；**不要**单独做架构终审  
- 若本轮另有更强主笔，退为实施/评审辅助，**不抢改同一方案文件**

### 当前模型 = 弱架构 / 极弱架构（mimo、deepseek、kimi-k2.6 旧等）

- **禁止**凭自身架构判断大幅改写方案正文（**k2.6 旧档**尤须遵守；勿与 **k3** 混淆）  
- **只做**：阅读强模型（或已定稿）方案 → 提出**具体问题、疑惑、矛盾点**（带文件路径与引用）  
- **反馈渠道**：交给强架构模型（同轮 Task 且 prompt 授权 `model`、或跨栈委派、或留给下一轮强模型 tick）  
- **由强模型改方案文档**；你可在强模型改完后做**实现向**补充（测试命令、文件列表）若 prompt 允许，但不改架构结论

```
弱模型 tick：读 plan → 输出「问题/疑惑清单」→ 强模型 tick：改 dev/plans/*.md
```

### 方案阶段 vs 实施阶段

| 阶段 | 弱模型 | 强/中架构模型 |
|:-----|:-------|:--------------|
| **写方案（首次）** | 并行多视角只反馈问题 | **强架构优先**主笔 |
| **写代码** | **当前环境模型**；**禁止** GPT / Opus；**禁止每 tick 重议选型** | 同左 |
| **验收** | Overall Verification **单路**收口 | 同左；不为验收多 spawn 评审报告 |

## 实施阶段：少纠结模型

**写代码、修 bug、补测试、勾 roadmap** 时：

- **固定**当前 Loop 环境的绑定模型（Cursor→Composer 或 prompt 写明的 Grok、CC→会话 slug、OpenCode→`-m`）  
- **禁止**每 tick 讨论「要不要换 kimi / deepseek / Composer / Grok」  
- **禁止**为省费用或「试试更强」在实施中跨栈 CLI  
- 父 agent 把时间花在 slice 质量、并行、隔离测试上，而非模型购物  

详见 [overview.md § 迭代原则](overview.md#迭代原则)。

## 写代码：默认模型与硬规则

**默认：用当前环境的模型写代码** — 不为此默认跨栈。能力/费用见 [能力对比](#能力对比单表)。

| 当前 Loop 环境 | 写代码默认模型 |
|:---------------|:---------------|
| **Cursor** | **Composer**（实施常绑）或 **Auto**（更省、更慢、略弱）；Task 默认不传贵 `model`；架构轨 prompt 写明时用 **Grok** |
| **Claude Code** | 会话绑定的 slug（常见 **mimo-v2.5-pro**） |
| **Qoder** | **`-m`**（常见 **`performance`** / **`efficient`** / Frontier；**勿**用 **`ultimate`** 写代码） |
| **Antigravity** | **gemini-3.5-flash**（可指定 `gemini-3.1-pro`） |
| **OpenCode** | **`-m`**（**k3**：`kimi-for-coding/k3`；旧档 `k2p6`；亦常见 deepseek） |
| **Kimi Code CLI** | **`kimi-code/k3`**（`kimi --yolo`）；**前端优先** |
| **Codex** | 本地配置 |

**硬规则**：

- **不要用 GPT 5.5、GPT 5.6、Opus 写代码**（有授权也不行）  
- **挖 bug 默认 Grok / kimi-k3 及以下**；贵模型须 prompt 明文且仍禁大量改代码  
- **前端改码优先 kimi-k3**（见能力表备注）  
- **默认不跨栈**；跨栈仅 prompt **明文授权**或当前环境无法执行（记 status）→ [external-cli.md](external-cli.md)

运行时选型简表 → [runtimes/INDEX.md](runtimes/INDEX.md)。slug / 命令 → [cli/INDEX.md](cli/INDEX.md)。

### GPT 5.6 slug 速查（按运行时）

| 运行时 | 典型标识 |
|:-------|:---------|
| **Qoder** | **`ultimate`**（`--list-models` → `Ultimate`）= **GPT 5.6** |
| **Cursor Task** | `gpt-5.6-sol-medium`、`gpt-5.6-terra-medium` 等 |
| **Codex** | `gpt-5.6-sol`、`gpt-5.6-terra`、`gpt-5.6-luna` |

## Cursor 内：子 agent 与换模型

在 **Cursor** 中跑 loop 时：

| 规则 | 说明 |
|:-----|:-----|
| **可用不同 `subagent_type`** | `coder`、`explore`、`reviewer` 等 — 分工照常 |
| **默认不换 Cursor 计费模型** | 子 agent **不传 `model`**，与父同模型（见 `.cursor/rules/subagent-model-policy.mdc`） |
| **高费用须 prompt 明文** | GPT 5.5 / GPT 5.6 / Opus 仅方案/挖 bug 专轨，**不得**写代码 |
| **无明文** | 架构/挖 bug 默认 **Grok**；不得偷偷升贵模型 |
| **想升级费用档** | `HUMAN_DECISION_REQUIRED`，等人类改 prompt |

任务默认模型见 [费用 × 任务矩阵](#费用--任务矩阵速查)。授权文案示例见 [human-input.md](human-input.md)。

## 维护

- 新模型入库：在 [能力对比](#能力对比单表) 补一行，并核对能力档 / 费用档  
- 与 [models-and-delegation.md](models-and-delegation.md) 冲突时，**能力排序以本文为准**，委派规则以该文为准  
