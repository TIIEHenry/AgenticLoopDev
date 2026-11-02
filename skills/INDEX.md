---
title: "Cursor Skills：归属与安装"
type: index
status: accepted
phase: N/A
updated: 2026-11-02
summary: "一键安装只建 symlink/指针到套件内 SKILL.md；改 loop 无需重装。Arch-First / 多方评审均不自动触发。sync-worktrees 在合并工位语境下自动适用。"
---

# Cursor Skills

Loop 持有架构方案和多方方案评审技能，正文在本目录。
文档同步与提交技能由 ProjectWiki 独立维护，正文位于当前项目根目录的
`scripts/wiki/skills/sync-docs-and-commit/SKILL.md`。使用 Loop 不要求接入 ProjectWiki。

## 安装 Loop 技能

在套件根（AgenticLoopDev，或消费者的 `dev/loop/`）执行：

```bash
./scripts/install-cursor-skills.sh --personal
./scripts/install-cursor-skills.sh /path/to/AnyRepo
./scripts/install-cursor-skills.sh
```

| 模式 | 装到哪 | 机制 |
|:-----|:-------|:-----|
| `--personal` | `~/.cursor/skills/` | 薄入口，运行时读取当前仓库的 `dev/loop/skills/…/SKILL.md` |
| 项目 | `<repo>/.cursor/skills/` | 相对 symlink，指向套件内目录 |

安装不复制正文，Loop 技能正文更新后无需重装。目标中已有同名入口会被替换，先核对待保留的本地改动。

```bash
./scripts/install-cursor-skills.sh --list
./scripts/install-cursor-skills.sh --dry-run --personal
./scripts/install-cursor-skills.sh --only architecture-first-solution
./scripts/install-cursor-skills.sh --only sync-worktrees
./scripts/install-cursor-skills.sh --only multi-party-design-review
```

也可直接读取 `@dev/loop/skills/multi-party-design-review/SKILL.md`。

## 技能归属

| Skill | 正文归属与入口 |
|:------|:---------------|
| [architecture-first-solution](architecture-first-solution/SKILL.md) | Loop，本目录 |
| [multi-party-design-review](multi-party-design-review/SKILL.md) | Loop，本目录 |
| sync-docs-and-commit | ProjectWiki，当前项目根目录 `scripts/wiki/skills/sync-docs-and-commit/SKILL.md` |

有 Loop 的仓库：plan 门禁见 [architecture-first-design.md](../agent-playbooks/architecture-first-design.md)。

## 旧文档同步入口迁移

| Skill | 调用 | SSOT |
|:------|:-----|:-----|
| [architecture-first-solution](architecture-first-solution/SKILL.md) | 仅显式调用（`disable-model-invocation`；`/architecture-first-solution`） | 本目录 |
| [multi-party-design-review](multi-party-design-review/SKILL.md) | 仅显式调用（`disable-model-invocation`；`/multi-party-design-review` 或「启动多方评审」） | 本目录 |
| [sync-worktrees](sync-worktrees/SKILL.md) | `/sync-worktrees` 或「合并当前工作区和所有 worktree、保留未提交」 | 本目录（含 `scripts/`） |

[旧技能文件](sync-docs-and-commit/SKILL.md) 仅保留兼容转向，已有个人薄入口或项目 symlink 仍可经它读取 ProjectWiki 正文。
加载入口不授予提交权限；Loop 的独立验收、Commit Gate、槽位和收口规则继续适用。

新安装的列表和默认安装均跳过该兼容项；显式 `--only sync-docs-and-commit` 会说明迁移路径并失败退出，不创建或修改目标。
迁移已有入口时，先核对当前项目是否已有 ProjectWiki 正文，再按当前项目采用的技能发现方式指向它；不要复制正文或重新生成 Loop 同名入口。
目标尚未接入时报告迁移情况，依项目规则完成已授权收尾，不为加载技能强制移植套件或创建文档。

## 维护

- **只改**本目录 `SKILL.md`；项目 symlink 自动跟上正文  
- `--personal` 默认薄指针（复制 `description` / `disable-model-invocation`）。有 `scripts/` 的技能改为**整份拷贝** `SKILL.md` + `scripts/`（无 Loop 的仓库也能跑）。改 description、正文或脚本后须重跑 `./scripts/install-cursor-skills.sh --personal`（可加 `--only <name>`）  
- ProjectWiki 文档同步技能在 ProjectWiki 维护；本目录旧入口仅作兼容。
- 禁止在 skill 内写某仓库专名 / 构建命令  
- 勿再 `rsync` 复制 skill 正文到 `.cursor/skills/`（旧拷贝请删掉后重跑安装脚本）
