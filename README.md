# AgenticLoopDev

This repository is the loop suite itself.

Its repository root directly corresponds to the previous `dev/loop/` folder
contents so downstream projects can consume it as a submodule at `dev/loop/`.

Runtime state such as `loop.pid`, locks, caches, and local logs should live in
`dev/loop/.runtime/` inside the consumer repository and stay ignored by git.
