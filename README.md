# AgenticLoopDev

This repository is the loop suite itself.

Its repository root directly corresponds to the previous `dev/loop/` folder
contents so downstream projects can consume it as a submodule at `dev/loop/`.

Runtime state such as `loop.pid`, locks, caches, and local logs should live in
`dev/loop/.runtime/` inside the consumer repository and stay ignored by git.

## Cursor skills (manual invoke)

Portable skills under `skills/` — no product-repo names.

```bash
# All local Cursor projects
./scripts/install-cursor-skills.sh --personal

# One specific repo
./scripts/install-cursor-skills.sh /path/to/AnyRepo
```

Then `/architecture-first-solution` or `/sync-docs-and-commit`.
See `skills/INDEX.md` and `porting.md`.
