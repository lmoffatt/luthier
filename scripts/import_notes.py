#!/usr/bin/env python3
"""Bring written notes into the record, with their dates and hashes.

Two kinds of file in a source folder (`~/Projects/HoTTification` was the case of 2026-10-09):

- `.odt` notes written by Luciano (2022 to 2023). Each is copied as it is and converted to
  Markdown next to it with pandoc; the converted file opens with a frontmatter that says the
  original, its sha256, the creation and modification dates read from the document's own
  metadata (`meta.xml`), the word count and how it was converted. The original is never edited.
- `.md` texts written by a model (the HoTTification manifests of June 2025, from ChatGPT). Each is
  copied as it is; its dates come from the file system, since Markdown has no metadata.

Each output folder gets a `manifest.jsonl`: one line per file with its origin, sha256, dates,
author and the version of this script. Mechanical, no model. Nothing is committed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

VERSION = "import_notes v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_NOTES_OUT = REPO_ROOT / "record" / "Lucianos ideas" / "HoTTification"
DEFAULT_MODEL_OUT = REPO_ROOT / "record" / "IA" / "HoTTification-2025-06"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def odt_meta(path: Path) -> dict:
    """creation and modification dates and the word count, from the document's meta.xml."""
    out = {"created": "", "modified": "", "words": ""}
    try:
        meta = zipfile.ZipFile(path).read("meta.xml").decode("utf-8")
    except (zipfile.BadZipFile, KeyError, OSError):
        return out
    c = re.search(r"<meta:creation-date>([^<]+)", meta)
    d = re.search(r"<dc:date>([^<]+)", meta)
    w = re.search(r'meta:word-count="(\d+)"', meta)
    out["created"] = c.group(1)[:19] if c else ""
    out["modified"] = d.group(1)[:19] if d else ""
    out["words"] = w.group(1) if w else ""
    return out


def pandoc_version() -> str:
    try:
        return subprocess.run(["pandoc", "--version"], capture_output=True, text=True, check=True).stdout.splitlines()[0]
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return "pandoc (version unknown)"


def convert_odt(src: Path, dst_md: Path) -> None:
    subprocess.run(["pandoc", str(src), "-t", "gfm", "--wrap=none", "-o", str(dst_md)], check=True)


def fs_times(path: Path) -> dict:
    st = path.stat()
    return {"modified": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%dT%H:%M:%S")}


def import_notes(src_dir: Path, notes_out: Path, model_out: Path, author_md: str, dry: bool) -> int:
    odts = sorted(src_dir.glob("*.odt"))
    mds = sorted(src_dir.glob("*.md"))
    if not odts and not mds:
        print(f"nothing to import in {src_dir}", file=sys.stderr)
        return 1
    pv = pandoc_version()
    stamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    for out, files, kind in ((notes_out, odts, "odt"), (model_out, mds, "md")):
        if not files:
            continue
        rows = []
        for f in files:
            if kind == "odt":
                m = odt_meta(f)
                date = (m["created"] or fs_times(f)["modified"])[:10]
                stem = f"{date} {f.stem}"
                row = {"file": f"{stem}.md", "original": f.name, "original_sha256": sha256(f), "kind": "note",
                       "author": "Luciano", "created": m["created"], "modified": m["modified"], "words": m["words"],
                       "converted_by": f"{VERSION}; {pv}; gfm", "imported": stamp, "origin": str(f)}
                print(f"{'would convert' if dry else 'convert'}  {f.name} -> {out.name}/{stem}.md  (created {m['created'][:10]})")
                if not dry:
                    out.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(f, out / f.name)
                    tmp = out / f"{stem}.body.md"
                    convert_odt(f, tmp)
                    body = tmp.read_text(encoding="utf-8")
                    tmp.unlink()
                    front = ["---", f"title: \"{f.stem}\"", "author: Luciano", f"original: {f.name}",
                             f"original_sha256: {row['original_sha256']}", f"created: {m['created']}",
                             f"modified: {m['modified']}", f"words: {m['words']}",
                             f"converted_by: {row['converted_by']}", "note: the original is next to this file; this conversion is derived and may be redone",
                             "---", ""]
                    (out / f"{stem}.md").write_text("\n".join(front) + body, encoding="utf-8")
                    row["sha256"] = sha256(out / f"{stem}.md")
            else:
                t = fs_times(f)
                row = {"file": f.name, "original": f.name, "sha256": sha256(f), "kind": "model text",
                       "author": author_md, "modified": t["modified"], "imported": stamp, "origin": str(f),
                       "copied_by": VERSION}
                print(f"{'would copy' if dry else 'copy'}  {f.name} -> {out.name}/  (modified {t['modified'][:10]})")
                if not dry:
                    out.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(f, out / f.name)
            rows.append(row)
        if not dry:
            with (out / "manifest.jsonl").open("w", encoding="utf-8") as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
            print(f"manifest: {out / 'manifest.jsonl'} ({len(rows)} files)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path, help="the folder with the .odt notes and the .md texts")
    ap.add_argument("--notes-out", type=Path, default=DEFAULT_NOTES_OUT, help="where Luciano's notes go")
    ap.add_argument("--model-out", type=Path, default=DEFAULT_MODEL_OUT, help="where the model's texts go")
    ap.add_argument("--author-md", default="model (ChatGPT)", help="author recorded for the .md texts")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    if not args.source.is_dir():
        print(f"ERROR: not a directory: {args.source}", file=sys.stderr)
        return 2
    return import_notes(args.source, args.notes_out, args.model_out, args.author_md, args.dry_run)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
