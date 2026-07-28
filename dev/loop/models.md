---
title: "Loop 模型能力量化"
type: guide
status: accepted
phase: N/A
updated: 2026-07-09
summary: "各模型在架构、写作、代码、费用等维度的相对能力排序；高费用模型须 loop prompt 明文授权。"
---

# 模型能力量化

> **用途**：Loop 父 agent 选型、方案主笔归属、弱模型如何配合强模型。  
> **总原则**：**工程质量优先，兼顾费用** — 见 [overview.md § 迭代原则](overview.md#迭代原则)。  
> **非绝对 benchmark**：项目实践中的**序关系**（高 > 低 ≈ 平），随产品更新可改本文。  
> **费用门禁**：**Opus、GPT 5.5** 属高/极高费用档 — **无 loop prompt 明文授权不得使用**（含 Task `model`、IDE 手动切换、自发「觉得需要更强」）。  
> **委派流程**见 [models-and-delegation.md](models-and-delegation.md)。

## Loop prompt：人类写什么

人类 **不** 指定本轮具体任务（不写改哪个文件、勾哪个 checkbox）。只写：

1. **当前模型**（**Claude Code / Codex 必填** slug + 运行时；**Cursor 推荐**；**OpenCode 用 `-m` 指定则不必写**）  
2. **大致方向**（范围/优先级，一两句话）

具体任务由 agent 读 status / roadmap 后**自主选取**。详见 [human-input.md](human-input.md)。

```text
当前模型：mimo-v2.5-pro（Claude Code）
方向：按 status 推进实施，优先引擎测试绿；不改架构方案正文
```

未写模型时：**Cursor** 可推断 Composer 并首轮确认；**Claude Code / Codex** 须在 prompt 写明或首轮读配置后声明。

**OpenCode** 用 **`-m provider/model`** 指定模型时（`opencode run`、`opencode -m` 启动 TUI），**不必**在 prompt 写 `当前模型：` — 能力档按 `-m` 对照 [opencode.md](runtimes/opencode.md#loop-能力档--opencode--m-对照) 查表。每轮输出仍应复述**实际** `-m`（或 `OPENCODE_MODEL`）。

| 运行时 | 模型是否固定 | 未在 prompt 写模型时 |
|:-------|:-------------|:---------------------|
| **Cursor** | 架构/挖 bug 默认 **Grok**；实施常 **Composer**（手动换模型须 prompt 同步） | 架构轨推断 Grok，实施轨可确认 Composer |
| **Claude Code** | **不固定** | 读会话配置 → 声明 `当前模型：<slug>（Claude Code）` |
| **OpenCode** | **不固定** | **有 `-m`** → 按 CLI 对照表，prompt 不写；**无 `-m`** → 读配置后声明 |
| **Antigravity** | **不固定** | 读配置或启动参数 `--model` → 声明 `当前模型：<slug>（Antigravity）` |
| **Codex** | 本地配置 | 读配置 → 声明 slug |

**Loop 每轮须可见说明当前模型**（父 agent 结尾输出；OpenCode 写 `-m` 值如 `kimi-for-coding/k2p6`）。能力与费用档按**实际绑定模型**查下表。

```bash
# OpenCode：模型在命令行，不在 prompt
opencode run -m kimi-for-coding/k2p6 --dir "$ROOT" "方向：大量改代码…"
```

**能力档**（用于方案主笔规则）：

| 档 | 模型 | 架构序 | 费用档 |
|:---|:-----|:-------|:-------|
| **强架构** | Opus、GPT 5.5 | 最高两档 | **高 / 极高** — **须 prompt 授权** |
| **中强架构** | Grok | 介于 Composer 与 GPT 5.5；可主笔一般与较复杂方案 | 中（**< deepseek**） |
| **中架构** | Composer、gemini-3.1-pro | 可主笔一般方案；复杂架构建议强/中强模型 | 中 |
| **弱架构** | mimo-v2.5-pro、deepseek-v4-pro、gemini-3.5-flash | **不主笔**含架构设计的方案全文 | 极低～中高 |
| **极弱架构** | kimi-k2.6 | **架构最低**；**禁止**主笔含架构权衡的方案 | 低 |

## 费用维度（硬门禁）

费用与能力**独立**：架构更强 ≠ 可以默认用。Loop 以**成本可控**为默认，贵模型是**显式 opt-in**。

### 费用档

**相对单价**（左更便宜，`<` 略贵，`<<` 跃迁加价）：

```
mimo-v2.5-pro  ≈  gemini-3.5-flash  <  kimi-k2.6  <  Composer  ≈  gemini-3.1-pro  <  Grok  <  deepseek-v4-pro  <<  GPT 5.5  <<  Opus
```

| 费用档 | 模型 | 默认可用？ | 授权方式 |
|:-------|:-----|:----------|:---------|
| **极低** | mimo-v2.5-pro、gemini-3.5-flash | ✅ | Claude Code / Antigravity 默认等 |
| **低** | kimi-k2.6 | ✅ | OpenCode `-m kimi-for-coding/k2p6` 等 |
| **中** | Composer、gemini-3.1-pro | ✅ | Cursor 默认 / Antigravity 指定 |
| **中（略高）** | Grok | ✅ | Cursor 指定（`当前模型：Grok`）；**低于 deepseek** |
| **中高** | deepseek-v4-pro | ✅ | OpenCode `-m deepseek/deepseek-v4-pro` 等 |
| **高** | GPT 5.5 | ❌ | loop prompt **明文** |
| **极高** | Opus | ❌ | loop prompt **明文** |

### 什么算「prompt 明文授权」

以下**至少满足一条**，否则 **禁止** 使用 GPT 5.5 / Opus（父 agent、子 agent、跨栈 CLI 均适用）：

| ✅ 有效授权 | 示例 |
|:------------|:-----|
| 人类 `当前模型：` 写明贵模型 | `当前模型：GPT 5.5（主架构）` |
| Loop Goal / [`loop-prompt.txt`](loop-prompt.txt) 或人类消息写明 | `本轨主架构授权：model=gpt-5.5` |

| ❌ 不算授权 | 说明 |
|:------------|:-----|
| Agent 自行判断「任务太难」 | → `HUMAN_DECISION_REQUIRED`，不得偷偷换模型 |
| 子 agent 默认「架构任务」 | 无父级明文仍用 Composer |
| 历史 tick 曾授权 | 每轮 / 每轨重新声明；未写则过期 |
| 用户未切换但 IDE 停在 Opus | loop 仍按 **Composer** 计，除非 prompt 写明 |

### 无授权时的降级

| 原本想用 | 无授权时改为 |
|:---------|:-------------|
| GPT 5.5 / Opus 主笔方案 | **Grok** 主笔；复杂处记 blocking question |
| Task `model=gpt-5.5` | **不传 `model`**（同父；Cursor 架构轨默认 Grok） |
| Opus / GPT 5.5 挖 bug | **Grok**（或 Composer / mimo / deepseek / kimi 等更低档） |
| GPT 5.5 / Opus 写代码 | **禁止**（有授权也不行 — 见 [代码性价比](#代码性价比)） |

### 费用 × 任务矩阵（速查）

| 任务 | 默认（低/中费用） | 高费用（须明文） |
|:-----|:------------------|:-----------------|
| 架构 / ADR 主笔 | **Grok** | GPT 5.5、Opus |
| 方案写作润色 | **Grok**（叙述亦可 Composer） | GPT 5.5（可选，仍须明文） |
| 大量改代码 | **当前环境模型**（见下） | ❌ 永不 GPT / Opus |
| 挖 bug / 根因 | **Grok 及以下**（Composer、mimo、deepseek、kimi…） | GPT 5.5、Opus（须明文） |
| 方案多视角评估 | 并行 reviewer / plan-analyst（费用可控） | 贵模型仅评估轨、不写代码 |
| 验收（Overall Verification） | 当前 tick **单路**收口 | ❌ 不为验收 spawn 贵模型或多份报告 |


## 方案文档：谁写、谁只提问

写 `dev/plans/`、`docs/architecture/`、ADR 等**含架构设计**的方案时：

### 首次起草：优先强架构

**第一次**创建某主题的方案 / ADR / 架构 doc（尚无 accepted 正文）时：

| 优先级 | 模型 | 条件 |
|:-------|:-----|:-----|
| 1 | **GPT 5.5、Opus** | loop prompt **明文授权** |
| 2 | **Grok** | **默认主笔**（Cursor）；架构介于 Composer 与 GPT 5.5；**无须**贵模型授权 |
| 3 | **Composer** | 非 Cursor / 无法用 Grok 时的降级主笔 |
| 4 | 弱档（mimo、deepseek、kimi） | **不主笔**；可并行多视角**只提问题** |

已有定稿后的修订：按当前模型档分工（见下）；重大架构变更仍建议强架构主笔 + 多视角评估。

### 当前模型 = 强架构（Opus / GPT 5.5）

> **前置条件**：loop prompt 已**明文授权**本 tick / 本轨使用 Opus 或 GPT 5.5（见 [费用维度](#费用维度硬门禁)）。无授权不得进入本节主笔角色。

- **你主笔**：直接起草、修改方案文档  
- 可吸收他人（人类、弱模型）反馈的问题与疑惑，**由你改文档**  
- 写作叙述可仍按 [写作序](#写作方案adr长文档) 润色（Composer / Grok 写作更强时，可拆轨：架构段落自写，叙述轨另委——仅 prompt 授权时）

### 当前模型 = 中强架构（Grok）

- **默认你主笔**：架构 / ADR / 方案文档（Cursor 上无贵模型授权时的**默认主笔**）  
- 架构与写作均介于 Composer 与 GPT 5.5  
- 若 loop 指定本轮另有 **GPT 5.5 / Opus 主笔**，你退为实施/评审辅助，**不与其抢改同一方案文件**

### 当前模型 = 中架构（Composer，且无更强模型在同轮主笔）

- 非 Cursor / 无法用 Grok 时，**你主笔**一般方案与架构 doc  
- 若 loop 指定本轮另有 **GPT 5.5 / Opus / Grok 主笔**，你退为实施/评审辅助，**不与其抢改同一方案文件**

### 当前模型 = 弱架构 / 极弱架构（mimo、deepseek、kimi-k2.6 等）

- **禁止**凭自身架构判断大幅改写方案正文（**kimi-k2.6 架构档最低**，尤须遵守）  
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

## 能力维度（序关系）

同一行内：**左 > 右**；`≈` 表示同一档。

### 架构设计

```
Opus  >  GPT 5.5  >  Grok  >  Composer  >  gemini-3.1-pro  >  mimo-v2.5-pro  ≈  deepseek-v4-pro  ≈  gemini-3.5-flash  >  kimi-k2.6
```

| 模型 | 档 | 说明 |
|:-----|:---|:-----|
| **Opus**（如 claude-opus-4.x） | S | 最强架构与复杂权衡；**贵**，loop 默认不用 |
| **GPT 5.5** | A | 架构 **强于 Grok / Composer**；主架构文档**仅 prompt 明文允许时**作父/主笔 |
| **Grok** | A− | Cursor **架构 / ADR 默认主笔**；架构 **介于 Composer 与 GPT 5.5**；**无须**贵模型授权 |
| **Composer** | B+ | 写作最强、代码性价比优于 Grok；架构主笔为 Grok 不可用时的降级 |
| **gemini-3.1-pro** | B+ | Antigravity 强推理模型；适合 Debug 与一般架构分析 |
| **mimo-v2.5-pro** | B | Claude Code **常见**模型；架构分析不错，偏实施 |
| **deepseek-v4-pro** | B− | OpenCode **常见**模型；中规中矩 |
| **gemini-3.5-flash** | B− | Antigravity 默认；高效率，适合代码开发与日常研究，不主笔复杂架构 |
| **kimi-k2.6** | C | **架构最低档**；OpenCode **`-m kimi-for-coding/k2p6`**；宜实施，不宜架构主笔 |

### 写作（方案、ADR、长文档）

```
Composer  >  Grok  >  GPT 5.5  >  gemini-3.1-pro  >  deepseek-v4-pro  ≈  kimi-k2.6  ≈  gemini-3.5-flash  >  mimo-v2.5-pro
```

| 模型 | 说明 |
|:-----|:-----|
| **Composer** | 写作最强；可润色 / 叙述轨；架构主笔默认让位 **Grok** |
| **Grok** | 写作 **介于 Composer 与 GPT 5.5**；Cursor 上**架构 / ADR 默认主笔** |
| **GPT 5.5** | 结构清晰；综合写作逊于 Composer / Grok |
| **gemini-3.1-pro** | 结构良好，表达逻辑清晰，适合编写中等复杂方案 |
| **deepseek-v4-pro** | 弱档中写作较好；可补章节、清单 |
| **kimi-k2.6** | 写作 **≈ deepseek**；可润色/补清单，**不**主笔含架构权衡的长文 |
| **gemini-3.5-flash** | 写作速度极快，适合生成大量基础描述或代码说明，不主笔架构长文 |
| **mimo-v2.5-pro** | 写作弱于 deepseek / kimi；宜实现向段落 |

### 代码（写代码 / 大量改代码）

**能力序**（性价比，左 > 右）：

```
mimo-v2.5-pro  ≈  gemini-3.5-flash  >  kimi-k2.6  >  Composer  ≈  gemini-3.1-pro  >  Grok  >  deepseek-v4-pro
```

**默认：用当前环境的模型写代码** — 不为此默认跨栈。

| 当前 Loop 环境 | 写代码默认模型 |
|:---------------|:---------------|
| **Cursor** | **Composer**（Task `coder`，不传 `model`）；prompt 写明时可用 **Grok**（代码性价比低于 Composer） |
| **Claude Code** | 会话绑定的 slug（常见 **mimo-v2.5-pro**） |
| **Antigravity** | **gemini-3.5-flash**（支持手动指定 `gemini-3.1-pro`） |
| **OpenCode** | **`-m`** 或会话绑定（常见 **kimi-k2.6**、**deepseek-v4-pro**） |
| **Codex** | 本地配置 |

| 模型 | 说明 |
|:-----|:-----|
| **mimo-v2.5-pro** | 费用**最低**；Claude Code 常见 |
| **gemini-3.5-flash** | 极其经济且响应迅速，工具调用能力极强，代码性价比极高 |
| **kimi-k2.6** | 费用次低；代码性价比高 |
| **Composer** | Cursor 默认；质量与费用居中；**代码性价比优于 Grok** |
| **gemini-3.1-pro** | 推理强大，改写大范围代码正确率高，价格适中 |
| **Grok** | 代码性价比 **低于 Composer**（介于 Composer 与 deepseek）；Cursor 可用，费用 **< deepseek** |
| **deepseek-v4-pro** | 可用；单价高于 Composer / Grok（见 [费用](#费用相对单价越低越好)） |

**硬规则**：

- **不要用 GPT 5.5、Opus 写代码**（贵且非实施专精）  
- **默认不跨栈**：在 Cursor 就用 Composer（或 prompt 写明的 Grok），在 Claude Code 就用当前 slug，在 OpenCode 就用当前 `-m`  
- **跨栈改码**（如 Cursor 父 agent 调 `claude -p` / `opencode run`）仅当 prompt **明文授权**或当前环境确实无法执行（记 status 原因）

### Bug 挖掘 / 根因

**能力序**（左 > 右）：

```
Opus  >  GPT 5.5  >  Grok  >  Composer  >  gemini-3.1-pro  >  mimo-v2.5-pro  ≈  deepseek-v4-pro  ≈  gemini-3.5-flash  >  kimi-k2.6
```

**默认**：**Grok 及以下**（Composer、mimo、deepseek、kimi 等）— 日常挖 bug、根因分析够用；Cursor 上**首选 Grok**。

**Opus、GPT 5.5** 能力更强但**高费用**，须 loop prompt **明文授权**（同 [费用维度](#费用维度硬门禁)）；**无授权不得**为挖 bug spawn 贵模型。有授权时可委派专轨根因分析，**仍禁止**用贵模型大量改代码。

| 模型 | 说明 |
|:-----|:-----|
| **Opus** | 根因最强；**须 prompt 授权** |
| **GPT 5.5** | 强于 Grok / Composer；**须 prompt 授权** |
| **Grok** | 挖 bug **介于 Composer 与 GPT 5.5**；Cursor **默认首选**，**无须**贵模型授权 |
| **Composer** | Grok 不可用时的降级；仍属「Grok 及以下」 |
| **gemini-3.1-pro** | 推理与上下文窗口极大，极为擅长跨文件复杂 bug 挖掘与关联分析 |
| **mimo / deepseek / kimi / gemini-3.5-flash** | 可用；复杂根因记 blocking question 或申请贵模型授权 |

### 费用（相对单价，越低越好）

从左到右**越来越贵**（`<` 略贵，`<<` 明显跃迁）：

```
mimo-v2.5-pro  ≈  gemini-3.5-flash  <  kimi-k2.6  <  Composer  ≈  gemini-3.1-pro  <  Grok  <  deepseek-v4-pro  <<  GPT 5.5  <<  Opus
```

| 模型 | 费用档 |
|:-----|:-------|
| **mimo-v2.5-pro** | **最便宜** |
| **gemini-3.5-flash** | 极低（与 mimo 相当） |
| **kimi-k2.6** | 次便宜 |
| **Composer** | 中 |
| **gemini-3.1-pro** | 中（与 Composer 相当） |
| **Grok** | 中（略高于 Composer；**低于 deepseek**） |
| **deepseek-v4-pro** | 高于 Grok / Composer |
| **GPT 5.5** | 高（须 prompt 授权） |
| **Opus** | 极高（须 prompt 授权） |

与 [费用维度硬门禁](#费用维度硬门禁) 一致。`<<` 表示相对前一档**非线性加价**。

## 速查矩阵（1=弱 … 5=强；费用 1=最贵 … 5=最省）

| 模型 | 架构 | 写作 | 代码性价比 | 挖 bug | 费用友好 | prompt 授权 |
|:-----|:---:|:---:|:----------:|:---:|:--------:|:-----------:|
| Opus | 5 | 4 | **—（禁止写代码）** | 5 | 1 | **必须** |
| GPT 5.5 | 4 | 3 | **—（禁止写代码）** | 4 | 2 | **必须** |
| Grok | 3.7 | 4 | 3.5 | 3.5 | 2.5 | 否 |
| deepseek-v4-pro | 2 | 3 | 3 | 3 | 2 | 否 |
| Composer | 3 | 5 | 4 | 3 | 3 | 否 |
| gemini-3.1-pro | 3.5 | 4 | 4 | 4 | 3 | 否 |
| kimi-k2.6 | 1 | 3 | 4.5 | 2 | 4 | 否 |
| gemini-3.5-flash | 2 | 3 | 5 | 3 | 5 | 否 |
| mimo-v2.5-pro | 3 | 2 | 5 | 3 | 5 | 否 |

数字为**相对档位**。**费用友好**：5=最便宜（mimo）→ 1=最贵（Opus/GPT 档）。与 [费用](#费用相对单价越低越好) 一致。

## Cursor 内：子 agent 与换模型

在 **Cursor** 中跑 loop 时：

| 规则 | 说明 |
|:-----|:-----|
| **可用不同 `subagent_type`** | `coder`、`explore`、`reviewer` 等 — 分工照常 |
| **默认不换 Cursor 计费模型** | 子 agent **不传 `model`**，与父 agent 同模型（Composer 或 prompt 写明的 **Grok**；见 `.cursor/rules/subagent-model-policy.mdc`） |
| **高费用须 prompt 明文** | **GPT 5.5 / Opus** 无授权 **禁止**；有授权可用于**主架构/方案文档**或**挖 bug/根因**专轨，**不得**写代码 |
| **Grok** | 默认可用（非贵模型档）；父会话写明 `当前模型：Grok` 后，子 agent 不传 `model` 即同用 Grok |
| **禁止贵模型写代码** | 有授权也不行 — 实施用**当前环境模型** |
| **无明文** | 架构/方案、挖 bug 默认 **Grok**（或更低档）；不得「偷偷」升 Opus / GPT 5.5 |
| **想升级费用档** | 输出 `HUMAN_DECISION_REQUIRED` + 建议文案，等人类改 prompt |

### Prompt 授权示例

```text
当前模型：Grok。方向：按 status 推进方案与实施
本轨主架构文档授权：子 agent 可使用 model=gpt-5.5（或 opus），仅用于 dev/plans/foo.md
本轨根因分析授权：子 agent 可使用 model=opus，仅做 bug 挖掘，不写 prod 代码
禁止：GPT 5.5 / Opus 参与写代码（实施轨只用 mimo、Composer 或 Grok）
默认轨：全部子 agent 不得传 model，保持与父相同（Composer 或 Grok）
```

### 任务 → 默认模型（Cursor loop）

| 任务 | 默认 | 高费用（须明文） |
|:-----|:-----|:-----------------|
| 主架构 / ADR 起草 | **Grok** | GPT 5.5、Opus |
| 方案写作、润色 | **Grok**（叙述亦可 Composer） | GPT 5.5 |
| 大量改代码 | **当前环境模型**（Cursor→Composer 性价比通常更好；或 Grok） | ❌ GPT / Opus |
| 挖 bug / 根因 | **Grok 及以下** | GPT 5.5、Opus |

## 其他运行时与模型

| 运行时 | 模型绑定 | 见 |
|:-------|:---------|:---|
| **Cursor** | 架构/挖 bug 默认 **Grok**；实施常 Composer；换模型须 prompt 同步 | [runtimes/cursor.md](runtimes/cursor.md) |
| **Claude Code** | **不固定** — 常见 mimo-v2.5-pro、kimi-k2.6、opus 等 | [runtimes/claude-code.md](runtimes/claude-code.md) |
| **Antigravity** | **不固定** — 常见 gemini-3.5-flash、gemini-3.1-pro | [runtimes/antigravity.md](runtimes/antigravity.md) |
| **OpenCode** | **`-m provider/model`** 指定；prompt 不必写 slug | [runtimes/opencode.md](runtimes/opencode.md) |
| **Codex** | 本地配置 | [runtimes/codex.md](runtimes/codex.md) |

Loop 须在每轮输出写明**实际模型**：Claude Code / Codex 来自 prompt 或配置；OpenCode 来自 **`-m`**（如 `kimi-for-coding/k2p6`）。勿写「OpenCode 默认 deepseek」等模糊表述。

## 维护

- 新模型入库：补一行序关系 + 速查表一行  
- 与 [models-and-delegation.md](models-and-delegation.md) 冲突时，**能力排序以本文为准**，委派规则以该文为准  
