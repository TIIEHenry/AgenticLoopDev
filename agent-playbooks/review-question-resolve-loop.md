---
title: "Review Question Resolve Loop"
type: guide
status: active
phase: N/A
created: 2026-06-17
updated: 2026-06-17
summary: "反复评审、问题提取、调查展开、更新收敛的子 agent 链路。"
---

# Review Question Resolve Loop

本 playbook 用于方案、计划、实现或文档的反复评审。目标是让不明白的地方被专门子 agent 展开调查，并通过证据收敛，而不是让父 agent 在主上下文里猜测。

## Loop Goal 模板

```text
Goal:
Run one Review-Question-Resolve cycle for <artifact/change>. Identify unresolved questions, investigate blocking ones with subagents, update the artifact if needed, and stop only when there are no blocking questions or a human decision is required.

Success Criteria:
- All reviewer questions are classified.
- Blocking questions have investigation results.
- Resolved questions update docs/code/roadmap as needed.
- Deferred questions are recorded with priority, reason, and exit condition.
- Overall Verification decides PASS / PARTIAL / FAIL.
```

## Review Chain

1. Dimension Review Agents 并行评审。
2. Question Extraction Agent 汇总、去重、分级问题。
3. Investigation Agents 针对 blocking / high-value clarification 展开事实调查。
4. Update Agent 根据调查结论更新 plan、roadmap、ADR、代码或文档。
5. Overall Verification Agent 判断是否收敛，或进入下一轮。

## Dimension Review Agents

按任务需要选择维度，不必每轮全量启用：

| Dimension | Focus |
|:----------|:------|
| Architecture | 模块边界、ADR、KMP 约束、状态流、跨模块契约 |
| Product / Interaction | 用户路径、空状态、错误状态、重试/取消、键盘/指针、Android/Desktop 差异 |
| UI / Visual | DESIGN-SPEC、组件目录、Surface、颜色、间距、golden 风险 |
| Performance / Resource | Flow / Compose 重组、缓存、长任务、Gradle daemon、adb 互斥 |
| Testing / Verification | 单测、desktopTest、golden、adb、真实 LLM E2E、手测矩阵 |
| Documentation / Traceability | plan、roadmap、status、ADR、Deferred Gaps、Research Queue 是否同步 |
| Security / Safety | 权限、路径、provider config、secret、tool side effect、sandbox |

## Dimension Review Prompt 模板

```text
Role:
You are the <Dimension> Review Agent for the current project.

Goal:
Review <artifact/change> only from the <Dimension> perspective and produce findings that can drive the review loop.

Inputs:
First read:
- `dev/loop/agent-playbooks/subagent-loop-startup.md`
- `dev/loop/agent-playbooks/review-question-resolve-loop.md`

Then read the artifact, code paths, tests, or docs passed by the parent prompt.

Constraints:
- Do not implement fixes.
- Do not claim whole-task completion.
- Do not re-review unrelated dimensions unless they directly affect your dimension.
- Human-facing output must be written in Chinese.

Output:
Dimension:
Verdict: PASS / PARTIAL / FAIL
Blocking Findings:
Non-Blocking Findings:
Questions:
Deferred Gaps:
Evidence:
Required Fixes:
Recommended Tests:
```

## Question Extraction

Question Extraction Agent 必须把所有 reviewer 的问题分类：

| Class | Meaning | Action |
|:------|:--------|:-------|
| Blocking Question | 不解决不能实现或不能宣布完成 | 派 Investigation Agent 或要求用户裁决 |
| Clarification Question | 影响质量，但可带假设推进 | 写明假设和验证方式 |
| Deferred Question | P2/P3 或受环境限制，不阻塞当前目标 | 写入 Deferred Gaps / Research Queue |
| Noise | 重复、无证据、过宽、不可行动 | 丢弃并写一句原因 |

输出格式：

```text
Blocking Questions:
- B1: <问题> — <为什么阻塞> — <建议调查 agent>

Clarification Questions:
- C1: <问题> — <可采用假设> — <验证方式>

Deferred Questions:
- D1: <问题> — <Priority> — <Why Deferred> — <Exit Condition>

Noise Dropped:
- <问题> — <丢弃原因>
```

## Investigation Agent

每个 Investigation Agent 只调查一个问题，避免上下文扩散。

```text
Role:
You are an Investigation Agent for the current project.

Goal:
Resolve question <B1/C1> with code, doc, test, or runtime evidence.

Inputs:
First read:
- `dev/loop/agent-playbooks/subagent-loop-startup.md`
- `dev/loop/agent-playbooks/review-question-resolve-loop.md`

Then read only the files needed to answer this question.

Constraints:
- Do not implement fixes unless explicitly requested.
- Do not broaden scope.
- Human-facing output must be written in Chinese.

Output:
Question:
Finding:
Evidence:
Decision / Recommendation:
Impact:
Required Update:
Residual Risk:
```

## Convergence Rules

继续下一轮评审的条件：

- 仍有 Blocking Question。
- 调查结果改变了方案、计划、实现或验收标准。
- Overall Verification 给出 FAIL。

停止循环的条件：

- 没有 Blocking Question。
- Clarification Question 都已有明确假设和验证方式。
- Deferred Question 都进入 Deferred Gaps 或 Research Queue，且包含 priority、reason、exit condition。
- Overall Verification 给出 PASS，或给出可接受的 PARTIAL。

## Anti-Spin Rule

每轮 review loop 必须满足至少一项：

- Blocking Question 数量减少。
- 新增了能改变判断的事实证据。
- 更新了 plan、roadmap、ADR、代码、测试或文档。
- 明确识别出需要用户裁决的问题。

如果一轮没有减少问题也没有新增证据，停止循环并请求人类裁决。
