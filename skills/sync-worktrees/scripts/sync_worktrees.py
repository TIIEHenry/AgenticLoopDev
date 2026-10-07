#!/usr/bin/env python3
"""Inventory / plan / cascade / verify git worktrees.

Never reset, stash, restore, checkout -B, or clean. The only write
subcommand is cascade, which runs `git merge --ff-only` per station.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

BANNED = (
    "git reset --hard",
    "git reset --keep",
    "git checkout --",
    "git checkout -B",
    "git restore",
    "git stash",
    "git clean",
    "git merge -X ours",
    "git merge -X theirs",
    "git add -A (merge commit)",
    "rsync of a worktree",
)


class GitError(RuntimeError):
    def __init__(self, args: list[str], returncode: int, stderr: str):
        super().__init__(f"git {' '.join(args)} -> {returncode}: {stderr.strip()}")
        self.returncode = returncode
        self.stderr = stderr


def git(cwd: str | Path, *args: str, check: bool = True, quiet: bool = False) -> str:
    cmd = ["git", "-C", str(cwd), *args]
    env = os.environ.copy()
    env.setdefault("GIT_TERMINAL_PROMPT", "0")
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    if check and proc.returncode != 0:
        raise GitError(list(args), proc.returncode, proc.stderr)
    if not quiet and proc.stderr.strip() and proc.returncode == 0:
        pass
    return proc.stdout


def git_ok(cwd: str | Path, *args: str) -> bool:
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return proc.returncode == 0


def git_code(cwd: str | Path, *args: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


@dataclass
class DirtyFile:
    status: str
    path: str
    blob: Optional[str]
    kind: str  # file | missing | submodule | other


@dataclass
class Station:
    role: str
    path: str
    head: str
    branch: Optional[str]
    detached: bool
    locked: bool
    vs_merge: str
    unique_count: int
    unique_sample: list[str]
    dirty_count: int
    stash_count: int
    rebase: bool
    merge_in_progress: bool
    dirty: list[DirtyFile] = field(default_factory=list)


def discover_repo(start: Optional[str] = None) -> str:
    cwd = start or os.getcwd()
    code, out, err = git_code(cwd, "rev-parse", "--show-toplevel")
    if code != 0:
        raise SystemExit(f"not a git repo ({cwd}): {err.strip()}")
    return out.strip()


def parse_worktree_porcelain(text: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    cur: dict[str, Any] = {}
    for raw in text.splitlines():
        if raw == "":
            if cur:
                blocks.append(cur)
                cur = {}
            continue
        if raw.startswith("worktree "):
            if cur:
                blocks.append(cur)
            cur = {"path": raw[len("worktree ") :], "detached": False, "locked": False, "branch": None, "head": ""}
        elif raw.startswith("HEAD "):
            cur["head"] = raw[len("HEAD ") :]
        elif raw.startswith("branch "):
            ref = raw[len("branch ") :]
            cur["branch"] = ref[len("refs/heads/") :] if ref.startswith("refs/heads/") else ref
        elif raw == "detached":
            cur["detached"] = True
        elif raw.startswith("locked"):
            cur["locked"] = True
    if cur:
        blocks.append(cur)
    return blocks


def classify(path: str, main_path: str, branch: Optional[str]) -> str:
    try:
        if os.path.samefile(path, main_path):
            return "human"
    except OSError:
        if os.path.abspath(path) == os.path.abspath(main_path):
            return "human"
    name = os.path.basename(os.path.abspath(path))
    if name == "merge" or branch in {"loop/merge", "merge"}:
        return "merge"
    if len(name) == 1 and "A" <= name <= "J":
        return "letter"
    return "other"


def infer_wt_root(main_path: str, stations: list[dict[str, Any]]) -> str:
    main_base = os.path.basename(os.path.abspath(main_path))
    for st in stations:
        parent = os.path.dirname(os.path.abspath(st["path"]))
        parent_base = os.path.basename(parent)
        if parent_base.lower() in {
            f"{main_base}-worktrees",
            f"{main_base.lower()}-worktrees",
        }:
            return parent
    return os.path.join(os.path.dirname(os.path.abspath(main_path)), f"{main_base}-WorkTrees")


def parse_status_z(payload: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    parts = payload.split("\0")
    i = 0
    while i < len(parts) and parts[i] != "":
        item = parts[i]
        xy = item[:2]
        path = item[3:] if len(item) > 3 else item[2:].lstrip()
        if "R" in xy or "C" in xy:
            dest = parts[i + 1] if i + 1 < len(parts) else path
            entries.append((xy, dest))
            i += 2
        else:
            entries.append((xy, path))
            i += 1
    return entries


def blob_for(path: str, rel: str, xy: str) -> tuple[str, Optional[str]]:
    full = os.path.join(path, rel)
    if os.path.isdir(os.path.join(full, ".git")) or os.path.isfile(os.path.join(full, ".git")):
        code, out, _ = git_code(full, "rev-parse", "HEAD")
        return "submodule", out.strip() if code == 0 else None
    if not os.path.exists(full):
        return "missing", None
    if os.path.isdir(full):
        return "other", None
    code, out, _ = git_code(path, "hash-object", "--", rel)
    if code == 0:
        return "file", out.strip()
    return "other", None


def stash_count(path: str) -> int:
    code, out, _ = git_code(path, "stash", "list")
    if code != 0 or not out.strip():
        return 0
    return len([ln for ln in out.splitlines() if ln.strip()])


def in_progress(path: str, name: str) -> bool:
    git_dir = git(path, "rev-parse", "--git-dir").strip()
    return os.path.exists(os.path.join(path, git_dir, name)) or os.path.exists(
        os.path.join(git_dir, name)
    )


def vs_merge_label(repo: str, head: str, merge_head: Optional[str]) -> tuple[str, int, list[str]]:
    if not merge_head:
        return "unknown", 0, []
    if head == merge_head:
        return "equal", 0, []
    head_in_merge = git_ok(repo, "merge-base", "--is-ancestor", head, merge_head)
    merge_in_head = git_ok(repo, "merge-base", "--is-ancestor", merge_head, head)
    if head_in_merge and merge_in_head:
        return "equal", 0, []
    if head_in_merge:
        return "behind", 0, []
    code, out, _ = git_code(repo, "rev-list", "--oneline", f"{merge_head}..{head}")
    sample = [ln for ln in out.splitlines() if ln.strip()]
    unique = len(sample)
    sample = sample[:8]
    if merge_in_head:
        return "ahead", unique, sample
    return "diverged", unique, sample


def resolve_ref(repo: str, *candidates: str) -> Optional[str]:
    for ref in candidates:
        code, out, _ = git_code(repo, "rev-parse", "--verify", "--quiet", ref)
        if code == 0 and out.strip():
            return out.strip()
    return None


def collect(repo: str) -> dict[str, Any]:
    porcelain = git(repo, "worktree", "list", "--porcelain")
    raw = parse_worktree_porcelain(porcelain)
    if not raw:
        raise SystemExit("git worktree list returned no worktrees")
    main_path = raw[0]["path"]
    merge_raw = next((x for x in raw if classify(x["path"], main_path, x.get("branch")) == "merge"), None)
    merge_head = merge_raw["head"] if merge_raw else None
    origin_main = resolve_ref(repo, "origin/main", "refs/remotes/origin/main")
    local_main = resolve_ref(repo, "main", "refs/heads/main")
    integration = merge_head or origin_main or local_main or raw[0]["head"]

    stations: list[Station] = []
    for item in raw:
        path = item["path"]
        head = item.get("head") or ""
        branch = item.get("branch")
        role = classify(path, main_path, branch)
        vs, unique, sample = vs_merge_label(path, head, integration)
        try:
            status_z = git(path, "status", "--porcelain", "-z")
            dirty_pairs = parse_status_z(status_z)
        except GitError:
            dirty_pairs = []
        dirty: list[DirtyFile] = []
        for xy, rel in dirty_pairs:
            kind, blob = blob_for(path, rel, xy)
            dirty.append(DirtyFile(status=xy, path=rel, blob=blob, kind=kind))
        st = Station(
            role=role,
            path=path,
            head=head,
            branch=branch,
            detached=bool(item.get("detached")),
            locked=bool(item.get("locked")),
            vs_merge=vs,
            unique_count=unique,
            unique_sample=sample,
            dirty_count=len(dirty),
            stash_count=stash_count(path),
            rebase=in_progress(path, "rebase-merge") or in_progress(path, "rebase-apply"),
            merge_in_progress=in_progress(path, "MERGE_HEAD"),
            dirty=dirty,
        )
        stations.append(st)

    wt_root = infer_wt_root(main_path, raw)
    origin_vs = None
    if origin_main:
        label, n, sample = vs_merge_label(repo, origin_main, integration)
        origin_vs = {"sha": origin_main, "vs_merge": label, "unique_count": n, "unique_sample": sample[:8]}

    tips: list[dict[str, Any]] = []
    seen: set[str] = set()
    if origin_vs and origin_vs["unique_count"] > 0 and origin_vs["vs_merge"] in {"ahead", "diverged"}:
        tips.append(
            {
                "source": "origin/main",
                "role": "remote",
                "path": None,
                "branch": "origin/main",
                "head": origin_main,
                "unique_count": origin_vs["unique_count"],
                "unique_sample": origin_vs["unique_sample"],
            }
        )
        seen.add(origin_main or "")
    for st in stations:
        if st.role == "merge":
            continue
        if st.head in seen:
            continue
        if st.unique_count <= 0 or st.vs_merge in {"equal", "behind"}:
            continue
        seen.add(st.head)
        tips.append(
            {
                "source": st.role,
                "role": st.role,
                "path": st.path,
                "branch": st.branch,
                "head": st.head,
                "unique_count": st.unique_count,
                "unique_sample": st.unique_sample,
            }
        )
    tips.sort(key=lambda t: (0 if t["role"] == "remote" else 1, t["unique_count"], t["head"]))

    merge_station = next((s for s in stations if s.role == "merge"), None)
    human = next((s for s in stations if s.role == "human"), stations[0])
    return {
        "repo": os.path.abspath(main_path),
        "wt_root": wt_root,
        "merge_path": merge_station.path if merge_station else None,
        "merge_branch": merge_station.branch if merge_station else None,
        "merge_head": merge_head,
        "integration": integration,
        "origin_main": origin_vs,
        "local_main": local_main,
        "human": {
            "path": human.path,
            "branch": human.branch,
            "head": human.head,
            "dirty_count": human.dirty_count,
            "stash_count": human.stash_count,
        },
        "stations": [station_dict(s) for s in stations],
        "tips_to_merge": tips,
        "banned": list(BANNED),
        "notes": notes_for(stations, merge_station, wt_root),
    }


def station_dict(s: Station) -> dict[str, Any]:
    d = asdict(s)
    return d


def notes_for(stations: list[Station], merge: Optional[Station], wt_root: str) -> list[str]:
    notes: list[str] = []
    if merge is None:
        notes.append(f"no merge slot; create with: git worktree add -b loop/merge {wt_root}/merge <origin/main|main>")
    if merge and merge.dirty_count:
        notes.append(
            "merge slot is dirty: keep that WIP on disk; merge other tips anyway; "
            "if git refuses overlapping paths, stop; never stash/commit to clear it; merge commit must not git add -A"
        )
    if merge and (merge.rebase or merge.merge_in_progress):
        notes.append("merge slot has rebase/merge in progress: finish or report; do not --abort if it would drop resolved hunks you need")
    for s in stations:
        if s.rebase or s.merge_in_progress:
            notes.append(f"{s.role} {s.branch or s.path} has rebase/merge in progress: leave it; do not abort/reset")
        if s.locked:
            notes.append(f"locked worktree skipped for writes: {s.path}")
        if s.dirty_count:
            notes.append(
                f"{s.role} {s.branch or s.path} has {s.dirty_count} uncommitted path(s): "
                "keep on disk; merge only existing HEAD; cascade ff-only may refuse on overlap — leave as-is"
            )
    notes.append("integrate with git merge (not rebase) so each source HEAD stays an ancestor of MERGE_SHA")
    notes.append("cascade every station with git merge --ff-only MERGE_SHA; never checkout -B on any station")
    notes.append("do not commit uncommitted files on any station (human, merge, letter, other) unless the user explicitly asks")
    notes.append("verify: snapshot dirty blobs must still hash the same on that station's disk; in-HEAD is not enough")
    notes.append("do not push unless the user asks")
    return notes


def print_inventory(data: dict[str, Any]) -> None:
    print(f"repo:        {data['repo']}")
    print(f"wt_root:     {data['wt_root']}")
    print(f"merge:       {data['merge_path'] or '(missing)'}  branch={data['merge_branch']}  HEAD={(data['merge_head'] or '')[:12]}")
    print(
        f"human:       {data['human']['path']}  branch={data['human']['branch']}  "
        f"HEAD={data['human']['head'][:12]}  dirty={data['human']['dirty_count']}  stash={data['human']['stash_count']}"
    )
    if data.get("origin_main"):
        om = data["origin_main"]
        print(f"origin/main: {om['sha'][:12]}  vs_merge={om['vs_merge']}  unique={om['unique_count']}")
    print()
    print(f"{'role':<8} {'branch':<22} {'HEAD':<12} {'vs_merge':<10} {'uniq':>4} {'dirty':>5} {'stash':>5}  path")
    for s in data["stations"]:
        print(
            f"{s['role']:<8} {(s['branch'] or '(detached)'):<22} {s['head'][:12]:<12} "
            f"{s['vs_merge']:<10} {s['unique_count']:>4} {s['dirty_count']:>5} {s['stash_count']:>5}  {s['path']}"
        )
    print()
    tips = data["tips_to_merge"]
    if not tips:
        print("tips to merge: (none — every station HEAD is already in the integration commit)")
    else:
        print("tips to merge into the merge slot (deduped HEADs, merge not rebase):")
        for i, t in enumerate(tips, 1):
            br = t["branch"] or t["head"][:12]
            print(f"  {i}. [{t['role']}] {br}  {t['head'][:12]}  unique={t['unique_count']}")
            for line in t["unique_sample"][:5]:
                print(f"       {line}")
    print()
    print("notes:")
    for n in data["notes"]:
        print(f"  - {n}")
    print()
    print("banned:", ", ".join(BANNED))


def print_plan(data: dict[str, Any]) -> None:
    merge = data["merge_path"]
    print("# plan: gather unique commits, then ff-only cascade")
    print("# keep uncommitted edits on every station; never reset / stash / restore / checkout -B / clean / commit WIP")
    if not merge:
        base = "origin/main" if data.get("origin_main") else ("main" if data.get("local_main") else "HEAD")
        print(f"mkdir -p {data['wt_root']}")
        print(f"git worktree add -b loop/merge {data['wt_root']}/merge {base}")
        print("# re-run inventory after the merge slot exists")
        return
    print("git fetch origin --prune")
    print(f"# all merges happen in: {merge}")
    merge_st = next(s for s in data["stations"] if s["role"] == "merge")
    if merge_st["dirty_count"]:
        print(f"# merge slot has {merge_st['dirty_count']} dirty paths: do not commit/stash them; do not git add -A")
    for t in data["tips_to_merge"]:
        src = t["branch"] or t["head"]
        if t["role"] != "remote" and t.get("path"):
            st = next(s for s in data["stations"] if s["path"] == t["path"])
            if st["dirty_count"]:
                print(f"# {st['role']} {src} has {st['dirty_count']} dirty paths: merge HEAD {t['head'][:12]} only; leave WIP on disk")
        print(f"git -C {merge} merge --no-edit {src}")
        print("# on conflict: true 3-way keep-both; no -X ours/theirs; no checkout --ours/--theirs whole file")
    print("# MERGE_SHA=$(git -C merge_path rev-parse HEAD)")
    print(f"python3 {Path(__file__).resolve()} cascade MERGE_SHA")
    print(f"python3 {Path(__file__).resolve()} verify --snapshot SNAP.json --expect-sha MERGE_SHA")


def cascade(repo: str, merge_sha: str, dry_run: bool) -> int:
    full = git(repo, "rev-parse", "--verify", merge_sha).strip()
    data = collect(repo)
    rc = 0
    print(f"cascade to {full}")
    for s in data["stations"]:
        label = f"{s['role']}:{s['branch'] or s['path']}"
        if s["locked"]:
            print(f"SKIP {label} locked")
            continue
        if s["rebase"] or s["merge_in_progress"]:
            print(f"SKIP {label} in-progress rebase/merge")
            rc = max(rc, 2)
            continue
        if s["head"] == full:
            print(f"OK   {label} already at MERGE_SHA")
            continue
        if not git_ok(s["path"], "merge-base", "--is-ancestor", s["head"], full):
            print(f"SKIP {label} HEAD is not an ancestor of MERGE_SHA (unique commits not in the integration)")
            rc = max(rc, 2)
            continue
        cmd = ["merge", "--ff-only", "--no-edit", full]
        if dry_run:
            print(f"DRY  {label} git -C {s['path']} {' '.join(cmd)}")
            continue
        code, out, err = git_code(s["path"], *cmd)
        text = (out + err).strip().replace("\n", " | ")
        if code == 0:
            print(f"OK   {label} {text or 'ff-only'}")
        else:
            print(f"FAIL {label} {text}")
            print("     leave the worktree as-is; do not stash/reset/restore/commit WIP to retry")
            rc = max(rc, 1)
    return rc


def verify(repo: str, snapshot_path: str, expect_sha: Optional[str]) -> int:
    snap = json.loads(Path(snapshot_path).read_text(encoding="utf-8"))
    data = collect(repo)
    now_by_path = {s["path"]: s for s in data["stations"]}
    rc = 0
    if expect_sha:
        expect = git(repo, "rev-parse", "--verify", expect_sha).strip()
        for s in data["stations"]:
            if s["role"] == "human":
                if s["head"] != expect:
                    print(f"FAIL human HEAD {s['head'][:12]} != MERGE_SHA {expect[:12]}")
                    rc = 1
                else:
                    print(f"OK   human at MERGE_SHA {expect[:12]}")
            elif s["head"] == expect:
                print(f"OK   {s['role']}:{s['branch']} at MERGE_SHA")
            elif git_ok(s["path"], "merge-base", "--is-ancestor", s["head"], expect):
                print(f"WARN {s['role']}:{s['branch']} still behind MERGE_SHA")
                rc = max(rc, 2)
            else:
                print(f"WARN {s['role']}:{s['branch']} not at MERGE_SHA (unique work kept on its branch)")
                rc = max(rc, 2)
    lost: list[str] = []
    for old in snap.get("stations", []):
        cur = now_by_path.get(old["path"])
        if not cur:
            print(f"WARN worktree disappeared: {old['path']}")
            rc = max(rc, 2)
            continue
        cur_paths = {d["path"] for d in cur["dirty"]}
        for d in old.get("dirty", []):
            rel = d["path"]
            blob = d.get("blob")
            status = (d.get("status") or "")
            untracked = "?" in status
            deleted = (not untracked) and ("D" in status[:2])
            full = os.path.join(old["path"], rel)
            kind = d.get("kind") or ""
            if deleted:
                if os.path.exists(full):
                    lost.append(f"{old['role']} deleted {rel} was restored on disk")
                continue
            if blob:
                if kind == "submodule":
                    code, out, _ = git_code(full, "rev-parse", "HEAD")
                    if code == 0 and out.strip() == blob:
                        continue
                    lost.append(f"{old['role']} submodule {rel} HEAD moved (was {blob[:8]})")
                    continue
                if disk_blob(old["path"], rel, kind) == blob:
                    continue
                lost.append(f"{old['role']} {rel} blob {blob[:8]} no longer on disk in {old['path']}")
            elif untracked:
                if os.path.exists(full) or rel in cur_paths:
                    continue
                lost.append(f"{old['role']} untracked {rel} disappeared from {old['path']}")
    if lost:
        rc = 1
        print("FAIL modifications lost:")
        for line in lost:
            print(f"  - {line}")
    else:
        print("OK   snapshot dirty blobs still on disk in every station")
    return rc


def disk_blob(station: str, rel: str, kind: str) -> Optional[str]:
    full = os.path.join(station, rel)
    if kind == "submodule":
        code, out, _ = git_code(full, "rev-parse", "HEAD")
        return out.strip() if code == 0 else None
    if not os.path.isfile(full):
        return None
    code, out, _ = git_code(station, "hash-object", "--", rel)
    return out.strip() if code == 0 else None


def build_parser() -> argparse.ArgumentParser:
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--repo", default=None, help="any checkout of the repo (default: cwd)")
    shared.add_argument("--json", action="store_true", help="JSON on stdout (inventory/plan)")
    p = argparse.ArgumentParser(
        description="Merge-prep for all git worktrees. Writes only via cascade (ff-only).",
        parents=[shared],
        epilog="examples:\n"
        "  %(prog)s inventory --json --repo /path/to/checkout\n"
        "  %(prog)s plan --repo /path/to/checkout\n"
        "  %(prog)s cascade MERGE_SHA --repo /path/to/checkout\n"
        "  %(prog)s verify --snapshot snap.json --expect-sha MERGE_SHA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("inventory", parents=[shared], help="list stations, unique commits, dirty files (default)")
    sub.add_parser("plan", parents=[shared], help="print merge order and commands")
    cas = sub.add_parser("cascade", parents=[shared], help="ff-only every station to MERGE_SHA")
    cas.add_argument("sha")
    cas.add_argument("--dry-run", action="store_true")
    ver = sub.add_parser("verify", parents=[shared], help="check MERGE_SHA follow + dirty blobs survived")
    ver.add_argument("--snapshot", required=True, help="JSON from inventory --json")
    ver.add_argument("--expect-sha", default=None)
    return p


def main(argv: list[str]) -> int:
    cmds = {"inventory", "plan", "cascade", "verify"}
    parser = build_parser()
    if argv and argv[0] in {"-h", "--help"}:
        parser.print_help()
        return 0
    if not any(a in cmds for a in argv if not a.startswith("-")):
        argv = ["inventory", *argv]
    args = parser.parse_args(argv)
    repo = discover_repo(args.repo)
    cmd = args.cmd or "inventory"
    if cmd in {"inventory", "plan"}:
        data = collect(repo)
        if args.json:
            json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
        elif cmd == "plan":
            print_plan(data)
        else:
            print_inventory(data)
        return 0
    if cmd == "cascade":
        return cascade(repo, args.sha, args.dry_run)
    if cmd == "verify":
        return verify(repo, args.snapshot, args.expect_sha)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
