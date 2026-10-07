#!/usr/bin/env python3
"""Extraer las ideas de diseño de cada transcripción de Luthier (modo editor).

Por cada transcripción `.md` del directorio de entrada, invoca el prompt
`extract_ideas_v1` vía el CLI de `claude` (o `codex`) y produce un archivo
hermano `<stem>_<prompt_id>_<agente>_<modelo>_ideas.md` en el directorio de
salida.

El frontmatter del output se construye de forma determinista en Python
(audio, fecha, duración, nº de ideas, agente, modelo, prompt, modo), pisando
cualquier frontmatter que genere el modelo. El modelo solo produce el cuerpo.

Es idempotente: salta las transcripciones que ya tienen un output no vacío
(salvo --force).
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "record" / "audios"
DEFAULT_OUTPUT = REPO_ROOT / "record" / "ideas"
DEFAULT_PROMPT = REPO_ROOT / "prompts" / "extract_ideas_v1.md"
PLACEHOLDER = "<<<TRANSCRIPCION>>>"
MODO = "editor"

DEFAULT_CLAUDE_MODEL = "sonnet"
DEFAULT_CODEX_MODEL = "gpt-5.4-mini"

DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
ARCHIVO_RE = re.compile(r"^\s*\*\*Archivo:\*\*\s*(.+?)\s*$", re.MULTILINE)
DURACION_RE = re.compile(r"^\s*\*\*Duraci[óo]n:\*\*\s*(.+?)\s*$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
FENCE_OPEN_RE = re.compile(r"\A\s*```[a-zA-Z]*\s*\n")
FENCE_CLOSE_RE = re.compile(r"\n```\s*\Z")
IDEA_HEADING_RE = re.compile(r"^###\s+\S", re.MULTILINE)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("directory", type=Path, nargs="?", default=DEFAULT_INPUT,
                   help=f"Directorio con transcripciones .md (default: {DEFAULT_INPUT}).")
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT,
                   help=f"Directorio de salida (default: {DEFAULT_OUTPUT}).")
    p.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT,
                   help=f"Archivo del prompt (debe contener {PLACEHOLDER}).")
    p.add_argument("--cli", choices=("auto", "claude", "codex"), default="auto",
                   help="CLI a usar. 'auto' prioriza claude y usa codex de fallback.")
    p.add_argument("--model", default=None, help="Modelo. Default según el CLI.")
    p.add_argument("--agente", default=None, help="Nombre del agente en el frontmatter. Default según el CLI.")
    p.add_argument("--force", action="store_true", help="Regenerar aunque exista el output.")
    p.add_argument("--dry-run", action="store_true", help="Listar sin llamar al modelo.")
    p.add_argument("--sleep", type=float, default=0.0, help="Pausa entre llamadas (segundos).")
    p.add_argument("--timeout", type=float, default=300.0, help="Timeout por llamada (segundos).")
    return p.parse_args(argv)


def _resolve_cli(choice: str) -> str:
    if choice == "claude":
        if shutil.which("claude") is None:
            raise RuntimeError("claude no está en el PATH")
        return "claude"
    if choice == "codex":
        if shutil.which("codex") is None:
            raise RuntimeError("codex no está en el PATH")
        return "codex"
    if shutil.which("claude"):
        return "claude"
    if shutil.which("codex"):
        return "codex"
    raise RuntimeError("ni claude ni codex están en el PATH")


def _slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "x"


def _run_claude(prompt_text: str, model: str, timeout: float) -> str:
    proc = subprocess.run(
        ["claude", "-p", "--model", model, "--output-format", "text",
         "--no-session-persistence", "--tools", ""],
        input=prompt_text, capture_output=True, text=True, timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or "claude falló")
    return proc.stdout


def _run_codex(prompt_text: str, model: str, timeout: float, workdir: Path) -> str:
    with tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        proc = subprocess.run(
            ["codex", "exec", "--skip-git-repo-check", "--color", "never",
             "--sandbox", "read-only", "-C", str(workdir),
             "--output-last-message", str(tmp_path), "-m", model, "-"],
            input=prompt_text, capture_output=True, text=True, timeout=timeout,
        )
        if proc.returncode != 0:
            raise RuntimeError((proc.stderr or proc.stdout).strip() or "codex falló")
        return tmp_path.read_text(encoding="utf-8")
    finally:
        tmp_path.unlink(missing_ok=True)


def _clean_body(raw: str) -> str:
    body = raw.strip()
    body = FRONTMATTER_RE.sub("", body)          # descartar frontmatter del modelo
    body = FENCE_OPEN_RE.sub("", body)
    body = FENCE_CLOSE_RE.sub("", body)
    return body.strip()


def _extract_meta(transcription: str, stem: str) -> tuple[str, str, str]:
    am = ARCHIVO_RE.search(transcription)
    audio = am.group(1).strip() if am else f"{stem}.mp3"
    dm = DURACION_RE.search(transcription)
    duracion = dm.group(1).strip() if dm else ""
    fm = DATE_RE.search(stem)
    fecha = fm.group(1) if fm else ""
    return audio, fecha, duracion


def _build_frontmatter(*, audio: str, fecha: str, duracion: str, n_ideas: int,
                       prompt_id: str, agente: str, modelo: str) -> str:
    lines = [
        "---",
        f"audio: {audio}",
        f"fecha: {fecha}",
        f"duracion: {duracion}",
        f"ideas: {n_ideas}",
        f"generado_por: {prompt_id}",
        f"modo: {MODO}",
        f"agente: {agente}",
        f"modelo: {modelo}",
        "---",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    args = _parse_args(argv)

    if not args.directory.is_dir():
        print(f"ERROR: no es un directorio: {args.directory}", file=sys.stderr)
        return 2
    if not args.prompt.is_file():
        print(f"ERROR: prompt no encontrado: {args.prompt}", file=sys.stderr)
        return 2
    prompt_template = args.prompt.read_text(encoding="utf-8")
    if PLACEHOLDER not in prompt_template:
        print(f"ERROR: el prompt no contiene {PLACEHOLDER}", file=sys.stderr)
        return 2

    try:
        cli = _resolve_cli(args.cli)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    modelo = args.model or (DEFAULT_CLAUDE_MODEL if cli == "claude" else DEFAULT_CODEX_MODEL)
    agente = args.agente or ("claude-code" if cli == "claude" else "codex")
    prompt_id = args.prompt.stem
    tag = f"{prompt_id}_{_slug(agente)}_{_slug(modelo)}_ideas"

    transcripts = sorted(p for p in args.directory.glob("*.md") if p.is_file())
    if not transcripts:
        print(f"No hay transcripciones .md en {args.directory}", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)
    jobs = []
    skipped = 0
    for t in transcripts:
        out = args.output_dir / f"{t.stem}_{tag}.md"
        if out.exists() and out.stat().st_size > 0 and not args.force:
            skipped += 1
            continue
        jobs.append((t, out))

    print(f"Transcripciones: {len(transcripts)} | ya hechas: {skipped} | pendientes: {len(jobs)}")
    print(f"CLI: {cli} | modelo: {modelo} | agente: {agente} | prompt: {prompt_id}")
    if not jobs:
        print("Nada que hacer.")
        return 0
    if args.dry_run:
        for i, (t, out) in enumerate(jobs, 1):
            print(f"[dry {i:02d}/{len(jobs):02d}] {t.name} -> {out.name}")
        return 0

    generated, failed = 0, []
    for i, (t, out) in enumerate(jobs, 1):
        try:
            transcription = t.read_text(encoding="utf-8")
            user_message = prompt_template.replace(PLACEHOLDER, transcription)
            print(f"[{i:02d}/{len(jobs):02d}] {t.name}", flush=True)
            if cli == "claude":
                raw = _run_claude(user_message, modelo, args.timeout)
            else:
                raw = _run_codex(user_message, modelo, args.timeout, REPO_ROOT)
            body = _clean_body(raw)
            n_ideas = len(IDEA_HEADING_RE.findall(body))
            audio, fecha, duracion = _extract_meta(transcription, t.stem)
            frontmatter = _build_frontmatter(
                audio=audio, fecha=fecha, duracion=duracion, n_ideas=n_ideas,
                prompt_id=prompt_id, agente=agente, modelo=modelo,
            )
            out.write_text(f"{frontmatter}\n\n{body}\n", encoding="utf-8")
            generated += 1
            print(f"  -> {out.name} ({n_ideas} ideas)", flush=True)
            if args.sleep:
                time.sleep(args.sleep)
        except Exception as exc:  # noqa: BLE001
            failed.append((t, str(exc)))
            print(f"  -> FALLÓ {t.name}: {exc}", file=sys.stderr, flush=True)

    print(f"\nResumen: generados {generated} | fallidos {len(failed)}")
    for t, reason in failed:
        print(f"  - {t.name}: {reason}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
