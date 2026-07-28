# AgenticLoopDev

This repository is the loop suite itself.

Its repository root directly corresponds to the previous `dev/loop/` folder
contents so downstream projects can consume it as a submodule at `dev/loop/`.

Runtime state such as `loop.pid`, locks, caches, and local logs should live in
`dev/loop/.runtime/` inside the consumer repository and stay ignored by git.

## Cursor skills (manual invoke)

SSOT: `skills/<name>/SKILL.md`. Install only creates symlink/pointer — **no reinstall** when the suite changes.

```bash
./scripts/install-cursor-skills.sh --personal          # @dev/loop/skills/... per workspace
./scripts/install-cursor-skills.sh /path/to/AnyRepo  # symlink into that repo
```

Or `@dev/loop/skills/sync-docs-and-commit/SKILL.md` directly.
See `skills/INDEX.md`.
