---
title: "Loop 模型能力量化"
type: guide
status: accepted
phase: N/A
updated: 2026-09-23
summary: "各模型能力对比（单表）与费用门禁；架构设计付费最优先，架构定格是 Opus 5.5（Fable/GPT 仅点名）；无明文才降级 Grok 4.7；kimi/mimo 须授权；gemini-3.8-flash 前端实施主力。"
---

# 模型能力量化

> **用途**：Loop 父 agent 选型、方案主笔归属、弱模型如何配合强模型。
> **总原则**：**工程质量优先，兼顾费用** — 见 [overview.md § 迭代原则](overview.md#迭代原则)。
> **非绝对 benchmark**：表内数字为项目实践中的**相对档位**，随产品更新可改本文。
> **费用门禁**：**Fable 5.1、Opus 5.5、GPT 5.6**（含 Qoder **Ultimate**）属高/极高/超极高费用档 — **无本 tick 人类显式指定不得使用**（含 Task `model`、IDE 停在贵档、`--list-models` 仅有 Ultimate、自发「觉得需要更强」、**Arch-First / 架构审查「要更强」**、**默认 `loop-prompt.txt` 正文**）。2026-07-06 贵价常驻授权已撤销。GPT 5.5 已彻底下线移除。
> **授权门禁**：**kimi-k3（中强架构审）与 mimo 2.6 pro / flash 均须明文授权**。
> **架构设计付费最优先，架构定格是 Opus 5.5**：方案 / ADR / Arch-First 先考虑付费档。付费档里**定格用 Opus 5.5**（本 tick 点名 Opus，或只授权付费/强架构、未点名另一档）。**Fable 5.1** 仅点名时做超顶格；**GPT 5.6** 仅点名时用。已点名的档不得用 Grok 顶替。未点名**不得擅自调用**付费档，此时才降级 **Grok 4.7**。审查义务本身仍**不构成**付费授权；想用付费档但无明文 → `HUMAN_DECISION_REQUIRED`。
> **执行硬铁律**：**架构/审查模型（Fable 5.1、Opus 5.5、GPT 5.6、Grok 4.7、kimi-k3）坚决不做执行、禁止写业务代码**。
> **Qoder**：Ultimate = GPT 5.6；**必须**人类写 `-m ultimate` 或 prompt 写明 `Ultimate`/`GPT 5.6` 才可用；默认实施按 `performance` 等非 Ultimate 档。
> **委派流程**见 [models-and-delegation.md](models-and-delegation.md)。

## 能力对比（单表）

相对档位：**1 = 弱 … 5 = 强**；**5.5 / 5+** 高于原 5 分顶。**费用友好：5 = 最省 … 0.5 = 最贵**。`—` = 禁止该用途。

| 模型 | 架构 | 写作 | 代码性价比 | 挖 bug | 费用友好 | prompt 授权 | 备注 |
|:-----|:---:|:---:|:----------:|:---:|:--------:|:-----------:|:-----|
| **Fable 5.1** | **5+** | 5 | **—** | 5 | 0.5 | **必须** | **超顶格架构 / 最贵**；单价高于 Opus 5.5；仅战略级重大方案/极限推演；**禁写代码** |
| **Opus 5.5** | **5.5** | 5 | **—** | 5 | 1 | **必须** | **架构定格 / 顶格强架构**；架构设计在付费档里定在这一档；单价低于 Fable 5.1；**禁写代码** |
| **GPT 5.6** | 4.2 | 3.5 | **—** | 4.2 | 2 | **必须** | 强架构；**Qoder `ultimate`** / Codex；**非** Cursor 可派档；**禁写代码**（GPT 5.5 已移除） |
| **Grok 4.7** | 3.9 | 4 | **—** | 3.8 | 2.5 | 否 | **无付费授权时的架构降级（免授权）**；子 agent 优先 Task，无档 `grok -p`（跟 CLI 默认 4.7）；**不是**架构设计首选；**不做执行** |
| **kimi-k3** | 3.9 | 3.5 | **—** | 3.8 | 3 | **必须** | 与 Grok 同档；**架构审专轨**；**只能用 kimi CLI 调用**；**不做执行**；**须授权** |
| **mimo 2.6 pro** | 3.2 | 3.5 | **4.7** | 3.8 | 2.6 | **必须** | 比 deepseek 更强更贵；适合**辅助方案**与**执行**；**须授权** |
| **deepseek-v4.1-flash** | 2.5 | 3 | **4.3** | 3.2 | 3.0 | 否 | OpenCode **`opencode-go/deepseek-v4.1-flash`**；**通用后端编码实施**；略强于 Composer |
| **mimo 2.6 flash** | 2.0 | 2.5 | 4.2 | 3.0 | 3.4 | **必须** | 价格介于 Composer 与 deepseek 之间；适合**执行**；**须授权** |
| Composer | 3 | 4.5 | 4 | 3 | 3.8 | 否 | Cursor 叙述润色默认；实施常绑；**快于 Auto** |
| **Auto** | 2.7 | 4 | 3.5 | 2.7 | **4.2** | 否 | Cursor 路由档；能力 **略弱于 Composer**；**最省费用**；**更慢** |
| **gemini-3.8-flash** | 2.5 | 3 | **4.5** | 3.5 | **4.5** | 否 | Antigravity 默认；**适合前端实施首选**，比 deepseek 更强；极低费用 |
| gemini-3.1-pro | 3.5 | 4 | 4 | 4 | 3 | 否 | Antigravity 强推理 |

**费用相对单价**（左更便宜；`<<` = 非线性加价）：

```
gemini-3.8-flash < Auto < Composer < mimo 2.6 flash < deepseek-v4.1-flash < mimo 2.6 pro < kimi-k3 ≈ Grok 4.7 << GPT 5.6 << Opus 5.5 < Fable 5.1
```

**能力档**（方案主笔规则用上表「架构」列归档）：

| 档 | 模型 | 费用档 |
|:---|:-----|:-------|
| **超顶格** | **Fable 5.1** | **超极高** — 仅本 tick **点名 Fable**；极限推演；**须 prompt 授权**；**不做执行** |
| **架构定格 / 顶格** | **Opus 5.5** | **极高** — 付费架构的定格模型；**须 prompt 授权**；**不做执行** |
| **强架构** | **GPT 5.6** | **高** — 仅本 tick **点名** GPT 5.6 / Ultimate；**须 prompt 授权**；**不做执行**（GPT 5.5 已下线移除） |
| **中强架构（降级）** | **Grok 4.7**（无付费授权时的降级）、**kimi-k3**（架构审·须授权） | 中～中（略高）；**两者均不做执行** |
| **中架构 / 辅助方案** | **mimo 2.6 pro**（辅助方案/执行·须授权）、Composer、gemini-3.1-pro、**Auto** | 中；Auto 略弱于 Composer，更省、更慢 |
| **实施执行主力** | **gemini-3.8-flash**（前端首选·免授权）、**deepseek-v4.1-flash**（后端·免授权）、**mimo 2.6 flash**（执行·须授权）、Composer | 极低～中高；**不主笔**含架构设计的方案全文 |

## 人类输入与模型声明

人类只写**当前模型 + 方向**（不写具体任务）→ **[human-input.md](human-input.md)**。
能力档按**实际绑定模型**查上表；OpenCode / Kimi slug → [cli/opencode.md](cli/opencode.md)、[cli/kimi.md](cli/kimi.md)。

## 费用维度（硬门禁）

费用与能力**独立**：架构更强 ≠ 可以默认用。Loop 以**成本可控**为默认，贵模型与特定模型是**显式 opt-in**。

### 费用档

相对单价见 [能力对比](#能力对比单表)。档位如下：

| 费用档 | 模型 | 默认可用？ | 授权方式 |
|:-------|:-----|:----------|:---------|
| **极低** | **gemini-3.8-flash** | ✅ | Antigravity 默认等；前端实施王牌 |
| **低（最省）** | **Auto** | ✅ | Cursor 路由档（Auto < Composer 单价，更慢） |
| **中低** | **Composer** | ✅ | Cursor 交互实施主力 |
| **中（须授权）** | **mimo 2.6 flash** | ❌ | 本 tick 明文（Composer < mimo flash）；适合执行 |
| **中（偏高）** | **deepseek-v4.1-flash** | ✅ | OpenCode `-m opencode-go/deepseek-v4.1-flash`（mimo flash < deepseek）；通用后端实施 |
| **中高（须授权）** | **mimo 2.6 pro** | ❌ | 本 tick 明文（deepseek < mimo pro）；比 gemini/deepseek 更强，辅助方案与执行 |
| **中高（架构降级）** | **Grok 4.7**（无付费授权时的降级）、**kimi-k3**（架构审·须授权） | 视模型 | 架构设计首选仍是付费档；Grok 仅在未授权付费档时使用；kimi 专职架构审（kimi 无 2.6，只有 k3） |
| **高** | **GPT 5.6** | ❌ | 本 tick 人类明文（Qoder `ultimate` 等） |
| **极高** | **Opus 5.5**（架构定格） | ❌ | 本 tick 人类明文 |
| **超极高** | **Fable 5.1** | ❌ | 本 tick 人类明文（单价最贵） |

### 什么算「prompt 明文授权」

以下**至少满足一条**，否则 **禁止** 使用 Fable 5.1 / Opus 5.5 / GPT 5.6 / kimi-k3 / mimo（父 agent、子 agent、跨栈 CLI 均适用）：

| ✅ 有效授权 | 示例 |
|:------------|:-----|
| 本 tick 人类 `当前模型：` 写明贵模型/需授权模型 | `当前模型：Ultimate / GPT 5.6（Qoder · 主架构）`；`当前模型：Fable 5.1（超强架构）`；`当前模型：Opus 5.5（顶格架构）`；`当前模型：kimi-k3（架构审）`；`当前模型：mimo 2.6 pro（辅助方案/执行）` |
| 本 tick 人类补充行 / Sticky 写明 | `本轨主架构授权：Opus 5.5`（架构定格）；`本轨主架构授权：Fable 5.1`（仅超顶格）；`本轨主架构授权：model=ultimate`（Qoder）或 `model=gpt-5.6`；`本轨架构审授权：kimi-k3`；`本轨执行授权：mimo 2.6 pro` |

| ❌ 不算授权 | 说明 |
|:------------|:-----|
| Agent 自行判断「任务太难」 | → `HUMAN_DECISION_REQUIRED`，不得偷偷换模型 |
| **默认 [`loop-prompt.txt`](loop-prompt.txt) 正文** | **不算**。2026-07-06 贵价常驻授权已撤销；贵价不得常驻套件文件 |
| **Arch-First / 架构审查「需要更强模型」** | **不算**授权。未明文**禁止**因此自行拉 Fable 5.1、Opus 5.5、GPT 5.6 或未经授权拉 kimi-k3。架构设计仍最优先考虑付费档：已授权则用；未授权才降级 **Grok 4.7**。想用付费档 → `HUMAN_DECISION_REQUIRED` |
| 多方评审「综合/审查用强架构」 | **不算**自行升档的授权。已授权付费档时「相对强」= 该付费档；未授权时降级 Grok 4.7 |
| 子 agent 默认「架构任务」 | 无父级明文仍用 Composer / 当前环境默认实施档 |
| 历史 tick 曾授权 | 每轮 / 每轨重新声明；未写则过期 |
| 用户未切换但 IDE / list 停在 Opus、Ultimate、GPT | loop **仍不得**用该贵档，除非本 tick 人类补充行 / `-m` **显式**写明 |
| Qoder `--list-models` 只有 Ultimate | **不算**授权；未显式指定则按 `performance`（或人类写明的其它档） |

### 无授权时的降级

| 原本想用 | 无授权时改为 |
|:---------|:-------------|
| Fable 5.1 / Opus 5.5 / GPT 5.6 主笔方案（未授权） | 降级 **Grok 4.7**（子 agent 优先，CLI 其次）；这是降级，不是架构设计首选 |
| 未授权想用 kimi-k3 架构审 | **Grok 4.7** 独立实例审查；想用 kimi 须 prompt 授权 |
| 未授权想用 mimo 2.6 pro / flash | 实施改用 **gemini-3.8-flash**（前端首选）或 **deepseek-v4.1-flash** / Composer |
| Task `model=gpt-5.6` / `opus` / `fable` / `ultimate` | **不传贵价 `model`**。架构轨：**子 agent 有 Grok 则 Task 传 Grok slug**；无档才 Shell `grok -p` |
| Arch-First 审查想用付费档但无明文 | 降级 **Grok 4.7** 独立审查；坚持用付费档 → `HUMAN_DECISION_REQUIRED` |
| 挖 bug / 根因 | **Grok 4.7**（或 Composer / gemini-3.8-flash / deepseek 等）；贵模型须明文 |
| Fable / Opus / GPT / Grok / kimi-k3 写代码 | **坚决禁止**（有授权也不行 — 架构审查模型不做执行） |

### 费用 × 任务矩阵（速查）

| 任务 | 默认（免审批 / 低中费用） | 授权通道（须明文） | 严禁行为 |
|:-----|:--------------------------|:-------------------|:---------|
| 架构 / ADR 主笔 | 无明文时降级 **Grok 4.7**（不是首选） | **定格 Opus 5.5**；Fable 5.1 / GPT 5.6 仅本 tick 点名该档 | 弱模型擅自主笔；有 Opus 授权却用 Grok 或别的付费档顶替定格 |
| **架构设计审查（Arch-First）** | 无明文时降级 **Grok 4.7 独立实例**（禁 Composer 单审） | **定格 Opus 5.5**；点名时才用 Fable / GPT 5.6；其次 **kimi-k3**（须授权） | 无明文擅自 spawn 付费档 |
| 辅助方案 / 混合设计 | Composer | **mimo 2.6 pro**（比 gemini 强·须授权） | — |
| **前端代码实施** | **gemini-3.8-flash**（比 deepseek 更强，前端首选） | **mimo 2.6 pro / flash**（须授权） | 严禁 Grok / kimi / 贵价写前端 |
| **通用后端实施** | **deepseek-v4.1-flash**（略强 Composer）、Composer | **mimo 2.6 pro / flash**（须授权） | 严禁架构/审查模型写业务代码 |
| 验收（Overall Verification） | 当前 tick **单路**收口 | ❌ 不为验收 spawn 贵模型或多份报告 | 验收多头扩散 |


## 方案文档：谁写、谁只提问

写 `dev/plans/`、`docs/architecture/`、ADR 等**含架构设计**的方案时：

### 首次起草：付费强架构最优先

**架构设计付费最优先。架构定格是 Opus 5.5。** **第一次**创建某主题的方案 / ADR / 架构 doc（尚无 accepted 正文）时：

| 优先级 | 模型 | 条件 |
|:-------|:-----|:-----|
| 1 | **Opus 5.5** | **架构定格**。本 tick 明文授权 Opus，或只授权付费/强架构且未点名另一档；**不做执行** |
| 2 | **Fable 5.1** | 仅本 tick **点名 Fable** 的超顶格；**不做执行** |
| 3 | **GPT 5.6** | 仅本 tick **点名** GPT 5.6 / Ultimate；**不做执行** |
| 4 | **Grok 4.7**（Cursor Task / CLI） | **仅当**本 tick 未授权付费档时的降级；**不是**定格；**子 agent 有 Grok 档则优先 Task**；**不做执行** |
| 5 | **kimi-k3** | 本 tick 人类 **明文授权**；**专职架构审**，亦可辅助起草；**不做执行** |
| 6 | **mimo 2.6 pro** | 本 tick 人类 **明文授权**；辅助方案与评估 |
| 7 | **Composer** | 非 Cursor / 无法用 Grok 时的降级主笔 |
| 8 | 弱档（gemini-3.8-flash、deepseek、Auto） | **不主笔**；可并行多视角**只提问题** |

已有定稿后的修订：按当前模型档分工（见下）；重大架构变更仍建议强架构主笔 + 多视角评估。

### 当前模型 = 超强 / 强架构（Fable 5.1 / Opus 5.5 / GPT 5.6）

> **前置条件**：本 tick 人类已**明文授权**使用 Fable、Opus 或 GPT 5.6（见 [费用维度](#费用维度硬门禁)）。无授权不得进入本节主笔角色。

- **你主笔**：直接起草、修改方案文档
- 可吸收他人（人类、弱模型）反馈的问题与疑惑，**由你改文档**
- **严禁写代码**：方案定稿后，实施交给当前环境执行模型

### 当前模型 = 中强架构（Grok 4.7 / kimi-k3）

- **Grok 4.7（无付费授权时的降级）**：子 agent 列表含 Grok → 用 **Task/Subagent** 传该 slug；无 Grok → 父 agent **Shell `grok -p`**（默认不传 `-m`，走本机 4.7 default）。本 tick 已授权付费档时**不**用 Grok 顶替。**不做执行**。
- **kimi-k3（架构审）**：须本 tick 授权；独立审查方案、ADR 与 Arch-First 闭环。**不做执行**。
- 若本轮另有 **Fable / Opus / GPT 5.6 主笔**，退为实施/评审辅助，**不抢改同一方案文件**

### 当前模型 = 实施执行模型（gemini-3.8-flash / deepseek-v4.1-flash / Composer / mimo 2.6 等）

- **禁止**凭自身架构判断大幅改写方案正文
- **只做**：阅读强模型（或已定稿）方案 → 提出**具体问题、疑惑、矛盾点**（带文件路径与引用）
- **专注代码实施**：gemini-3.8-flash 专攻前端与高吞吐实施，deepseek-v4.1-flash 与 Composer 专攻通用后端实施

```
弱模型 tick：读 plan → 输出「问题/疑惑清单」→ 强模型 tick：改 dev/plans/*.md
```

## 实施阶段：少纠结模型

**写代码、修 bug、补测试、勾 roadmap** 时：

- **固定**当前 Loop 环境的绑定模型（Cursor→Composer/Auto、Antigravity→gemini-3.8-flash、OpenCode→deepseek-v4.1-flash、CC→mimo 须授权）
- **禁止**每 tick 讨论「要不要换 kimi / deepseek / Composer / Grok」
- **禁止**为省费用或「试试更强」在实施中随意跨栈 CLI
- 父 agent 把时间花在 slice 质量、并行、隔离测试上，而非模型购物

详见 [overview.md § 迭代原则](overview.md#迭代原则)。

## 写代码：默认模型与硬规则

**默认：用当前环境的模型写代码** — 不为此默认跨栈。能力/费用见 [能力对比](#能力对比单表)。

| 当前 Loop 环境 | 写代码默认模型 |
|:---------------|:---------------|
| **Antigravity** | **gemini-3.8-flash**（**前端实施首选**，比 deepseek 更强，极低费用高吞吐） |
| **OpenCode** | **`-m opencode-go/deepseek-v4.1-flash`**（通用后端实施，略强于 Composer） |
| **Cursor** | **实施** `Task`（Composer / Auto） |
| **Claude Code** | **mimo 2.6 pro / mimo 2.6 flash**（**须授权**；pro 适合辅助方案与执行，flash 偏便宜执行） |
| **Qoder** | **`-m`**（常见 **`performance`** / **`efficient`** / Frontier；**勿**用 **`ultimate`** 写代码） |
| **Codex** | 本地配置 |

**硬规则**：

- **严禁用 Fable 5.1、Opus 5.5、GPT 5.6、Grok 4.7、kimi-k3 写代码（架构与审查模型不做执行）**
- **前端改码首选 gemini-3.8-flash**（比 deepseek 更强）；通用后端实施首选 deepseek-v4.1-flash / Composer
- **kimi-k3 专职架构审（只能用 kimi CLI 调用）、mimo 2.6 系列均须 prompt 授权**
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
| **默认不换 Cursor 计费模型** | 实施子 agent **不传 `model`**，与父同模型 |
| **架构 / Arch-First** | **付费档最优先**（本 tick 已明文则走人类点名的路径；Cursor **勿** Task 传贵价 `model`）。未授权才：子 agent 列表含 Grok 时传该 Grok slug；无档才 `grok -p` |
| **高费用须本 tick 人类明文** | Fable 5.1 / Opus 5.5 / GPT 5.6 是架构设计首选，仅方案/挖 bug 专轨，**不得**写代码；默认 loop-prompt **不**授权，未授权不得擅自调用 |
| **无明文** | 架构/挖 bug **降级** **Grok 4.7**；不得偷偷升付费档 |
| **想升级费用档** | `HUMAN_DECISION_REQUIRED`，等人类改 prompt |

任务默认模型见 [费用 × 任务矩阵](#费用--任务矩阵速查)。授权文案示例见 [human-input.md](human-input.md)。

## 维护

- 新模型入库：在 [能力对比](#能力对比单表) 补一行，并核对能力档 / 费用档
- 与 [models-and-delegation.md](models-and-delegation.md) 冲突时，**能力排序以本文为准**，委派规则以该文为准
