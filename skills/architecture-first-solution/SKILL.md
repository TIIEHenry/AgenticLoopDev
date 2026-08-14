---
name: architecture-first-solution
description: >-
 Analyze bugs and design tasks by optimizing for architecture and design
 patterns first, seeking the best code design that prevents recurrence of the
 same class of problems; after the written plan/solution, review it with a
 mid-strong or stronger architecture model (not Composer). Use when diagnosing
 root causes, designing fixes, writing plans/ADRs, refactoring for
 maintainability, choosing between local patch vs structural change, or when
 the user asks for architecture-first / design-pattern optimization or
 architecture plan review.
---

# Architecture-First Solution

**跨项目通用。** 分析问题与设计方案时，**禁止先跳进局部打补丁**。优先从架构边界与设计模式寻找最优设计，消除问题类，而非只修当前实例。方案写完后**必须**做 **架构审查（≥中强架构模型）**——**禁止**以 Composer / 弱架构模型作为**唯一**审查者。

若当前仓库装有 Loop 套件，细读：`dev/loop/agent-playbooks/architecture-first-design.md`（及 `dev/loop/models.md` 档位）。**未装套件**时仍按本文步骤执行，审查模型用本会话可用的中强+架构模型。

## When to apply

- 排障 / 根因分析 / bug fix 设计
- 写 plan、ADR、或非 trivial 实施方案
- 在「局部修复」与「结构调整」之间取舍
- 用户提到：架构优化、设计模式、同类问题、防复发、方案审查

## Workflow

```
Architecture-First Progress:
- [ ] 1. Problem class (不只是症状)
- [ ] 2. Architecture & pattern options
- [ ] 3. Choose optimal design (写明取舍)
- [ ] 4. Write the plan/solution
- [ ] 5. Architecture review ≥ mid-strong (mandatory)
- [ ] 6. Incorporate review findings
```

### 1. Problem class — 先定问题类

| 问题 | 产出 |
|:-----|:-----|
| 可见症状是什么？ | 1–2 句 |
| 这是**哪一类**问题？（契约漂移、职责错位、状态机缺口、缺少不变量、错误分层、并发/生命周期、边界泄漏…） | 问题类标签 |
| 为什么同类问题还会再出现？ | 复发机制 |
| 最小补丁会留下什么结构性债？ | 明确风险 |

**通过标准**：能用一句话说明「修完后，同类问题为何更难再发生」。

### 2. Architecture & design-pattern lens

只写相关项：边界 / 不变量 / 抽象层次 / 设计模式（禁止为模式而模式）/ 单一真相源 / 失败与生命周期 / 可测试性。

```
Option A — <name>
 Pros: …
 Cons: …
 Prevents recurrence?: yes/no — how

Option B — <name>
 …
```

### 3. Choose the optimal design

1. **消除问题类** > 只消症状
2. 契合现有架构与 ADR；推翻须先记 ADR
3. 最小充分复杂度
4. 局部性；跨模块契约显式写出
5. 可验证

写清：**选定方案、拒绝方案、拒绝理由**。

### 4. Write the plan/solution

含：Problem class、设计决策、触点、非目标、验证、需更新的 docs/plan/ADR。
仍遵守仓库「先方案再编码」；trivial 可缩短，但步骤 1–3 思考不可跳过。

### 5. Architecture review（≥中强）— mandatory

方案正文写完、**开始大规模编码之前**，由**独立**审查者（作者 ≠ 审查者实例）做架构审查。

**模型档**（有 `dev/loop/models.md` 则以其为准；否则用下表实践默认）：

| 优先级 | 审查模型 | 条件 |
|:-------|:---------|:-----|
| 1 | 贵价强架构模型（GPT 5.5/5.6、Opus、Qoder Ultimate） | 用户/prompt **明文授权** — **仅此有效** |
| 2 | **中强架构默认**（**`grok -p`** 优先；降级 Grok/kimi-k3） | **无贵价授权时的默认**；无须贵模型授权 |
| — | 写作向 / 弱架构模型（如 Composer、多数 flash/小模型） | **禁止**作为唯一架构审查者 |

**硬规则**：做架构审查 **≠** 获得贵价授权。「要更强审查者」只说明须 ≥中强（默认 **`grok -p`** 或 Grok/kimi-k3），**禁止**因此自行 spawn GPT / Opus / Ultimate（含 Task `model=`、跨栈 CLI）。未明文却要用贵价 → `HUMAN_DECISION_REQUIRED`。

Grok CLI：**Cursor 内也用 Shell** `grok -p --no-plan --permission-mode bypassPermissions --always-approve` 做独立审查（≠ 作者会话）。
Cursor `Task`：**仅** CLI 不可用时传**中强** `model`（如 Grok）——**不含**贵价 slug。
**Prompt 必须含**：方案路径或正文、问题类与选定设计各一句、下列清单：

```
审查目标：从架构与设计模式评估该方案，不是润色文案。

请回答：
1. 方案是否只在修症状，而未消除问题类？若是，给出更优结构。
2. 边界/职责/依赖方向是否有更干净的切分？
3. 是否有更合适的设计模式或更简单的不变量强制方式？
4. 复发风险：6 个月后同类 bug 是否仍容易出现？如何堵住？
5. 过度设计或范围膨胀了吗？指出可删减处。
6. 与仓库既有架构/ADR 的冲突或遗漏文档点。
7. 结论：Approve / Approve with changes / Reject — 并给出必须修改的具体条目。
```

若 Task 不可用：在同一会话做**等价中强架构审查**，标注「架构审查（会话等价）」。
**Anti-Spin**：同一方案最多 **2** 轮审查；仍 Reject → `HUMAN_DECISION_REQUIRED`。

### 6. Incorporate findings

- Reject / must-fix → 改方案后再审（计入轮次）
- Approve with changes → 合并后再编码
- Approve → 实施时保持选定架构，禁止退化成局部补丁

```
问题类: …
选定设计: …
架构审查(≥中强): Approve | Approve with changes | Reject
关键调整: …（如有）
```

## Anti-patterns

- 只加 `if` / 重试，不追问职责是否放错层
- 复制粘贴修多处，却不抽策略或单一入口
- 无关新抽象、「未来也许用得上」的层
- 方案未写完或未经架构审查就开始大改
- 用 Composer 单审冒充架构闸
- **以「架构审查需要更强」为由，未获明文却拉 GPT / Opus / Ultimate**

## Trivial exception

单行笔误、明确无结构含义的文案/日志 → 可跳过完整选项对比与架构审查；须**显式标注**。有「会否复发」疑虑 → **不**按 trivial。
