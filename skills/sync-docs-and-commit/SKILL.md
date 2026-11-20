---
name: sync-docs-and-commit
description: >-
  Compatibility entry for the ProjectWiki sync-docs-and-commit skill. Read the
  current project root scripts/wiki/skills/sync-docs-and-commit/SKILL.md.
---

# 文档同步与提交：兼容入口

正文已迁到 ProjectWiki。先定位当前项目根目录，读取
`scripts/wiki/skills/sync-docs-and-commit/SKILL.md`，按该文件和当前项目规则处理。
加载本入口或目标技能本身不授予 commit / push 权限；先核对本次用户授权。
Loop 会话仍须遵守 Overall Verification、Commit Gate、槽位和收口门禁。

若目标文件不存在，报告此旧入口需要迁移，按当前项目规则处理已获授权的收尾；
不要求为此移植 Loop 或 ProjectWiki，也不补造计划、状态或归档文档。
