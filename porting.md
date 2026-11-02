---
title: "Loop 套件移植与同步"
type: guide
status: accepted
phase: N/A
updated: 2026-11-02
summary: "Loop 套件移植与同步；不绑定消费仓库任务内容；合入时机见 closeout 转换表；skills 一键安装。"
---

# Loop 套件移植与同步

本仓库根目录就是套件内容，消费者通常放在 `dev/loop/`。套件只维护调度协议、playbook 与技能，不保存项目的任务、构建命令或文档生命周期规则。worktree / 集成分支对齐只能用 Git，不能用下文的目录复制。

## 套件治理

- 人类明确要求维护套件时，可以修改源仓；自主 Loop tick 不得自行修改 `dev/loop/**`。未授权修改使 Overall Verification 为 `FAIL`、Commit Gate 为 `NOT_READY`。
- 项目需要改变套件时，把建议记入项目待处理项或人类会话。源仓修改和消费者升级分别核对，不自动同步所有仓库。
- pid、锁、缓存与日志只放消费者 `dev/loop/.runtime/`，由套件 `.gitignore` 忽略。升级不得覆盖或删除运行态。

## 项目侧绑定

在项目已有的开发入口（通常为 `dev/INDEX.md`，或根 `AGENTS.md` 指向的入口）用一个短节登记下列角色。**角色映射只维护这一处**，根 `AGENTS.md` 和派工提示链接该入口；不另建配置文件，也不复制任务进度。

| 角色 | 按项目实际填写 |
|:-----|:-----------------|
| 任务来源 | 用户已授权目标、需求条目、已有计划或任务清单的路径；注明采用哪些来源 |
| 执行与协调记录 | 当前任务记录及并行协调入口；若启用 worktree 池，在这里登记槽位/波次记录的位置 |
| 待处理项来源 | 未完成问题、延期缺口、待调查问题的唯一入口；可共用一份待办，以类型或文字区分 |
| 验证入口 | 实际命令及适用范围的权威入口，含文档检查与提交检查 |
| 归档约定 | 项目现有的完成记录保留、清理和归档规则入口 |

只登记实际采用的角色；不需要的角色明确写“无/未采用”，不为接入造空表或计划。已有 status 或 parallel board 承担恢复/槽位契约时继续使用，不能仅因减少文档而删除它。

单项轻量工作无需额外看板，执行与协调记录角色可写“无”。单任务跨会话恢复可复用已有任务记录或提交证据，只需能定位任务、未完成事项和恢复依据；不得强加未使用的槽位、波次等并发字段。角色写“无”不能作为丢失这些恢复依据的理由；依据不足时先补齐再恢复工作。

启用并发 worktree 池时，必须先绑定能保存 slice、冲突域、写者、槽位状态、波次成员、阻塞原因、验证与收口结果的协调记录。角色仍为“无”或记录不可用时停止并发派工并补齐绑定，不能跳过实际采用机制所需的槽位、冲突隔离或 closeout 门禁。

**读取顺序**：根 `AGENTS.md` → 其开发入口中的绑定 → 本轮相关来源。本文及套件其他文件中的 `dev/progress/`、`dev/roadmap/active/`、`dev/parallel/active/` 是未声明绑定时的默认布局示例。声明了绑定就按实际路径读取；显式未采用的来源不再要求读取、创建或更新，不能因旧目录碰巧存在而恢复旧约束。父 agent 派工时传入绑定入口和本轮具体来源。

未声明绑定的既有项目继续使用原布局：`dev/progress/status.md`、`deferred-gaps.md`、`research-queue.md`、`health-gates.md`，已有 active roadmap / parallel board 仍参与调度。默认队列格式见 [subagent-loop-startup.md](agent-playbooks/subagent-loop-startup.md)。迁移时先盘点仍在使用的记录，再在已有入口登记替代关系，不能丢失未完成任务和运行中的槽位。

### 与 ProjectWiki 配合

ProjectWiki 管需求、知识文档、生命周期、固定格式和文档检查；Loop 管派工、冲突隔离、槽位恢复、独立验收和收口。项目绑定使用 ProjectWiki 的实际入口，不复制一套 phase / status / 双队列。

任务记录的轻重服从项目规则：已授权且目标、边界、验收明确的普通修复可直接 `implement`，依据与验证可记在已有任务记录或提交说明；有重要风险、跨模块协调或交接需要时再建计划；涉及应保留的设计取舍或推翻已有决策时按项目规则写 ADR。没有计划文件本身不构成阻塞，也不能降低派工单、独立验收和恢复证据要求。

验证从项目登记入口选择与影响范围一致的命令；记录实际命令、输入范围和输出，工作区验证不能冒充 staged 验证。采用 ProjectWiki 的项目按根目录 `scripts/wiki/skills/sync-docs-and-commit/SKILL.md` 及其链接的项目规则同步文档、处理提交提醒。Loop 不复制这些规则；未接入 ProjectWiki 的项目按自己的验证与提交规则处理。独立验收、Commit Gate 和槽位收口门禁仍由 Loop 执行。

## 首次接入与升级

先确认消费者采用子模块还是普通目录。升级前检查源仓、目标仓和目标套件的状态，保留项目改动；有未提交套件修改、未处理 gitlink 变化或运行中写入时先停止升级并报告，不能覆盖。下文命令为示例，不代表授权对所有消费者升级。

### Git 子模块

子模块用 Git 固定具体提交，不用 rsync。首次接入（在消费者根目录，替换 URL 和提交）：

```bash
git status --short
git submodule add <suite-repository-url> dev/loop
git -C dev/loop checkout --detach <reviewed-suite-commit>
git diff -- .gitmodules dev/loop
```

已有子模块升级时，先确认 `.gitmodules`、套件 gitlink 与子模块内容没有待处理改动，且当前子模块 HEAD 与父仓登记版本一致；其他无关 WIP 保留，不要求清理整个消费者工作区；已声明但尚未初始化的子模块先用 `git submodule update --init -- dev/loop` 检出父仓登记版本。不要把父仓尚未登记的套件 HEAD 当作升级起点。

```bash
git status --short -- .gitmodules dev/loop
git submodule status -- dev/loop
git -C dev/loop status --short
git -C dev/loop fetch origin
git -C dev/loop show --stat <reviewed-suite-commit>
git -C dev/loop checkout --detach <reviewed-suite-commit>
git diff --submodule=log -- dev/loop
```

检查实际变化后，在消费者提交 gitlink；首次接入还须提交 `.gitmodules`。不自动推送。子模块不能访问固定提交时先解决版本来源，不能改用目录覆盖。

### 普通目录复制

`SRC` 是本源仓根目录，**不是** `$SRC/dev/loop/`。若维护的是另一消费者内的普通副本，才将 `SRC` 指向它的套件目录。先核对源套件无未提交修改，目标不是子模块且 `dev/loop/` 没有待保留的本地差异；忽略文件也须检查，不能仅凭 `git status` 干净认定可覆盖。

```bash
SRC=/path/to/AgenticLoopDev
DEST=/path/to/TargetRepo
git -C "$SRC" status --short
git -C "$DEST" status --short -- dev/loop
git -C "$DEST" ls-files --stage -- dev/loop
git -C "$DEST" status --short --ignored -- dev/loop
rsync -anci --delete --exclude='.git' --exclude='.runtime/' "$SRC/" "$DEST/dev/loop/"
```

`ls-files --stage` 若显示 mode `160000`，改走子模块路线。检查预览中的覆盖和删除：保留本地修改与运行态，确认源和目标路径正确后才执行同参数实拷贝：

```bash
rsync -ac --delete --exclude='.git' --exclude='.runtime/' "$SRC/" "$DEST/dev/loop/"
```

不使用 `--delete-excluded`；`.git`（文件或目录）和 `.runtime/` 不能跨仓复制或删除。`--delete` 仅在核对过的普通副本内清除旧套件文件，不能对 worktree 或整个仓库使用。

## 接入后的核对

1. 根 `AGENTS.md` 链接项目开发入口及 `dev/loop/INDEX.md`，项目绑定指向实际存在的来源。
2. 按绑定读取真实任务、协调状态、待处理项和验证入口；无绑定旧项目核对默认布局。检查显式未采用的来源不会被强制读取。
3. 用一项边界明确的任务核对 `implement` 派工、独立验收和恢复字段；无可执行任务时记录穷尽证据并停止，不自动造计划。
4. 按项目登记命令验证实际影响范围。静态阅读和临时项目 smoke 不能称为真实 Loop 运行成功。
5. 核对套件 diff、项目绑定 diff、运行态未变，再按本次授权提交。旧入口是否删除由项目迁移范围决定，先保留未完成记录。

## Cursor skills（可选）

安装脚本只安装 Loop 持有的架构与多方方案评审技能，创建指向套件的 symlink / 指针，正文更新后无需重装：

```bash
./dev/loop/scripts/install-cursor-skills.sh --personal
./dev/loop/scripts/install-cursor-skills.sh
/path/to/AgenticLoopDev/scripts/install-cursor-skills.sh /path/to/AnyRepo
```

也可直接读取 Loop 对应的 `@dev/loop/skills/<name>/SKILL.md`。文档同步与提交技能由 ProjectWiki 独立维护，目标为当前项目根目录 `scripts/wiki/skills/sync-docs-and-commit/SKILL.md`；旧 Loop 文件只兼容已有指针，新安装跳过它，显式安装会失败并提示迁移。目标缺失不要求强制接入 ProjectWiki，按当前项目规则处理已授权收尾。加载技能不授予提交权限。归属与旧入口迁移见 [skills/INDEX.md](skills/INDEX.md)。项目具体构建命令只改项目验证入口，不写进套件。

## 相关

- [INDEX.md](INDEX.md) — 套件索引
- [execution-contract.md](execution-contract.md) — 任务选择与调度
- [worktrees.md](worktrees.md)、[worktree-closeout.md](worktree-closeout.md) — 槽位与收口
- [health-gates.md](health-gates.md) — 验证时机
