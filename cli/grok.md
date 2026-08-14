---
title: "Grok CLI（grok）"
type: guide
status: accepted
phase: N/A
updated: 2026-08-14
summary: "Grok Build CLI：架构优先；直接 grok -p（勿 login）；跟 CLI default、勿硬编 -m；Loop 须 --no-plan+bypass+always-approve。"
---

# Grok CLI：`grok`

**Loop 优先级**：架构 / ADR / 方案主笔 / 挖 bug / Arch-First 审查 — **本仓库默认优先 `grok` CLI**，**高于 Cursor 内 `Task` Grok 模型档**。能力档见 [../models.md](../models.md)。

### Cursor 内 Loop

父 agent 在 **Cursor** 跑 `/loop` 时，架构轨仍用 **Shell 工具**调用本页命令，**不要**：

- 起 `Task` 并选 Grok 模型做架构主笔/审查 
- 为架构把 Cursor 聊天模型切成 Grok（实施轨保持 Composer/Auto）

## 前置

```bash
which grok
grok --version
grok models # 看 Default model（以本机为准）
```

**直接用**：本机已配好 CLI（常见为 `config.toml` 里 default 模型带 key）。**不要**在 Loop 里跑 `grok login`，也**不要**为委派去检查 / 补登录。

| ❌ 错误 | ✅ 正确 |
|:--------|:--------|
| Loop 里 `grok login` / 要求人类先登录 | 直接 `grok -p …` |
| 硬编 `-m grok-4.5`（本机 default 常为其它档） | **不传 `-m`**，跟 `grok models` 的 Default |
| `which grok` 失败仍空转 | 降级 Cursor `Task` Grok |

## 模型：跟 CLI 默认

```bash
grok models
# Default model: <以本机为准，常见 grok-4.6>
```

| 做法 | 说明 |
|:-----|:-----|
| **推荐** 不传 `-m` | 用本机 Default |
| 人类本 tick 写明 slug | 才加 `-m <slug>` |
| ❌ 文档/agent 自行钉死旧 slug | 易打到未配置的模型 → 空输出/挂起 |

能力对比表里的「Grok / grok-4.5」仍是能力档标签；**Shell 命令以本机 default 为准**。

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

Loop / 父 agent 委派架构 doc、方案、只读审计时，**默认用单轮 headless + 完全权限 + `--no-plan` + CLI 默认模型**：

```bash
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
GROK_LOOP_AUTH='--no-plan --permission-mode bypassPermissions --always-approve'

# ✅ 直接用；不传 -m → 本机 default
grok $GROK_LOOP_AUTH -p "$prompt"
# 或从文件：
grok $GROK_LOOP_AUTH --prompt-file /path/to/prompt.txt
# 仅当人类点名：
# grok $GROK_LOOP_AUTH -m <slug> -p "$prompt"
```

**反例**：

```bash
# ❌ 缺 --no-plan → 易绑 grok-build-plan
grok --permission-mode bypassPermissions --always-approve -p "$prompt"
# ❌ 仅 acceptEdits → headless 可能停在 permission_prompt
grok --no-plan --permission-mode acceptEdits --always-approve -p "$prompt"
# ❌ 硬编本机未作 default 的 -m（常见坑）
grok $GROK_LOOP_AUTH -m grok-4.5 -p "$prompt"
# ❌ Loop 里要求 login
grok login
```

| 参数 | 说明 |
|:-----|:-----|
| `-p`, `--single <PROMPT>` | 单轮 prompt，打印回复后退出（**Loop 委派首选**） |
| `-m`, `--model <MODEL>` | 可选；**默认省略**（跟 CLI default）；人类点名才传 |
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
grok $GROK_LOOP_AUTH -p "$(cat <<'EOF'
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
grok --no-plan --permission-mode bypassPermissions --always-approve "你的任务"
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
grok $GROK_LOOP_AUTH -p "$prompt"
```

## 能力与选型

| slug | 说明 |
|:-----|:-----|
| **CLI default**（常见 **`grok-4.6`**） | `grok models` 的 Default；**Loop Shell 首选（不传 `-m`）** |
| 其它档 | 仅人类点名时 `-m` |
| Cursor `Grok` | IDE 内档；**`which grok` 失败**时的降级 |

对比 → [../models.md](../models.md)。

## Loop 门禁

| 当前环境 | `grok` CLI |
|:---------|:-----------|
| **已在 Grok 交互会话** | ❌ 不要再起同目录 `grok -p`；会话内继续 |
| **Cursor 内 · 架构/doc/bug** | ✅ **Shell `grok -p`**（直接用；**禁止 Task Grok**；**禁止** Loop 内 `login`） |
| **其它环境 · 架构/doc/bug** | ✅ **Shell `grok -p`** |
| **`which grok` 失败** | 降级 Task Grok |
| **任意环境 · 实施写代码** | ❌ 用当前环境实施模型（Cursor `Task` Composer…） |

同栈全文 → [../external-cli.md](../external-cli.md) · L2 → [../runtimes/grok.md](../runtimes/grok.md)。
