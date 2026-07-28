---
title: "Cursor Skills（可一键安装）"
type: index
status: accepted
phase: N/A
updated: 2026-07-28
summary: "Loop 套件内可移植 Cursor skills；用 scripts/install-cursor-skills.sh 装到项目 .cursor/skills/。"
---

# Cursor Skills

本目录是 **Loop 套件内的 skill SSOT**（跨项目、无仓库专名）。  
人类在目标仓库 **手动调用**（Cursor `/skill-name`）前，须先安装到该仓库的 `.cursor/skills/`。

## 一键安装

在**套件根**（本仓库根，或消费者的 `dev/loop/`）执行：

```bash
# 装到「当前目录所在 git 仓库」的 .cursor/skills/
./scripts/install-cursor-skills.sh

# 或指定目标仓库根
./scripts/install-cursor-skills.sh /path/to/TargetRepo

# 只装某一个
./scripts/install-cursor-skills.sh --only sync-docs-and-commit /path/to/TargetRepo

# 列出 / dry-run
./scripts/install-cursor-skills.sh --list
./scripts/install-cursor-skills.sh --dry-run
```

安装用 `rsync -a --delete`，目标侧同名 skill 目录与套件保持一致。

> **不是** loop tick 自动注入：`.cursor/skills/` 仍属项目侧；套件只提供源与安装脚本。  
> 全量同步套件仍用 [porting.md](../porting.md) 的 `rsync`；skills 可随套件复制，或单独跑本脚本刷新。

## 技能列表

| Skill | 手动调用 | 说明 |
|:------|:---------|:-----|
| [architecture-first-solution](architecture-first-solution/SKILL.md) | `/architecture-first-solution` | 问题类→选型→方案；**架构审查（≥中强）** |
| [sync-docs-and-commit](sync-docs-and-commit/SKILL.md) | `/sync-docs-and-commit` | 同步文档/行动层 → 限定范围 commit（默认不 push） |

Loop 内对应契约：[architecture-first-design.md](../agent-playbooks/architecture-first-design.md)（plan 门禁与 Reviewer）。

## 维护

- 改 skill 正文 → 只改本目录，再对消费者跑 `install-cursor-skills.sh`
- 禁止在 skill 内写某仓库模块名 / 构建命令；项目路径约定用 `dev/progress/`、`dev/plans/` 等相对约定
