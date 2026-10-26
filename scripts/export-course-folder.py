#!/usr/bin/env python3
"""Export current course artifacts, with ownership-aware removal of stale PDFs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

REPO = Path(__file__).resolve().parents[1]
MANIFEST = ".fusion-skript-export.json"


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_shares(dest):
    sync = Path.home() / "Nextcloud"
    if not dest.is_relative_to(sync.resolve()):
        return []
    # List all so that parent-folder and nested shares are included.
    result = subprocess.run(["helpy", "--json", "nextcloud", "share_list", "--public_only"],
                            capture_output=True, text=True, check=True)
    shares = json.loads(result.stdout)["shares"]
    remote = "/" + dest.relative_to(sync.resolve()).as_posix()
    return [s for s in shares if s["path"] == "/" or remote == s["path"]
            or remote.startswith(s["path"].rstrip("/") + "/")
            or s["path"].startswith(remote + "/")]


def safe_target(dest, relative):
    path = dest / relative
    if Path(relative).is_absolute() or not path.resolve().is_relative_to(dest):
        raise ValueError("Unsafe export manifest path: " + relative)
    if path.is_symlink():
        raise ValueError("Refusing symlink export target: " + relative)
    return path


def export(repo, site, dest):
    """Stage inputs first, then copy and record only files we wrote."""
    wanted = {}
    decks = sorted((site / "slides").glob("*.pdf"))
    if (site / "present/decks.json").is_file():
        active = {d["stem"] + ".pdf" for d in
                  json.loads((site / "present/decks.json").read_text())["decks"]}
        decks = [p for p in decks if p.name in active]
    if not decks:
        raise ValueError("No eligible deck PDFs; build the site first")
    wanted.update({"slides/" + p.name: p for p in decks})
    figures = repo / "derivations/build/fig"
    wanted.update({"figures/" + p.relative_to(figures).as_posix(): p
                   for p in figures.rglob("*") if p.is_file()
                   and p.suffix.lower() in {".svg", ".pdf", ".png"}})
    derivations = repo / "derivations"
    wanted.update({"derivations/" + p.relative_to(derivations).as_posix(): p
                   for p in derivations.rglob("*") if p.is_file()
                   and "build" not in p.relative_to(derivations).parts
                   and "__pycache__" not in p.parts
                   and (p.suffix in {".py", ".md", ".typ", ".toml", ".json"}
                        or p.name in {"Makefile", "requirements.txt"})})
    for name in ("LICENSE", "LICENSE-CONTENT.md"):
        wanted["derivations/" + name] = repo / name
    # Animations: the registered MP4 revisions staged by prepare-media.py, under
    # the file names their stream URLs expect, and the scene sources with data.
    registry = repo / "media/animations.json"
    register = json.loads(registry.read_text())["animations"] if registry.is_file() else {}
    if register:
        wanted["animations/animations.json"] = registry
    for slug, record in register.items():
        video = site / "media" / (slug + ".mp4")
        if video.is_file() and checksum(video) != record["mp4_sha256"]:
            raise ValueError("Staged animation is not the registered revision: " + slug)
        stem = Path(record["stream_url"].split("?")[0]).stem
        wanted["animations/" + stem + ".mp4"] = video
        wanted["animations/" + stem + ".png"] = repo / record["poster"]
    animations = repo / "animations"
    if register:
        wanted.update({"animation-sources/" + p.relative_to(animations).as_posix(): p
                       for p in animations.rglob("*") if p.is_file()
                       and "__pycache__" not in p.parts})
    for source in wanted.values():
        if not source.is_file():
            raise ValueError("Missing export input: " + str(source))
    dest.mkdir(parents=True, exist_ok=True)
    manifest_path = safe_target(dest, MANIFEST)
    old = json.loads(manifest_path.read_text())["files"] if manifest_path.exists() else {}
    for relative in old:
        safe_target(dest, relative)
    owned = dict(old)
    written, removed, preserved = [], [], []
    with tempfile.TemporaryDirectory(prefix="fusion-export-") as tmp:
        staging = Path(tmp)
        for relative, source in wanted.items():
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            safe_target(dest, relative)
        # Only previously exported, unchanged files are eligible for removal.
        for relative, previous_hash in old.items():
            stale = relative not in wanted
            if not stale:
                continue
            target = safe_target(dest, relative)
            if target.exists() and checksum(target) != previous_hash:
                preserved.append(relative)
                continue
            if target.is_file():
                target.unlink()
                removed.append(relative)
            owned.pop(relative, None)
        for relative in wanted:
            source = staging / relative
            target = safe_target(dest, relative)
            new_hash = checksum(source)
            if not target.exists() or checksum(target) != new_hash:
                target.parent.mkdir(parents=True, exist_ok=True)
                temp = target.with_name(target.name + ".fusion-export.tmp")
                # Never follow a user-supplied temporary-file symlink.
                with temp.open("xb") as out, source.open("rb") as inp:
                    shutil.copyfileobj(inp, out)
                os.replace(temp, target)
                written.append(relative)
            owned[relative] = new_hash
        data = {"version": 1, "files": owned}
        temp = manifest_path.with_name(MANIFEST + ".tmp")
        with temp.open("x") as out:
            json.dump(data, out, indent=2, sort_keys=True)
            out.write("\n")
        os.replace(temp, manifest_path)
    print(json.dumps({"target": str(dest), "profile": "full",
                      "written": written, "current": list(wanted), "removed": removed,
                      "preserved_modified": preserved}, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dest", type=Path, nargs="?", default=Path.home() / "Nextcloud/lv/fusion/2026")
    args = p.parse_args()
    dest = args.dest.resolve()
    shares = public_shares(dest)  # Failure stops the export, never assumes privacy.
    print("Public shares covering export: " + ", ".join(s["url"] for s in shares))
    site = Path(os.environ.get("SITE_DIR", REPO / "public")).resolve()
    export(REPO, site, dest)


if __name__ == "__main__":
    main()
