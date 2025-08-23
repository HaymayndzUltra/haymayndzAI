#!/usr/bin/env python3
from __future__ import annotations
import os, sys, subprocess, time, re
from pathlib import Path
from typing import List, Tuple, Optional

DAYS = 3
NOW = time.time()
SINCE_EPOCH = NOW - (DAYS * 24 * 60 * 60)
SINCE_ISO = time.strftime("%Y-%m-%d", time.localtime(SINCE_EPOCH))

IGNORE_DIRS = {".git", ".cursor", "node_modules", "venv", ".venv", "__pycache__", "memory-bank/logs"}

LABNOTES_REL = Path("frameworks/fwk-001-cursor-rules/DOCS/Labnotes.md")
CHANGES_DIR_REL = Path("frameworks/fwk-001-cursor-rules/DOCS/changes")
REPORTS_DIR_REL = Path("frameworks/fwk-001-cursor-rules/DOCS/reports")

def discover_repo_root() -> Path:
    env = os.getenv("REPO_ROOT")
    if env:
        try:
            return Path(env).resolve()
        except Exception:
            pass
    ws = Path("/workspace")
    if ws.exists():
        return ws.resolve()
    return Path.cwd().resolve()

def is_git_repo(root: Path) -> bool:
    return (root / ".git").is_dir()

def run_git_changes(root: Path) -> str:
    if not is_git_repo(root):
        return "(not a git repository)\n"
    cmd = [
        "git", "log", f"--since={SINCE_ISO}",
        "--pretty=format:commit %H %ad %an %s", "--date=iso", "--name-status"
    ]
    try:
        out = subprocess.check_output(cmd, cwd=str(root), stderr=subprocess.STDOUT, text=True)
        return out.strip() + "\n"
    except subprocess.CalledProcessError as e:
        return f"(git log failed)\n{e.output}\n"

def list_fs_changes(root: Path) -> List[Tuple[str, float, int]]:
    changes: List[Tuple[str, float, int]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).resolve().relative_to(root)
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        if any(str(rel_dir).startswith(ign) for ign in IGNORE_DIRS):
            continue
        for fn in filenames:
            p = Path(dirpath) / fn
            try:
                st = p.stat()
            except FileNotFoundError:
                continue
            if st.st_mtime >= SINCE_EPOCH:
                rel = p.resolve().relative_to(root).as_posix()
                changes.append((rel, st.st_mtime, st.st_size))
    changes.sort(key=lambda x: x[1], reverse=True)
    return changes

def parse_labnotes_blocks(root: Path) -> List[Tuple[str, str]]:
    path = root / LABNOTES_REL
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    blocks: List[Tuple[str, str]] = []
    cur_title: Optional[str] = None
    cur_lines: List[str] = []
    date_re = re.compile(r"^###\s+(\d{4}-\d{2}-\d{2})")
    for line in text:
        m = date_re.match(line)
        if m:
            if cur_title is not None and cur_lines:
                blocks.append((cur_title, "\n".join(cur_lines)))
            cur_title = line.strip()
            cur_lines = []
        else:
            if cur_title is not None:
                cur_lines.append(line)
    if cur_title is not None and cur_lines:
        blocks.append((cur_title, "\n".join(cur_lines)))
    recent: List[Tuple[str, str]] = []
    for title, body in blocks[::-1]:
        dm = re.search(r"(\d{4}-\d{2}-\d{2})", title)
        if not dm:
            continue
        try:
            ts = time.mktime(time.strptime(dm.group(1), "%Y-%m-%d"))
        except Exception:
            continue
        if ts >= SINCE_EPOCH:
            recent.append((title, body))
    return recent[::-1]

def extract_paths_from_labnotes(body: str) -> List[str]:
    paths = []
    for line in body.splitlines():
        m = re.search(r"^-\s*Path:\s*([^\(]+)\(abs:\s*([^\)]+)\)", line.strip())
        if m:
            rel = m.group(1).strip()
            paths.append(rel)
    return paths

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def main() -> int:
    root = discover_repo_root()
    git_out = run_git_changes(root)
    fs_changes = list_fs_changes(root)
    lab_blocks = parse_labnotes_blocks(root)

    git_doc = [
        f"# Git Changes (since {SINCE_ISO})",
        "",
        "```",
        git_out.rstrip(),
        "```",
        "",
    ]
    write_text(root / CHANGES_DIR_REL / "git_changes.md", "\n".join(git_doc))

    fs_doc_lines = [f"# Filesystem Changes (since {SINCE_ISO})", "", "| Path | mtime | size |", "| --- | --- | ---:|"]
    for rel, mt, sz in fs_changes[:1000]:
        fs_doc_lines.append(f"| {rel} | {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mt))} | {sz} |")
    write_text(root / CHANGES_DIR_REL / "fs_changes.md", "\n".join(fs_doc_lines))

    ln_doc_lines = [f"# Labnotes Changes (since {SINCE_ISO})", ""]
    lab_paths: List[str] = []
    if lab_blocks:
        for title, body in lab_blocks:
            ln_doc_lines.append(f"## {title}")
            lab_paths.extend(extract_paths_from_labnotes(body))
            ln_doc_lines.append("```markdown")
            ln_doc_lines.append(body.strip())
            ln_doc_lines.append("```")
            ln_doc_lines.append("")
    else:
        ln_doc_lines.append("(no labnotes entries in window)")
    write_text(root / CHANGES_DIR_REL / "labnotes_changes.md", "\n".join(ln_doc_lines))

    git_files: set[str] = set()
    if git_out and "(git log failed)" not in git_out and "(not a git repository)" not in git_out:
        for line in git_out.splitlines():
            if line and (line[0] in {"A","M","D","R","C","T"}) and "\t" in line:
                parts = line.split("\t")
                if len(parts) >= 2:
                    git_files.add(parts[-1].strip())
    fs_files = {p for (p, _, _) in fs_changes}
    ln_files = set(lab_paths)

    only_fs = sorted(fs_files - git_files)
    only_git = sorted(git_files - fs_files)
    only_ln = sorted(ln_files - (fs_files | git_files))

    disc_lines = ["# Discrepancies", "", f"Window since: {SINCE_ISO}", "", "## In FS only (not in git)"]
    disc_lines += [f"- {p}" for p in only_fs[:1000]] or ["- (none)"]
    disc_lines += ["", "## In Git only (not in fs)"]
    disc_lines += [f"- {p}" for p in only_git[:1000]] or ["- (none)"]
    disc_lines += ["", "## In Labnotes only (not in fs/git)"]
    disc_lines += [f"- {p}" for p in only_ln[:1000]] or ["- (none)"]
    write_text(root / CHANGES_DIR_REL / "discrepancies.md", "\n".join(disc_lines))

    latest = [
        f"# Latest Current (last {DAYS} days)",
        "",
        f"- Time window start: {SINCE_ISO}",
        f"- Repo root: {root}",
        "",
        "## Sources",
        f"- Git: frameworks/fwk-001-cursor-rules/DOCS/changes/git_changes.md",
        f"- Filesystem: frameworks/fwk-001-cursor-rules/DOCS/changes/fs_changes.md",
        f"- Labnotes: frameworks/fwk-001-cursor-rules/DOCS/changes/labnotes_changes.md",
        f"- Discrepancies: frameworks/fwk-001-cursor-rules/DOCS/changes/discrepancies.md",
        "",
        "## Summary Snapshot",
        f"- Git commits found: {'0' if git_out.startswith('(') else str(git_out.count('commit '))}",
        f"- Files touched (fs): {len(fs_files)}",
        f"- Labnotes blocks: {len(lab_blocks)}",
    ]
    write_text(root / REPORTS_DIR_REL / "Latest_Current.md", "\n".join(latest))

    print("Reports written:")
    print(f"- {CHANGES_DIR_REL / 'git_changes.md'}")
    print(f"- {CHANGES_DIR_REL / 'fs_changes.md'}")
    print(f"- {CHANGES_DIR_REL / 'labnotes_changes.md'}")
    print(f"- {CHANGES_DIR_REL / 'discrepancies.md'}")
    print(f"- {REPORTS_DIR_REL / 'Latest_Current.md'}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
