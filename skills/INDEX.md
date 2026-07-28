---
title: "Cursor Skills（可一键安装）"
type: index
status: accepted
phase: N/A
updated: 2026-07-28
summary: "跨项目可移植 Cursor skills；--personal 装全机，或装到任意仓库 .cursor/skills/。"
---

# Cursor Skills

本目录是 **Loop 套件内的 skill SSOT**（跨项目、无仓库专名）。  
技能正文**不**绑定某一产品仓库；装到哪，哪就能 `/skill-name` 手动调用。

## 一键安装（推荐两种）

在**套件根**（AgenticLoopDev 仓库根，或任意消费者的 `dev/loop/`）执行：

```bash
# A) 个人全局：一次安装，本机所有 Cursor 项目可用
./scripts/install-cursor-skills.sh --personal

# B) 指定任意项目仓库根（团队可 git 共享 .cursor/skills）
./scripts/install-cursor-skills.sh /path/to/AnyRepo

# C) 无参数：套件在 <repo>/dev/loop 时自动装到 <repo>；
#    在 submodule 内则优先装到 superproject
./scripts/install-cursor-skills.sh

# 只装某一个 / dry-run / 列表
./scripts/install-cursor-skills.sh --only sync-docs-and-commit --personal
./scripts/install-cursor-skills.sh --dry-run --personal
./scripts/install-cursor-skills.sh --list
```

| 目标 | 命令 | 适用 |
|:-----|:-----|:-----|
| `~/.cursor/skills/` | `--personal` | **多项目个人使用**（最通用） |
| `<repo>/.cursor/skills/` | 路径或自动探测 | 单仓库 / 团队共享 |

安装用 `rsync -a --delete`，目标侧同名 skill 与套件保持一致。

> 全量同步 Loop 套件仍见 [porting.md](../porting.md)。可只装 skills、不装整套 loop。

## 技能列表

| Skill | 手动调用 | 说明 |
|:------|:---------|:-----|
| [architecture-first-solution](architecture-first-solution/SKILL.md) | `/architecture-first-solution` | 问题类→选型→方案；**架构审查（≥中强）**；无 loop 亦可 |
| [sync-docs-and-commit](sync-docs-and-commit/SKILL.md) | `/sync-docs-and-commit` | 文档/行动层（有则更）→ 限定 commit；无 `dev/progress` 亦可 |

有 Loop 的仓库：plan 门禁另见 [architecture-first-design.md](../agent-playbooks/architecture-first-design.md)。

## 维护

- 改 skill → 只改本目录，再对 `--personal` 或各消费者重跑安装脚本  
- **禁止**在 skill 内写某仓库模块名、applicationId、构建命令  
- 路径只用「常见约定 / 探测存在则用」，见各 SKILL.md  
