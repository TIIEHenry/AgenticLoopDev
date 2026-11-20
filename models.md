---
title: "Loop 模型能力量化"
type: guide
status: accepted
phase: N/A
updated: 2026-11-19
summary: "各 CLI 现行模型与费用门禁。架构定格仍是 Opus 5.5；超顶格现行 Fable 5.2；Codex 日常是 gpt-6.2-sol；Cursor 实施是 Composer 2.5；Kimi 旗舰是 K3.1 Pro；AGY 强档是 Gemini 4。"
---

# 模型能力量化

> **用途**：Loop 父 agent 选型、方案主笔归属、弱模型如何配合强模型。
> **总原则**：**工程质量优先，兼顾费用** — 见 [overview.md § 迭代原则](overview.md#迭代原则)。
> **非绝对 benchmark**：表内数字为项目实践中的**相对档位**。2026-11-19 新进行按官网定位和 [Cursor 标价](https://cursor.com/docs/models-and-pricing) 插进原表，不是新一轮对照实测。
> **目录核对日**：2026-11-19。来源见 [CLI 现行目录](#cli-现行目录2026-11-19)。
> **费用门禁**：下列模型**无本 tick 人类显式指定不得使用**（含 Task `model`、IDE 停在贵档、`--list-models` 只有贵档、自发「觉得需要更强」、Arch-First「要更强」、默认 `loop-prompt.txt`）：**Fable 5.2、Fable 5.1、Opus 5.5、GPT-6.2 Astra、GPT-5.6 Sol、GPT-5.6 Terra、Gemini 4 Neon、Gemini 4 Carbon、Gemini 4 Argon、Qoder Ultimate**。2026-07-06 贵价常驻授权已撤销。
> **授权门禁**：**Kimi K3.1 Pro、k3**（架构审）与 **mimo 2.6 pro / flash**、以及 Kimi 的执行档（`k3-256k`、`kimi-for-coding`）**均须明文授权**。
> **架构设计付费最优先，架构定格是 Opus 5.5**：方案 / ADR / Arch-First 先考虑付费档。付费档里**定格用 Opus 5.5**。**Fable 5.2** 是现行超顶格，仅点名时用（点名 Fable 5.1 仍可用，但是上一档、Cursor 默认隐藏）。**GPT-6.2 Astra** 与 **GPT-5.6 Sol** 仅点名时用。已点名的档不得用 Grok 顶替。未点名不得擅自调用，此时才降级 **Grok 4.7**。想用付费档但无明文 → `HUMAN_DECISION_REQUIRED`。
> **执行硬铁律**：架构/审查模型**禁止写业务代码**。名单：**Fable 5.2 / 5.1、Opus 5.5、GPT-6.2 Astra、GPT-5.6 Sol、GPT-5.6 Terra、Gemini 4 Neon / Carbon / Argon、Grok 4.7、Kimi K3.1 Pro、k3**。
> **Qoder**：只登记档位，不登记具体型号，也不把顶档映射到其他 CLI 的某一代。`ultimate` 须人类点名，不写代码。实施用本机 `qodercli --list-models` 里的非顶档。旧档名 `performance` 不再当作现行档。
> **委派流程**见 [models-and-delegation.md](models-and-delegation.md)。

## 能力对比（单表）

相对档位：**1 = 弱 … 5 = 强**；**5.5 / 5+** 高于原 5 分顶。**费用友好：5 = 最省 … 0.5 = 最贵**。`—` = 禁止该用途。

GPT-6.2 与 Kimi K3.1 Pro 没有放进分数表：Codex 文档没有给出可与 Cursor 标价对齐的单价，K3.1 也没有进入 Cursor 价目。它们的门禁在 [目录](#cli-现行目录2026-11-19) 和下面的档位表里。

| 模型 | 架构 | 写作 | 代码性价比 | 挖 bug | 费用友好 | prompt 授权 | 备注 |
|:-----|:---:|:---:|:----------:|:---:|:--------:|:-----------:|:-----|
| **Fable 5.2** | **5+** | 5 | **—** | 5 | 0.6 | **必须** | **现行超顶格**。Cursor 标价输入 $8 / 输出 $40，约为 Opus 5.5 的 2 倍，比 Fable 5.1 低约 20%。**禁写代码** |
| **Fable 5.1** | **5+** | 5 | **—** | 5 | 0.5 | **必须** | 上一档。Cursor 价目默认隐藏。点名仍可用。**禁写代码** |
| **Opus 5.5** | **5.5** | 5 | **—** | 5 | 1 | **必须** | **架构定格**。Cursor 标价输入 $4 / 输出 $20。**禁写代码** |
| **GPT-5.6 Sol** | 4.2 | 3.5 | **—** | 4.2 | 2 | **必须** | Cursor 现行 GPT 旗舰（输出 $20，页面写明促销至 2026-11-21）。**禁写代码**。Cursor 价目没有 GPT-6 |
| **Gemini 4 Neon** | 4.0 | 4 | **—** | 4.0 | 2.6 | **必须** | AGY 上含该模型的套餐里，新对话默认模型。Cursor 输出 $15。**禁写代码** |
| **Gemini 4 Carbon** | 3.8 | 3.8 | **—** | 3.8 | 2.6 | **必须** | Ultra / Enterprise。介绍价到 2026-11-30，之后 Cursor 输出 $20。**禁写代码** |
| **Gemini 4 Argon** | 3.7 | 3.6 | **—** | 3.7 | 2.6 | **必须** | Pro（付费或指定试用）/ Ultra / Enterprise。**禁写代码** |
| **Grok 4.7** | 3.9 | 4 | **—** | 3.8 | 2.5 | 否 | **无付费授权时的架构降级**。xAI 与 Cursor 的现行旗舰；同池还有 4.6、4.5。子 agent 优先 Task，无档才 `grok -p`（不硬编 `-m`）。**不做执行** |
| **kimi-k3** | 3.9 | 3.5 | **—** | 3.8 | 3 | **必须** | 上一档旗舰。现行旗舰是 **K3.1 Pro**，授权和禁写代码与本行相同。**只能用 kimi CLI** |
| **GPT-5.6 Terra** | 3.6 | 3.5 | **—** | 3.6 | 2.8 | **必须** | Cursor 中档 GPT（输出 $12）。**禁写代码** |
| gemini-3.1-pro | 3.5 | 4 | 4 | 4 | 3 | 否 | AGY 上只剩 Enterprise。不要再当 AGY 默认强档 |
| **mimo 2.6 pro** | 3.2 | 3.5 | **4.7** | 3.8 | 2.6 | **必须** | 2026-11-19 的 Cursor 价目没有 MiMo。规则不变：辅助方案与执行，须授权 |
| **Gemini 4 Hydrogen** | 3.0 | 3.2 | **4.4** | 3.4 | 3.2 | 否 | AGY Pro 及以上的官方执行档，也是 Orchestrator 的实现模型。Free / Plus 没有 |
| **deepseek-v4.1-flash** | 2.5 | 3 | **4.3** | 3.2 | 3.0 | 否 | OpenCode **`opencode-go/deepseek-v4.1-flash`**。Cursor 价目仍有此模型（默认隐藏）。通用后端实施 |
| **gemini-3.8-flash** | 2.5 | 3 | **4.5** | 3.5 | **4.5** | 否 | AGY **全套餐**都有，含 Free / Plus。前端与免费档实施默认。Cursor 输出 $3.75 |
| **GPT-5.6 Luna** | 2.2 | 3 | 4 | 2.5 | **4.4** | 否 | 便宜高量（输出 $1.2）。可执行，不主笔架构。Cursor 上属第三方，Plus / Free 没有 |
| **mimo 2.6 flash** | 2.0 | 2.5 | 4.2 | 3.0 | 3.4 | **必须** | 执行档，须授权 |
| **Composer 2.5** | 3 | 4.5 | 4 | 3 | 3.8 | 否 | Cursor 实施默认。标价输入 $0.5 / 输出 $2.5。**不要默认 Fast**（Fast 输出 $15） |
| **Auto** | 2.7 | 4 | 3.5 | 2.7 | **4.2** | 否 | Cursor 路由。个人套餐只有 **Cost**。Teams 的 Balance / Intelligence 可能路由到第三方并另外计费，实施不要靠它摸到 Fable / Opus |

**输出单价**（美元 / 百万 token，Cursor 价目 2026-11-19；左更便宜）：

```
GPT-5.6 Luna $1.2 < Composer 2.5 $2.5 < gemini-3.8-flash $3.75 < Grok 4.7 $6 < Gemini 4 Hydrogen $7.5 < Gemini 4 Argon / Carbon 介绍价 $10 < GPT-5.6 Terra $12 < Gemini 4 Neon = Kimi K3 $15 < GPT-5.6 Sol = Opus 5.5 $20 < Fable 5.2 $40 < Fable 5.1 $50
```

Carbon 自 2026-12-01 起输出 $20。Grok 4.7 在 xAI API 上以 200k prompt 为长上下文分界；Cursor 价目写的是超过 256k 两倍、上限 500k。Auto 没有固定单价。

**能力档**：

| 档 | 模型 | 费用档 |
|:---|:-----|:-------|
| **超顶格** | **Fable 5.2**（现行）；Fable 5.1 仅点名上一档 | **超极高** — 须点名；**不做执行** |
| **架构定格** | **Opus 5.5** | **极高** — 须点名；**不做执行** |
| **强架构** | **GPT-6.2 Astra**、**GPT-5.6 Sol**、**Gemini 4 Neon** | **高** — 须点名；**不做执行** |
| **中强架构** | **Grok 4.7**（无付费授权时的降级）、**K3.1 Pro / k3**（须授权）、Gemini 4 Carbon / Argon、GPT-5.6 Terra | 中高；除 Grok 外须点名或授权；**不做执行** |
| **中架构 / 辅助** | mimo 2.6 pro（须授权）、Composer 2.5、Auto（Cost）、gemini-3.1-pro（仅 Enterprise） | 中 |
| **实施** | **gemini-3.8-flash**（全套餐）、**Gemini 4 Hydrogen**（AGY Pro+）、**Composer 2.5**、**deepseek-v4.1-flash**、GPT-5.6 Luna / `gpt-6-luna`、Kimi 执行档（须授权）、**gpt-6.2-sol**（仅当父会话已经是 Codex 的这个模型） | 极低～中；**不主笔**架构全文 |

## CLI 现行目录（2026-11-19）

账号、套餐和客户端版本会少掉其中一部分。命令里的 id 以本机 `grok models`、`agy models`、Codex `/model`、Kimi 登录后写入的 `config.toml` 为准。

### Codex

来源：[Models | ChatGPT Learn](https://learn.chatgpt.com/docs/models)。

| 模型 | 文档中的 id | Loop |
|:-----|:------------|:-----|
| GPT-6.2 Astra | 正文称为 GPT-6.2 Astra；与 Sol 同组。id 以 `/model` 为准 | **强架构**。须点名。**禁写代码** |
| GPT-6.2 Sol | `gpt-6.2-sol` | 官方日常编码推荐。父会话已经绑这个模型时，按当前环境写代码。跨栈 spawn 仍须点名 |
| GPT-6.1 Terra | `gpt-6.1-terra` | 写作、看图、电脑操作。CLI **0.159.0+**。父会话已绑定时可执行 |
| GPT-6.1 Sol | `gpt-6.1-sol` | ChatGPT 登录的 Codex 上，GPT-5.5 的替换档（Plus 及以上）。要和 IDE 扩展共用配置时，文档举例用这个 id |
| GPT-6 Luna | `gpt-6-luna` | 便宜高量。Free / Go 的替换档 |
| GPT-6 Sol | `gpt-6-sol` | 文档给出的 `gpt-5.4` 替换 id |

`~/.codex/config.toml` 的现行示例是 `model = "gpt-6.2-sol"`。上下文：GPT-6.2 Astra / Sol 最高 1M；GPT-6.1 Sol 在 Codex 里默认 500k。

ChatGPT 登录的 Codex 已退役：`gpt-5.5`（2026-10-14）、`gpt-5.4` / `gpt-5.4-mini`（2026-08-31）、`gpt-5.3-codex-spark`（2026-09-14）。`gpt-5.2` 与 `gpt-5.3-codex` 已弃用。API key 会话不受这批 ChatGPT 退役影响，Loop 仍然不选 `gpt-5.5`。

```bash
codex --model gpt-6.2-sol
codex exec -m gpt-6.2-sol "Review the current changes"
```

### Cursor

来源：[Models & Pricing](https://cursor.com/docs/models-and-pricing)。

套餐内模型：**Grok 4.7、Grok 4.6、Grok 4.5、Composer 2.5**。Plus / Free 只有这四类，没有 Auto、没有第三方。

第三方（Premium 及以上，按 API 标价从预付额度扣）里，价目表直接列出且未标 Hidden 的现行档包括：Fable 5.2、Opus 5.5、Sonnet 5.5、Haiku 5.5、GPT-5.6 Sol / Terra / Luna、Gemini 4 Neon / Carbon / Argon / Hydrogen、Gemini 3.8 Flash、Gemini 3.1 Pro。**没有 GPT-6。** Fable 5.1、Opus 5、GPT-5.5 仍在表里但默认隐藏。

Task 不传贵价 slug。未授权架构降级时，传列表里**版本最新**的 Grok slug。2026-11-19 的一次会话里见过 `grok-4.7-xhigh` 和 `cursor-grok-4.6-high-fast`，以当时列表为准，不要钉死 4.6。实施默认 **Composer 2.5**（`composer-2.5`），不要默认 `composer-2.5-fast`。

Auto 的路由池会变。帮助中心曾写路由包含 GPT-5.5、Opus 5、Grok 4.6、Fable 5，并要求池里留着 Grok 4.6。个人套餐只用 Cost。

### Grok CLI

来源：[Grok Models](https://docs.x.ai/developers/models)、[CLI reference](https://docs.x.ai/build/cli/reference)。

代码和对话的推荐仍是 **Grok 4.7**（`grok-4.7`）。上下文 500k。API 标价：prompt 小于 200k 时输入 $2 / 缓存 $0.5 / 输出 $6；达到 200k 后整单按两倍。知识截止 2026-05。同页还有 `grok-4.6`、`grok-4.5`、`grok-4.3`、`grok-4.20-*`、`grok-build-0.1`。

```bash
grok models
grok --no-plan --permission-mode bypassPermissions --always-approve -p "$prompt"
```

Loop 不传 `-m`，除非本 tick 人类写了 slug。

### Kimi Code

来源：[Kimi Code Overview](https://www.kimi.com/code/docs/en/)。CLI 别名沿用配置文档里的 `kimi-code/<模型 ID>`，以 `/login` 写进 `~/.kimi-code/config.toml` 的键为准。

| 模型 ID | 说明 | Loop |
|:--------|:-----|:-----|
| `k3.1-pro` | 现行旗舰。Moderato / Plus 起；Allegretto / Pro 起开到 1M。思考强制，默认 `max` | **架构审**。须授权。**禁写代码**。别名按惯例为 `kimi-code/k3.1-pro` |
| `k3.1-pro-highspeed` | Allegretto / Pro 起。大约 2–3 倍速度、约 2 倍额度，1M | 与 K3.1 Pro 同一条禁写代码规则 |
| `k3` | 上一档旗舰。`low` / `high` / `max` | 同上。`kimi-code/k3` |
| `k3-256k` | 256k 内与 k3 同结果；1M 的 k3 大约多一倍额度 | 须授权后**可以执行** |
| `kimi-for-coding` | K2.8 Preview | 须授权后可以执行。官方子代理说明把它当作日常改码 |
| `kimi-for-coding-highspeed` | K2.7 Code HighSpeed | 须授权后可以执行 |

配置文档里的示例默认仍可能是 `kimi-code/k3`。点名架构审时优先 K3.1 Pro；本机配置没有这个键就不要手写一个未登录的别名。

### Antigravity（`agy`）

来源：[Choose a model](https://antigravity.google/docs/models/)。

| 模型 | 套餐 | CLI | Loop |
|:-----|:-----|:----|:-----|
| Gemini 4 Neon | Pro（付费或指定试用）/ Ultra / Enterprise。Free / Plus 没有 | `--model gemini-4-neon-xhigh`；思考 `low` / `medium` / `high` / `xhigh`。上下文最高 512k | 含该模型时，**没选过模型的新对话默认就是它**。须点名才拿来做架构。**禁写代码** |
| Gemini 4 Carbon | Ultra / Enterprise | `agy models` | 须点名。**禁写代码** |
| Gemini 4 Argon | 与 Neon 同一档套餐 | `agy models` | 须点名。**禁写代码** |
| Gemini 4 Hydrogen | Pro（非试用付费）/ Ultra / Enterprise | 思考档同上，id 以 `agy models` 为准 | **官方执行档**。不必再单独写「授权 Gemini 4」 |
| Orchestrator (Neon / Carbon / Argon) | 与对应规划模型相同；Enterprise 表上没有 Orchestrator | `agy --model "Orchestrator (Neon)"`。`--effort` 无效 | 规划模型出计划，Hydrogen 改代码。付费套餐的日常实施可以用 |
| Gemini 3.8 Flash | **含 Free / Plus 的全部套餐** | 继续用 `gemini-3.8-flash`；本机若只有分档 id，用 `agy models` 列出的那条 | Free / Plus 的实施默认 |
| Gemini 3.7 / 3.6 Flash、Gemini 3.1 Pro | 仅 Enterprise | — | 不要当默认 |
| Claude Opus 5.5 / Sonnet 5.5 thinking | Pro 付费 / Ultra / Enterprise | `agy models` | 仍走 Opus / 会话模型门禁，不因为出现在 AGY 里就免授权 |
| Claude Opus 4.6 / Sonnet 4.6、GPT-OSS-120b | 页面仍标 2026-11-18 移除 | — | 不要当默认 |

Loop 的 `agy -p` **必须带 `--model`**。不带的话，有 Neon 的套餐会把新会话开在 Neon 上。

```bash
agy --model gemini-3.8-flash --dangerously-skip-permissions -p "$prompt"
agy --model "Orchestrator (Neon)" --dangerously-skip-permissions -p "$prompt"
```

## 人类输入与模型声明

人类只写**当前模型 + 方向** → **[human-input.md](human-input.md)**。

## 费用维度（硬门禁）

费用与能力独立。贵模型和 Kimi / MiMo 是显式 opt-in。

| 费用档 | 模型 | 默认可用？ | 授权方式 |
|:-------|:-----|:----------|:---------|
| **极低** | gemini-3.8-flash、GPT-5.6 Luna / `gpt-6-luna` | ✅ | 全套餐或便宜档。Luna 在 Cursor 上仍要 Premium 才有第三方 |
| **低** | Composer 2.5、Auto Cost | ✅ | Cursor 实施。不要默认 Composer Fast |
| **中** | Gemini 4 Hydrogen、deepseek-v4.1-flash | ✅ | Hydrogen 仅 AGY Pro+；deepseek 走 OpenCode |
| **中（须授权）** | mimo 2.6、Kimi `k3-256k` / `kimi-for-coding` | ❌ | 本 tick 明文后可执行 |
| **中高（架构降级）** | Grok 4.7 | ✅ 降级通道 | 未授权付费档时用。不做执行 |
| **中高（须授权）** | K3.1 Pro、k3 | ❌ | 架构审。禁写代码 |
| **高** | GPT-6.2 Astra、GPT-5.6 Sol、GPT-5.6 Terra、Gemini 4 Neon / Carbon / Argon、Qoder Ultimate | ❌ | 本 tick 点名。禁写代码 |
| **极高** | Opus 5.5 | ❌ | 架构定格。本 tick 点名 |
| **超极高** | Fable 5.2；Fable 5.1 | ❌ | 点名。5.2 是现行档 |

### 什么算「prompt 明文授权」

以下**至少满足一条**，否则禁止使用上表「须授权 / 高及以上」的模型：

| ✅ 有效授权 | 示例 |
|:------------|:-----|
| 本 tick `当前模型：` | `当前模型：Opus 5.5`；`当前模型：Fable 5.2`；`当前模型：gpt-6.2-astra`；`当前模型：GPT-5.6 Sol`；`当前模型：Gemini 4 Neon`；`当前模型：kimi-code/k3.1-pro` |
| 本 tick 补充行 / Sticky | `本轨主架构授权：Opus 5.5`；`本轨架构审授权：k3.1-pro`；`本轨执行授权：kimi-for-coding` |

| ❌ 不算授权 | 说明 |
|:------------|:-----|
| Agent 觉得任务太难 | → `HUMAN_DECISION_REQUIRED` |
| 默认 `loop-prompt.txt` | 不算。贵价不得写回这个文件 |
| Arch-First「需要更强」 | 不算。未授权就降级 Grok 4.7 |
| 多方评审「相对强」 | 已授权用该付费档；未授权降级 Grok 4.7 |
| 子 agent 默认「架构任务」 | 无明文仍用当前环境实施档 |
| 历史 tick | 过期 |
| IDE 停在贵档、list 里看得到 | 不算 |
| AGY 新对话默认 Neon | **不算**授权。实施命令必须自己带 `--model` |
| Qoder list 只有顶档 | 不算。未指定则用人类写明的非顶档 |

### 无授权时的降级

| 原本想用 | 无授权时改为 |
|:---------|:-------------|
| Fable / Opus / GPT-6.2 Astra / GPT-5.6 Sol / Gemini 4 Neon 主笔 | **Grok 4.7**（子 agent 优先，CLI 其次） |
| K3.1 Pro / k3 架构审 | **Grok 4.7** 另一实例 |
| mimo、Kimi 执行档 | gemini-3.8-flash、Gemini 4 Hydrogen（已在 AGY Pro+）、deepseek-v4.1-flash、Composer 2.5 |
| Task `model=gpt-*` / `opus` / `fable` / `ultimate` / Gemini 4 推理档 | **不传**。架构轨传列表最新 Grok slug |
| 上述架构模型写代码 | **禁止**。Codex 父会话已经是 `gpt-6.2-sol` 时，那是当前环境，可以写代码 |

### 费用 × 任务矩阵

| 任务 | 默认 | 授权通道 | 严禁 |
|:-----|:-----|:---------|:-----|
| 架构 / ADR 主笔 | 无明文时 **Grok 4.7** | **定格 Opus 5.5**。点名才用 Fable 5.2、GPT-6.2 Astra、GPT-5.6 Sol、Gemini 4 Neon | 有 Opus 授权却改用 Grok 或其他付费档 |
| Arch-First 审查 | 无明文时 **另一实例 Grok 4.7** | 定格 Opus 5.5；其次已授权的 K3.1 Pro / k3 | Composer / Auto / Hydrogen 单独终审 |
| 前端 / 免费档实施 | **gemini-3.8-flash** | Kimi 执行档、mimo（须授权） | 架构模型写代码 |
| AGY Pro+ 日常实施 | **Gemini 4 Hydrogen** 或 **Orchestrator** | 单独点名 Neon 只做推理，不执行 | 不传 `--model` 落到 Neon |
| Cursor 实施 | **Composer 2.5** 或 Auto Cost | — | 默认 Fast；用 Auto Intelligence 摸第三方 |
| 通用后端 | **deepseek-v4.1-flash**、Composer 2.5 | mimo（须授权） | 架构模型写代码 |
| Codex 父会话 | 会话已经绑定的 slug；日常推荐 `gpt-6.2-sol` | Astra 只在点名后做方案 / 挖 bug | 未点名改去 Astra |
| 验收 | 当前 tick 单路收口 | — | 为验收再开贵模型 |

## 方案文档：谁写、谁只提问

### 首次起草

| 优先级 | 模型 | 条件 |
|:-------|:-----|:-----|
| 1 | **Opus 5.5** | 架构定格。点名 Opus，或只授权付费且未点名另一档 |
| 2 | **Fable 5.2** | 仅点名。点名 5.1 时用 5.1 |
| 3 | **GPT-6.2 Astra** 或 **GPT-5.6 Sol** | 仅点名该一个。Qoder 顶档单独点名，不并进这一行 |
| 4 | **Gemini 4 Neon / Carbon / Argon** | 仅点名。不顶替 Opus |
| 5 | **Grok 4.7** | 未授权付费档时的降级。有子 agent 档就 Task |
| 6 | **K3.1 Pro / k3** | 明文授权。架构审，也可辅助起草 |
| 7 | Composer 2.5 | 没有 Grok 时的降级主笔 |
| 8 | Hydrogen、gemini-3.8-flash、deepseek、Luna、Auto | **不主笔**。可以只提问题 |

### 当前模型 = 付费强架构

本 tick 已经点名 Fable、Opus、GPT-6.2 Astra、GPT-5.6 Sol/Terra 或 Gemini 4 推理档时，由该模型改方案。**不写代码**。

### 当前模型 = 中强（Grok 4.7 / K3.1 Pro / k3）

Grok：子 agent 有档就 Task 传最新 Grok slug；没有才 `grok -p`，不传 `-m`。Kimi 架构审须授权，只用 kimi CLI。本轮已有付费主笔时，不抢同一份方案。

### 当前模型 = 实施档

禁止凭自己的判断改架构正文。只提带路径的问题。代码按 [写代码](#写代码默认模型与硬规则) 的环境默认。

## 实施阶段：少纠结模型

写代码时固定当前环境的执行档，不要每 tick 重新挑选。

| 当前环境 | 写代码 |
|:---------|:-------|
| **Cursor** | Composer 2.5 或 Auto Cost。不默认 Fast |
| **Antigravity Free / Plus** | `gemini-3.8-flash`（或 `agy models` 给出的 3.8 id） |
| **Antigravity Pro+** | Hydrogen，或 `"Orchestrator (Neon)"` / Argon / Carbon 中套餐有的那个。命令带 `--model` |
| **OpenCode** | `opencode-go/deepseek-v4.1-flash` |
| **Codex** | 会话已绑定的 slug。日常是 `gpt-6.2-sol`。Astra 不写代码 |
| **Kimi** | 仅当本 tick 授权了 `k3-256k` 或 `kimi-for-coding`。K3.1 Pro / k3 不写代码 |
| **Claude Code** | 会话实际 slug。没有固定模型 |
| **Qoder** | 本机 list 里的非顶档。不用 `ultimate` 写代码。不在仓库里写具体型号 |

**硬规则**：

- 架构名单里的模型不写 prod 代码
- Cursor Task 不传贵价 `model`
- 默认不跨栈。跨栈要明文，或当前环境做不到并记入 status

## Cursor 内：子 agent

| 规则 | 说明 |
|:-----|:-----|
| 实施默认不传 `model` | 与父同模型 |
| 架构未授权 | Task 传列表最新 Grok slug（`grok-4.7-*` 或 `cursor-grok-*`） |
| 无 Grok 档 | `grok -p`，三旗标，不传 `-m` |
| 已点名付费档 | 走人类点名的路径，不用 Grok 顶替，也不在 Cursor Task 里派 |
| 想升档 | `HUMAN_DECISION_REQUIRED` |

## 维护

- 换代时先改 [目录](#cli-现行目录2026-11-19)，再改档位表和 `loop-prompt.txt` 的授权名单
- 与 [models-and-delegation.md](models-and-delegation.md) 冲突时，能力排序以本文为准，委派路径以该文为准
