---
name: multi-party-design-review
description: >-
  Multi-party solution design: ask platforms, delegate the same task to multiple
  agents for full candidate plans in OS temp, synthesize with a strong-architecture
  model into the project, run fast-model multi-perspective reviews, then another
  strong-architecture review/update, weak-architecture implementer questions,
  then strong-architecture refines the plan; the implementer Q&A loop may run
  multiple rounds and backtrack to synthesis / fast multi-perspective / strong
  review when questions are deep. Use when the user asks for 多方评审, 方案设计,
  同一任务多路并行起草, or design review before implementation.
---

# 多方反复评审 · 方案设计

**跨项目通用。** 固定流水线：**问可用平台 → 同一任务多路并行写 tmp 候选 → 相对强综合进仓库 → 快速模型多视角评审 → 另一相对强审查并更新 →〔相对弱执行方提问 ⇄ 相对强细化；可回跳〕→ 收口**。默认 **不写 prod、不自主 commit**。  
「相对强」≠ 必须 GPT；贵价模型另需明文授权。

有 Loop 时遵守 [`models.md`](../../models.md) 费用门禁与能力档；起草原则可参考 [`architecture-first-solution`](../architecture-first-solution/SKILL.md)。多视角输出格式可参考 [`review-question-resolve-loop.md`](../../agent-playbooks/review-question-resolve-loop.md)。

## When to apply

- 用户要 **方案设计**、**同一任务多路并行** 再综合，并要 **多视角** 打磨  
- 首次或重大修订 plan / ADR，定稿前加固

**不要**用：纯实施改码、trivial 文案。

**两处「并行」勿混淆**：

| 步骤 | 是什么 |
|:-----|:-------|
| **2** | **同一任务** 派多个 worker，各写一份 **完整候选方案** → tmp |
| **4** | 综合稿后，快速模型多视角并行只评不改；**视角数 3～5**（核心三必选） |
| **6⇄7** | **相对弱执行方审查提问** 可 **多轮**；相对强细化后可再问；可 **回到 3/4/5** |

## 硬门禁

### 「强架构」= 相对强，不是「必须 GPT」

本技能里的 **强架构 / 综合主笔 / 审查者 / 细化** 指：在本轮 **已选平台与已授权模型** 里，选 **架构能力相对更强** 的档位来写/审方案——**默认可以是 Grok、kimi-k3 等中强**，不必上 GPT。

| 概念 | 含义 |
|:-----|:-----|
| **相对强架构** | 本轮可用里架构档更高者；**综合/审查还须偏快**（常见默认：**Grok**；有授权且用户要时才用更慢的 GPT/ultimate） |
| **相对弱 / 快速** | Auto、Composer、mimo、flash、Qoder efficient… — 适合步骤 2 并行、步骤 4 多视角、步骤 6 提问 |
| **贵价模型** | GPT 5.5 / GPT 5.6 / Qoder `ultimate` / Opus — **另计费用门禁**，与「要不要相对强主笔」不是同一回事 |

对照 [`models.md`](../../models.md) 能力档：综合与审查 **至少中强**；**禁止**只用 Auto/Composer/弱档做综合终稿或唯一架构审查。  
**贵价模型**：仅当用户在 0b 选 **B（授权贵价）** 或明文点名才可派；未授权 → 用 Grok/k3 等相对强即可。

其它硬规则：

- **Cursor 本机可派**：Auto / Grok / Composer。其中 **Grok = Cursor 上的相对强架构**（可综合/审查/细化）；Auto/Composer = 相对弱/快速。Cursor **派不出** GPT——若要用贵价，走 Qoder `ultimate` / Codex 等，且须 B 授权
- 综合主笔与审查者须为 **两个不同实例**（作者 ≠ 审查者）；审查者须为相对强（≥中强），**禁止** Composer/Auto/弱档单独终审
- 相对弱 **只提问**；细化由相对强主笔改项目文档（步骤 7）
- 并行草案 **只写系统临时目录**

### 平台 → 能派什么

| 平台 | 可派模型 | 相对强架构？ | 贵价（须 B）？ |
|:-----|:---------|:-------------|:---------------|
| **Cursor** | Auto / Grok / Composer | **Grok** | 无（不派 GPT） |
| **Qoder** | performance / efficient / … | performance 等可作并行；架构向可用中强档 | **`ultimate`**（= GPT 5.6） |
| **Codex** | 本地配置 | 视模型 | **gpt-5.6-*** 等 |
| **Claude Code** | mimo 等 | 视 slug | 仅明文 **Opus** |
| **OpenCode / Kimi** | k3 等 | **kimi-k3** 可作相对强 | 按明文 |

### 角色默认落点（无 B 时）

| 角色 | 落点 |
|:-----|:-----|
| **综合主笔 / 审查 / 细化** | **相对强且偏快**：架构能力够用的前提下 **优先更快**（见下） |
| **并行草案（2）** | 相对弱/中：Auto、Composer、Qoder performance… |
| **多视角（4）** | **快速**：Auto 优先等；**不要**为多视角烧贵价 |
| **执行方提问（6）** | 相对弱：Auto / Composer / mimo… |

### 综合（3）与审查（5）：相对强 + 不能太慢

步骤 3 / 5（及回跳再综合/再审）是流水线卡点，须 **架构能力不错，且速度不能太慢**。

| 优先级 | 选型 | 说明 |
|:-------|:-----|:-----|
| 1 | **Cursor Grok** | 本仓库默认：中强架构 + **快于** kimi-k3；综合与审查优先 |
| 2 | 其它平台上 **偏快的中强**（若有） | 同档里选更快的；审查须 ≠ 综合实例 |
| 3 | kimi-k3 等 | 架构 ≈ Grok 但 **更慢** — 仅当 Grok 不可用或用户点名 |
| 4 | 贵价 GPT / ultimate / Opus | **通常更慢更贵** — 仅 0b 选 B 且用户接受耗时时用；默认 **不要**拿来做 3/5 |

约束：

- 综合与审查仍须 **两个不同实例**；可用「Grok 综合 + 另一 Grok 会话审查」或「Grok + 另一平台偏快中强」  
- **禁止**用 Auto/Composer 做 3/5 终稿或唯一审查（架构偏弱）  
- **禁止**为「更强一点」默认升到慢速贵价，除非用户选 B 且明确要  
- 细化（7）同样优先 **相对强且偏快**（与综合同档，如 Grok），避免每轮细化卡很久  

## Workflow

```
Multi-Party Design Review:
- [ ] 0a. AskQuestion 多选可用平台
- [ ] 0b. AskQuestion 选角色预设（仅基于已选平台）
- [ ] 1. Scope（产物路径 / 目标 / 非目标）
- [ ] 2. 同一任务多路并行 → 各写一份 tmp 候选方案
- [ ] 3. 相对强 A：综合方案 → 写入项目
- [ ] 4. 快速模型：多视角并行评审（只评不改）
- [ ] 5. 相对强 B：审查（含多视角问题）→ 更新项目方案
- [ ] 6⇄7. 执行方审查环（可多轮；可回跳）
      - [ ] 6. 相对弱：执行方审查提问（只问不改）
      - [ ] 7. 相对强 A：按提问细化项目方案
      - [ ] 6b. 若仍有 Blocking / 新问题 → 再 6，或按路由回跳 3/4/5
- [ ] 8. 收口；仍有需人类裁决的 → HUMAN_DECISION_REQUIRED
```

### 0. 询问可用平台 → 再锁定角色

**在派任何子 agent / CLI 之前**先做完本步。  
**禁止**把大段「请按条列出…」粘进聊天。

#### 交互方式（优先级）

1. **有 `AskQuestion`（或等价选择题 UI）→ 必须用它**  
2. **每条助手消息最多 1 个** `AskQuestion`  
3. **无交互工具** → 用下方极短 Fallback，勿扩写

#### 第 0a 题（必须先做）：哪些平台能用？

`AskQuestion` **多选**：

```text
标题: 本轮方案设计可用哪些平台？
选项（多选）:
- Cursor
- Qoder
- Claude Code
- Codex
- OpenCode
- Kimi
```

未勾选的平台 → 本轮 **禁止**对该栈派 Task/CLI。

#### 第 0b 题：在已选平台上怎么分配？（下一轮消息）

根据 0a 结果出题（仍用 `AskQuestion` **单选**），只含 **用户已选平台** 能支撑的预设：

```text
标题: 在已选平台上用哪套角色预设？
选项示例（按可用平台裁剪）:
A) 默认 — 综合/审查/细化=相对强且偏快(优先 Grok)；并行+多视角+提问=Auto/Composer。无贵价
B) 授权贵价 — 允许 ultimate/Codex gpt，但 3/5 **默认仍优先 Grok 等偏快相对强**；仅用户明确「综合/审查用贵价」时才换慢速贵价
C) 由你按「相对强偏快 vs 快速弱」自动分配
D) 微调
```

- 选 **A/C**：3/5/7 用 **Grok（或同档偏快中强）**，**不要**自行升 ultimate/gpt，也 **不要**用偏慢的 k3 抢默认  
- 选 **B**：贵价可用，但未点名「3/5 用贵价」时仍用偏快相对强  
- 选 **B** 且 0a 无 Qoder/Codex：贵价用不上 → 用 Grok 等继续  

#### Fallback（无 AskQuestion）

分两句等两次回复，禁止合成长问卷：

```text
1) 可用平台？回编号可多选：1 Cursor 2 Qoder 3 Claude 4 Codex 5 OpenCode 6 Kimi
2)（答完再问）回 A 默认相对强 / B 授权贵价 / C 自动分配
```

#### 锁定表（向用户只复述一行摘要）

| 角色 | 平台 + 模型 | 相对档 |
|:-----|:------------|:-------|
| 并行草案 ×N | … | 相对弱/中；同一任务各写一份 |
| **综合主笔** | … | **相对强且偏快**（默认 Grok） |
| **审查者** | … | **相对强且偏快**，≠ 主笔实例 |
| **执行方提问** | … | **相对弱**（只问） |
| **细化文档** | … | **相对强且偏快**（与综合同档） |

摘要例：`综合 Grok(快) → 多视角 Auto → 审查 另一 Grok 会话 → 提问 Auto ⇄ 细化 Grok`。

### 1. Scope

确认（或缺省并写出假设）：

| 项 | 说明 |
|:---|:-----|
| **项目产物路径** | 如 `dev/plans/….md` |
| **目标一句话** | 要解决什么 |
| **非目标** | 本轮不做 |
| **tmp 根目录** | 见下 |

### 2. 同一任务 · 多路并行写 tmp 候选方案

**含义**：把 **同一份** Scope + 任务说明，**同时委派给 ≥2 个** 不同平台/模型的 agent；每个 agent **独立**交一份 **完整候选方案**（不是拆维度、不是各写一节）。

**不是**：多视角分工（多视角在 **步骤 4**，用快速模型）。

1. 创建系统临时目录（Linux/macOS）：

```bash
TMP_DESIGN="$(mktemp -d "${TMPDIR:-/tmp}/mpdr-XXXXXX")"
echo "$TMP_DESIGN"
```

2. 准备 **同一** 任务 prompt（所有并行 worker 原文一致），至少含：目标、非目标、约束、须覆盖的章节（问题类 / 选项 / 选定设计 / 风险 / 验证）。

3. **并行委派**（Task / Subagent / 跨栈 CLI，按锁定表）：每个 worker 只把自己的完整方案写到 tmp：

```text
$TMP_DESIGN/draft-<platform>-<model>.md
```

例：`draft-cursor-grok.md`、`draft-qoder-performance.md`、`draft-cursor-auto.md`。

4. 父 agent 汇总文件列表；**此时仍不写仓库**。各草案之间允许结论冲突——留给步骤 3 综合消解。

### 3. 相对强 A — 综合进项目

用锁定的 **综合主笔**（相对强且偏快：默认 **Grok**；慢速 k3/贵价仅点名或 Grok 不可用时）：

- 输入：全部 `$TMP_DESIGN/draft-*.md` + Scope
- 产出：**综合方案** 写入 **项目产物路径**（覆盖或新建均须在输出里说明）
- 综合要求：消解冲突、写明取舍、保留必要备选一句、可实施的下一步
- **frontmatter 必填**（见下）；缺项则步骤 3 未完成

#### 项目方案 frontmatter（多方架构评审标注）

须含仓库文档门禁字段（`title` / `type` / `status` / `phase` / `updated` / `summary`），并 **额外** 标明来自本技能与模型来源：

```yaml
---
title: "<方案标题>"
type: architecture   # 或 plan，按产物类型
status: draft
phase: <phase 或 N/A>
updated: YYYY-MM-DD
summary: "多方架构评审综合稿：…"
origin: multi-party-design-review
mpdr:
  skill: multi-party-design-review
  # 步骤 3 写入时必填：
  synthesized_by: "<平台> / <模型>"          # 例：Cursor / Grok
  draft_sources:                            # 本轮吸收的并行候选
    - platform: Cursor
      model: Auto
      file: draft-cursor-auto.md
    - platform: Qoder
      model: performance
      file: draft-qoder-performance.md
  # 后续步骤追加（写入时先留空列表/空串，禁止省略键）：
  perspective_reviewers: []                 # 步骤 4：[{dimension, platform, model}, …]
  architecture_reviewed_by: ""            # 步骤 5：例 Codex / gpt-5.6-terra 或 Cursor / Grok（另一会话）
  architecture_review_verdict: ""         # Approve | Approve with changes | Reject
  refined_by: ""                          # 步骤 7 最近一轮细化模型
  implementer_ask_rounds: 0               # 执行方环轮次
---
```

规则：

- `origin: multi-party-design-review` **不可省** — 标明本文是多方架构评审产物，不是单人随手草稿  
- `mpdr.synthesized_by` + `mpdr.draft_sources` 在步骤 3 **必须已填实**  
- 步骤 4 / 5 / 7 更新方案时 **同步改** `perspective_reviewers` / `architecture_reviewed_by` / `verdict` / `refined_by` / `implementer_ask_rounds`  
- `summary` 宜含「多方架构评审」字样，便于检索  

```text
综合完成：
- 项目方案: <path>
- frontmatter.origin / mpdr.synthesized_by / draft_sources: OK
- 吸收的 tmp 草案: …
- 拒绝的冲突点及理由: …
```

### 4. 快速模型 — 多视角并行评审

**时机**：综合方案 **已写入项目之后**。  
**模型**：仅 **快速/省钱档**（Cursor **Auto** 优先，或 Composer / Qoder `efficient`·`performance` / mimo / flash）。**禁止** GPT / ultimate / Opus 跑本步。

#### 视角数量（硬上下限）

| | 数量 | 说明 |
|:--|:-----|:-----|
| **下限** | **3** | 少于此数不算完成步骤 4；默认必含下表「核心三」 |
| **上限** | **5** | 含核心三在内最多 5 维；**禁止**为凑热闹开满目录或超过 5 |
| **回跳再跑 4** | 仍遵守 3～5；只补缺维或重跑相关维，总数仍 ≤5 |

选维规则：先固定 **核心三**，再按题从「可选维」里加 **0～2** 个（合计 ≤5）。Scope 可写明加减；未写则用核心三（=3）。

**核心三（必选）**：

| 维度 | 焦点 |
|:-----|:-----|
| Architecture | 边界、契约、不变量、复发（快速扫，终审仍交步骤 5） |
| Product / Interaction | 用户路径、空/错态 |
| Testing / Verification | 如何证伪、门禁缺口 |

**可选维（最多再加 2）**：

| 维度 | 何时加 |
|:-----|:-------|
| Documentation / Traceability | 方案要挂 roadmap/ADR/status 时 |
| Security / Safety | 权限、密钥、副作用相关 |
| Performance | 热路径、缓存、长任务相关 |

按维 **并行** 委派（每维一个 worker，**只评不改**）。输出写到 tmp，例如 `$TMP_DESIGN/perspective-architecture.md`，须含：

```text
Dimension:
Verdict: PASS / PARTIAL / FAIL
Blocking Findings:
Non-Blocking Findings:
Questions:
Evidence:
Required Fixes:
```

父 agent **汇总去重**（Blocking / Clarification / Noise）写入 `$TMP_DESIGN/perspective-summary.md`，**先不改**方案正文架构结论；但须 **更新项目方案 frontmatter**：

```yaml
mpdr.perspective_reviewers:
  - dimension: Architecture
    platform: Cursor
    model: Auto
  - dimension: Product / Interaction
    platform: Cursor
    model: Auto
  # …共 3～5 项
```

### 5. 相对强 B — 审查并更新

用锁定的 **审查者**（另一相对强且偏快实例，≠ A；默认另一 Grok 会话，勿默认改用更慢的 k3/贵价）：

- 输入：项目综合方案 + `$TMP_DESIGN/perspective-summary.md`（及必要分维文件）
- 审查清单（须逐条回答）：

1. 是否只在修症状、未消问题类？更优结构？  
2. 边界/职责/依赖是否可更干净？  
3. 模式是否过重或过简？  
4. 六个月后同类问题是否易复发？  
5. 与仓库既有 ADR/架构是否冲突？  
6. 多视角 Blocking 哪些必须吸收、哪些可 Deferred？  
7. 结论：`Approve` / `Approve with changes` / `Reject`

- **Approve** → 进入步骤 6；并更新 frontmatter：`mpdr.architecture_reviewed_by`、`mpdr.architecture_review_verdict`  
- **Approve with changes / Reject** → 由主笔 A（或审查者按用户指定）**更新项目方案**（含 frontmatter 同上）；审查循环 **最多 2 轮**，仍 Reject → `HUMAN_DECISION_REQUIRED`  
- 审查笔记可写 `$TMP_DESIGN/review-roundN.md`；**终稿只以项目路径为准**

### 6⇄7. 执行方审查环（可多轮，可回跳）

相对弱以 **实施审查者** 身份反复提问；相对强细化文档。问题可以很多，**不要**指望一轮问完。

```text
        ┌──────────────────────────────────────────────┐
        ▼                                              │
   [6 相对弱提问] → [7 相对强细化文档] ──仍有疑问？──┬─是─→ 再 6
        │                      │                     │
        │                      │ 问题动摇设计？        └─否─→ 8 收口
        │                      ├─ 需重综合 / 重选方案 → 回 3（必要时重做 2）
        │                      ├─ 多视角未覆盖的产品/测试洞 → 回 4 再 5
        │                      └─ 仅架构终审级争议 → 回 5
        └─ 每轮写入 tmp，带轮次号
```

#### 回跳路由（按问题性质）

| 问题信号 | 回到 |
|:---------|:-----|
| 接口/状态机/落点不清、缺验收步骤 | **7** 细化即可（本环默认） |
| 多视角没扫到的交互/测试/安全洞 | **4**（快速多视角）→ **5** → 再进 6 |
| 强审结论被新事实推翻、边界要改 | **5**（相对强再审）→ 再 6 |
| 候选方案级冲突、选定设计摇晃 | **3** 重新综合（必要时 **2** 再开一路候选）→ 4→5→6 |
| 需人类拍板 | 写入方案 `HUMAN_DECISION_REQUIRED`，可继续问其它非阻塞项 |

#### Anti-Spin（执行方环）

每轮 6→7 **至少一项**：Blocking 减少、方案新增可实施细节、新证据、或标出待人类裁决。  
默认最多 **5** 轮 6⇄7；回跳 3/4/5 合计最多 **2** 次。超限仍 Blocking → `HUMAN_DECISION_REQUIRED`，停止空转。

#### 步骤 6 — 相对弱执行方审查提问

- **只读** 当前项目方案（及必要代码/契约）  
- **禁止**改项目文档  
- 每轮写入 `$TMP_DESIGN/implementer-questions-round<N>.md`（N 从 1 递增），并更新合并版 `$TMP_DESIGN/implementer-questions.md`  
- 分类：Blocking / Clarification / Deferred（含义同前）  
- 问题宜多、宜具体；可声明「本轮先问第 1～k 个 Blocking，其余下轮」  
- 若认为须回跳：在输出里写 `SuggestBacktrack: 3|4|5` 与理由  

```text
执行方审查提问 round N:
SuggestBacktrack: none | 3 | 4 | 5
Blocking: …
Clarification: …
Deferred: …
```

每轮结束后 **必须** 进 7 或按 `SuggestBacktrack` 回跳（父 agent 裁决路由），不得只丢问题给用户。

#### 步骤 7 — 相对强细化文档（每轮提问后必做）

用 **综合主笔同档、偏快相对强**（默认 Grok）**改写项目方案**：

| 输入 | 动作 |
|:-----|:-----|
| 本轮 `implementer-questions-round<N>.md` | 关闭能关的 Blocking；Clarification 落假设或补设计 |
| 回跳后的新多视角/强审结论（若有） | 一并吸收进正文 |
| Deferred | 方案「延期」节或 Deferred Gaps；勿假装已解决 |

细化后写 `$TMP_DESIGN/refine-notes-round<N>.md`，并更新 frontmatter：`mpdr.refined_by`、`mpdr.implementer_ask_rounds: N`，然后：

- 仍可能有实施疑问 → **再跑步骤 6**（新一轮）  
- 执行方建议回跳且父 agent 同意 → 执行回跳，完成后再进 6  
- Blocking=0 且执行方本轮明确 `ReadyToImplement: yes` → 步骤 8  

```text
细化 round N 完成:
- 已关闭 Blocking: …
- 已落假设: …
- 下一动作: 再6 | 回3 | 回4 | 回5 | 收口8 | HUMAN_DECISION_REQUIRED
```

### 8. 收口

- 仅当执行方环收敛（无 Blocking，或仅剩 Deferred/人类裁决）  
- Final Output 含 **轮次 N** 与回跳次数  
- **不要**在本技能内开始大范围写 prod 代码  

## 委派提示

| 步骤 | 做法 |
|:-----|:-----|
| 2 多路并行 | **同一 prompt** 派 ≥2 worker 写完整候选 |
| 3 综合 | **相对强且偏快**（默认 Grok）；勿默认 k3/贵价拖慢 |
| 4 多视角 | **快速**；Auto 优先 |
| 5 审查 | **另一偏快相对强**（默认另一 Grok 会话） |
| 6⇄7 | 提问用相对弱；细化用偏快相对强；可回跳 |

默认示例：`综合 Grok → 多视角 Auto → 审查 另一 Grok →〔提问 Auto ⇄ 细化 Grok〕×N → 收口`。

## Final Output

```text
可用模型锁定: …
TMP_DESIGN: …
项目方案: <path>
执行方环: rounds=N / backtracks=…
末轮提问: Blocking n / Clarification n / Deferred n
细化: 已关闭… / ReadyToImplement: yes|no
下一步: 人类裁决（若有）/ 转入实施（另开会话）
```

## Anti-patterns

- **把第 0 步长文问卷贴进聊天**（必须用 `AskQuestion` 或短 Fallback）  
- **跳过 0a、直接问角色/预设**（必须先问可用平台）  
- 步骤 3 写出的项目方案 **缺** `origin: multi-party-design-review` 或 `mpdr.synthesized_by` / `draft_sources`  
- 步骤 4/5/7 改了正文却 **不更新** 对应 `mpdr.*` 模型来源字段  
- 3/5/7 默认用偏慢的 k3 或贵价，拖慢流水线（除非用户点名或 Grok 不可用）  
- 把「强架构」理解成 **必须 GPT**  
- 未选 B 却自行派 ultimate/gpt  
- 在 Cursor 上派 GPT/Sonnet（本机无此档）  
- 用 Auto/Composer 做综合终稿或唯一架构审查  
- 步骤 4 视角 **<3 或 >5**  
- 用贵价跑步骤 4 多视角，或跳过步骤 4 直接审  
- 把步骤 2 做成多维度分工（多视角只属于步骤 4）  
- 多视角 reviewer 直接改项目方案（须经步骤 5）  
- **执行方只问一轮就收口**，或问题很多却不准回跳 3/4/5  
- **提问后不跑步骤 7**，或只在聊天答疑不改项目文档  
- 执行方环空转（Blocking 不减、文档不增细节）  
- 让相对弱自己改方案正文  
- 未锁定就开始派未选平台  
- 并行草案直接写进 `dev/plans/`  
- 综合与审查用同一模型实例「自审」  
- 把 tmp 当仓库 SSOT 长期引用  

## Trivial exception

无结构含义的措辞修正 → 可跳过本流水线；须标注。
