---
title: "Grok CLI（grok）"
type: guide
status: accepted
phase: N/A
updated: 2026-08-08
summary: "Grok Build CLI：架构优先；Loop 须 --no-plan + bypassPermissions + always-approve；同栈禁止再起 grok -p。"
---

# Grok CLI：`grok`

**Loop 优先级**：架构 / ADR / 方案主笔 / 挖 bug / Arch-First 审查 — **本仓库默认优先 `grok` CLI**（`-m grok-4.5`），**高于 Cursor 内 `Task` Grok 模型档**。能力档见 [../models.md](../models.md)。

### Cursor 内 Loop

父 agent 在 **Cursor** 跑 `/loop` 时，架构轨仍用 **Shell 工具**调用本页命令，**不要**：

- 起 `Task` 并选 Grok 模型做架构主笔/审查  
- 为架构把 Cursor 聊天模型切成 Grok（实施轨保持 Composer/Auto）

## 前置

```bash
which grok
grok --version
grok doctor          # 终端/剪贴板/输入支持
grok models          # 列出可用模型（默认 grok-4.5）
# 未登录时：
grok login
```

## Loop 委派：完全权限 + 禁 plan（**必选**）

Loop / 父 agent 用 Shell 调 `grok -p` 时，**必须**带下列旗标，避免 headless 卡在工具审批或默认进入 `grok-build-plan`：

```bash
# 本仓库 Loop 标准授权（仅受信仓库根目录）
GROK_LOOP_AUTH='--no-plan --permission-mode bypassPermissions --always-approve'
```

| 参数 | 说明 |
|:-----|:-----|
| `--no-plan` | **禁止**默认进 `grok-build-plan`；缺则易卡在 plan / `waiting_for_model`、迟迟无生产 diff |
| `--permission-mode bypassPermissions` | 跳过工具权限确认（与 `claude --permission-mode bypassPermissions` 同档） |
| `--always-approve` | 自动批准工具执行（与上项并用，Loop **默认三开**） |

**禁止** Loop 委派时省略上述 flags 指望人工点批准。只读审计仍用完全权限跑工具，靠 **prompt** 约束不改码（见下）。

> **对比 Claude Code**：`claude` **无** `--no-plan`；勿用 `--permission-mode plan`（那是进入只读 Plan）。Claude 非交互改码用 `claude --permission-mode bypassPermissions -p` 即可 → [claude.md](claude.md)。

## 推荐：非交互 `grok -p`

Loop / 父 agent 委派架构 doc、方案、只读审计时，**默认用单轮 headless + 完全权限 + `--no-plan`**：

```bash
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
GROK_LOOP_AUTH='--no-plan --permission-mode bypassPermissions --always-approve'

grok $GROK_LOOP_AUTH -m grok-4.5 -p "$prompt"
# 或从文件：
grok $GROK_LOOP_AUTH -m grok-4.5 --prompt-file /path/to/prompt.txt
```

**反例**：

```bash
# ❌ 缺 --no-plan → 易绑 grok-build-plan
grok --permission-mode bypassPermissions --always-approve -p "$prompt"
# ❌ 仅 acceptEdits → headless 可能停在 permission_prompt
grok --no-plan --permission-mode acceptEdits --always-approve -p "$prompt"
```

| 参数 | 说明 |
|:-----|:-----|
| `-p`, `--single <PROMPT>` | 单轮 prompt，打印回复后退出（**Loop 委派首选**） |
| `-m`, `--model <MODEL>` | 模型 ID；本仓库默认 **`grok-4.5`** |
| `--prompt-file <PATH>` | 从文件读 prompt |
| `--output-format plain\|json\|streaming-json\|streaming-messages-json` | headless 输出格式 |
| `--reasoning-effort <EFFORT>` | 推理模型力度（`--effort` 别名） |
| `--max-turns <N>` | 限制 agent 轮次 |
| `--disallowed-tools <TOOLS>` | 禁用内置工具（逗号分隔） |
| `--disable-web-search` | 禁用 web 搜索/抓取 |

### 只读审计（禁改码）

与 [antigravity.md §只读审计](antigravity.md#只读审计强制强调) 同构，prompt **必须**写死：

```bash
GROK_LOOP_AUTH='--no-plan --permission-mode bypassPermissions --always-approve'
grok $GROK_LOOP_AUTH -m grok-4.5 -p "$(cat <<'EOF'
只读审计。禁止写文件、禁止跑会改仓库的命令。
禁止 git checkout -- / restore / stash / clean / reset（AGENTS.md）。
任务：<审计范围>
交付：问题清单 + 文件路径引用；不改 prod。
EOF
)"
```

## 交互会话

人工深度结对或需要多轮工具时：

```bash
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
# 交互也须完全权限（受信目录）：
grok --no-plan --permission-mode bypassPermissions --always-approve -m grok-4.5 "你的任务"
```

| 参数 / 命令 | 说明 |
|:------------|:-----|
| `-c`, `--continue` | 续本目录最近会话 |
| `-r`, `--resume [<ID\|TITLE>]` | 按 ID/标题恢复会话 |
| `--fork-session` | 恢复时 fork 新 session ID |
| `-w`, `--worktree [<NAME>]` | 在新 git worktree 中启动（交互；`-p` 不建 worktree） |
| `--worktree-ref <REF>` | worktree 基线分支/tag/commit |
| `grok sessions` | 列出/搜索/恢复会话 |
| `grok inspect` | 展示本目录发现的配置（rules、skills、权限） |
| `grok export` | 导出会话 Markdown |

完整列表：`grok --help`。

## Prompt 骨架（架构 doc）

```bash
ROOT="$(git rev-parse --show-toplevel)"
prompt="$(cat <<EOF
仓库：$ROOT
先读：dev/progress/status.md、AGENTS.md、本轮 plan / roadmap
任务：<架构方案 / ADR / 挖 bug / Arch-First 审查>
交付：<改哪些 dev/plans|decisions|docs；或问题清单>
约束：不 commit；无关模块不改；文档用中文。
工作区保护：禁止 git checkout -- / restore / stash / clean。
EOF
)"
GROK_LOOP_AUTH='--no-plan --permission-mode bypassPermissions --always-approve'
grok $GROK_LOOP_AUTH -m grok-4.5 -p "$prompt"
```

## 能力与选型

| slug | 说明 |
|:-----|:-----|
| **`grok-4.5`** | CLI 默认；中强架构；**Loop 架构轨首选** |
| Cursor `Grok` | IDE 内档；**grok CLI 不可用**时的降级 |

对比 → [../models.md](../models.md)。

## Loop 门禁

| 当前环境 | `grok` CLI |
|:---------|:-----------|
| **已在 Grok 交互会话** | ❌ 不要再起同目录 `grok -p`；会话内继续 |
| **Cursor 内 · 架构/doc/bug** | ✅ **Shell `grok -p -m grok-4.5`**（**禁止 Task Grok**） |
| **其它环境 · 架构/doc/bug** | ✅ **Shell `grok -p -m grok-4.5`** |
| **任意环境 · 实施写代码** | ❌ 用当前环境实施模型（Cursor `Task` Composer…） |

同栈全文 → [../external-cli.md](../external-cli.md) · L2 → [../runtimes/grok.md](../runtimes/grok.md)。
