---
title: "Cursor Skills（指向 Loop SSOT）"
type: index
status: accepted
phase: N/A
updated: 2026-07-29
summary: "一键安装只建 symlink/指针到套件内 SKILL.md；改 loop 无需重装。"
---

# Cursor Skills

**SSOT 永远在本目录** `skills/<name>/SKILL.md`。  
一键安装**不复制正文**，只让 Cursor 能发现并手动调用；loop 更新后**不必再安装**。

## 一键安装

在套件根（AgenticLoopDev，或消费者的 `dev/loop/`）执行：

```bash
# 推荐：本机所有项目 — 薄指针，运行时 @ 当前仓库的 dev/loop/skills/.../SKILL.md
./scripts/install-cursor-skills.sh --personal

# 单仓库：相对 symlink → dev/loop/skills/<name>
./scripts/install-cursor-skills.sh /path/to/AnyRepo
./scripts/install-cursor-skills.sh   # 套件在 <repo>/dev/loop 时自动指向该 repo
```

| 模式 | 装到哪 | 机制 | loop 改了还要装吗 |
|:-----|:-------|:-----|:------------------|
| `--personal` | `~/.cursor/skills/` | 薄包装：强制 Read/`@dev/loop/skills/…/SKILL.md` | **否** |
| 项目 | `<repo>/.cursor/skills/` | **symlink** → 套件内目录 | **否** |

```bash
./scripts/install-cursor-skills.sh --list
./scripts/install-cursor-skills.sh --dry-run --personal
./scripts/install-cursor-skills.sh --only sync-docs-and-commit
./scripts/install-cursor-skills.sh --only multi-party-design-review
```

也可不安装、直接在对话里：

```text
@dev/loop/skills/multi-party-design-review/SKILL.md
```

## 技能列表

| Skill | 调用 | SSOT |
|:------|:-----|:-----|
| [architecture-first-solution](architecture-first-solution/SKILL.md) | `/architecture-first-solution` | 本目录 |
| [multi-party-design-review](multi-party-design-review/SKILL.md) | `/multi-party-design-review` | 本目录 |
| [sync-docs-and-commit](sync-docs-and-commit/SKILL.md) | `/sync-docs-and-commit` | 本目录 |

有 Loop 的仓库：plan 门禁见 [architecture-first-design.md](../agent-playbooks/architecture-first-design.md)；多方方案评审见本目录 multi-party-design-review。

## 维护

- **只改**本目录 `SKILL.md`；已 symlink/指针的消费者自动跟上  
- 禁止在 skill 内写某仓库专名 / 构建命令  
- 勿再 `rsync` 复制 skill 正文到 `.cursor/skills/`（旧拷贝请删掉后重跑安装脚本）
