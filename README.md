# AgenticLoopDev

This repository is the loop suite itself.

Its repository root directly corresponds to the previous `dev/loop/` folder
contents so downstream projects can consume it as a submodule at `dev/loop/`.

Runtime state such as `loop.pid`, locks, caches, and local logs should live in
`dev/loop/.runtime/` inside the consumer repository and stay ignored by git.

## Cursor skills (manual invoke)

Portable skills live under `skills/`. Install into a project:

```bash
./scripts/install-cursor-skills.sh /path/to/TargetRepo
```

Then use `/architecture-first-solution` or `/sync-docs-and-commit` in Cursor.
See `skills/INDEX.md` and `porting.md`.
