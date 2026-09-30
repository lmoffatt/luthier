#!/usr/bin/env python3
"""Consolidar las ideas de diseño extraídas en el ecosistema de ideas de Luthier.

Junta todos los `*_ideas.md` producidos por `extract_ideas.py`, los pasa como un
único corpus al prompt `consolidate_ideas_v1` (vía `claude` o `codex`) y produce
un único archivo `_luthier_ideas_<prompt_id>_<agente>_<modelo>.md`.

El frontmatter del output se construye de forma determinista en Python (nº de
fuentes, nº de ecosistemas, nº de ideas, agente, modelo, prompt, modo), pisando
lo que genere el modelo.
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
DEFAULT_IDEAS_DIR = REPO_ROOT / "docs" / "ideas"
DEFAULT_PROMPT = REPO_ROOT / "prompts" / "consolidate_ideas_v1.md"
PLACEHOLDER = "<<<INPUT>>>"
MODO = "editor"

DEFAULT_CLAUDE_MODEL = "sonnet"
DEFAULT_CODEX_MODEL = "gpt-5.4"

AUDIO_RE = re.compile(r"^\s*audio:\s*(.+?)\s*$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
FENCE_OPEN_RE = re.compile(r"\A\s*```[a-zA-Z]*\s*\n")
FENCE_CLOSE_RE = re.compile(r"\n```\s*\Z")
ECO_RE = re.compile(r"^## ", re.MULTILINE)
IDEA_RE = re.compile(r"^### ", re.MULTILINE)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ideas_dir", type=Path, nargs="?", default=DEFAULT_IDEAS_DIR,
                   help=f"Directorio con los *_ideas.md (default: {DEFAULT_IDEAS_DIR}).")
    p.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT,
                   help=f"Archivo del prompt (debe contener {PLACEHOLDER}).")
    p.add_argument("--output", type=Path, default=None,
                   help="Archivo de salida. Default: <ideas_dir>/_luthier_ideas_<tag>.md")
    p.add_argument("--cli", choices=("auto", "claude", "codex"), default="auto",
                   help="CLI a usar. 'auto' prioriza claude y usa codex de fallback.")
    p.add_argument("--model", default=None, help="Modelo. Default según el CLI.")
    p.add_argument("--agente", default=None, help="Nombre del agente en el frontmatter. Default según el CLI.")
    p.add_argument("--source-agente", default=None,
                   help="Tomar solo extracciones de este agente (p. ej. claude-code).")
    p.add_argument("--source-model", default=None,
                   help="Tomar solo extracciones de este modelo (p. ej. opus). Evita mezclar modelos.")
    p.add_argument("--aggregate-output", type=Path, default=None,
                   help="(debug) Guardar el bundle ensamblado en este archivo.")
    p.add_argument("--force", action="store_true", help="Regenerar aunque exista el output.")
    p.add_argument("--dry-run", action="store_true", help="Ensamblar y reportar sin llamar al modelo.")
    p.add_argument("--timeout", type=float, default=900.0, help="Timeout de la llamada (segundos).")
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
    text = re.sub(r"[^a-z0-9]+", "-", text.strip().lower())
    return text.strip("-") or "x"


def _collect(ideas_dir: Path, agente: str | None = None, model: str | None = None) -> list[Path]:
    files = []
    for p in ideas_dir.glob("*_ideas.md"):
        if not p.is_file() or p.name.startswith("_"):
            continue
        if model and not p.name.endswith(f"_{_slug(model)}_ideas.md"):
            continue
        if agente and f"_{_slug(agente)}_" not in p.name:
            continue
        files.append(p)
    return sorted(files, key=lambda p: p.name.lower())


def _bundle(files: list[Path]) -> str:
    blocks = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        am = AUDIO_RE.search(text)
        label = am.group(1).strip() if am else f.stem
        blocks.append(f"===== ARCHIVO: {label} =====\n{text.strip()}")
    return "\n\n".join(blocks)


def _run_claude(prompt_text: str, model: str, timeout: float) -> str:
    # Una sola llamada sincrónica que puede tardar varios minutos: avisamos
    # cada 60 s para que la espera no parezca un cuelgue.
    proc = subprocess.Popen(
        ["claude", "-p", "--model", model, "--output-format", "text",
         "--no-session-persistence", "--tools", ""],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True,
    )
    start = time.monotonic()
    pending_input = prompt_text
    while True:
        try:
            out, err = proc.communicate(input=pending_input, timeout=60.0)
            break
        except subprocess.TimeoutExpired:
            pending_input = None
            elapsed = time.monotonic() - start
            if elapsed >= timeout:
                proc.kill()
                proc.communicate()
                raise RuntimeError(f"timeout tras {int(elapsed)} s (subilo con --timeout)")
            print(f"  ... {model} sigue trabajando ({int(elapsed)} s)", flush=True)
    if proc.returncode != 0:
        raise RuntimeError((err or out).strip() or "claude falló")
    return out


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
    body = FRONTMATTER_RE.sub("", body)
    body = FENCE_OPEN_RE.sub("", body)
    body = FENCE_CLOSE_RE.sub("", body)
    return body.strip()


def main(argv: list[str]) -> int:
    args = _parse_args(argv)

    if not args.ideas_dir.is_dir():
        print(f"ERROR: no es un directorio: {args.ideas_dir}", file=sys.stderr)
        return 2
    if not args.prompt.is_file():
        print(f"ERROR: prompt no encontrado: {args.prompt}", file=sys.stderr)
        return 2
    prompt_template = args.prompt.read_text(encoding="utf-8")
    if PLACEHOLDER not in prompt_template:
        print(f"ERROR: el prompt no contiene {PLACEHOLDER}", file=sys.stderr)
        return 2

    files = _collect(args.ideas_dir, args.source_agente, args.source_model)
    if not files:
        print(f"No hay *_ideas.md en {args.ideas_dir} (con los filtros dados). "
              f"Corré extract_ideas.py primero.", file=sys.stderr)
        return 1

    bundle = _bundle(files)
    approx_tokens = len(bundle) // 4
    print(f"Fuentes: {len(files)} | bundle: {len(bundle)} chars (~{approx_tokens} tokens)")

    if args.aggregate_output:
        args.aggregate_output.parent.mkdir(parents=True, exist_ok=True)
        args.aggregate_output.write_text(bundle, encoding="utf-8")
        print(f"Bundle guardado en {args.aggregate_output}")

    try:
        cli = _resolve_cli(args.cli)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    modelo = args.model or (DEFAULT_CLAUDE_MODEL if cli == "claude" else DEFAULT_CODEX_MODEL)
    agente = args.agente or ("claude-code" if cli == "claude" else "codex")
    prompt_id = args.prompt.stem

    output = args.output or (args.ideas_dir / f"_luthier_ideas_{prompt_id}_{_slug(agente)}_{_slug(modelo)}.md")

    print(f"CLI: {cli} | modelo: {modelo} | agente: {agente} | prompt: {prompt_id}")
    print(f"Salida: {output}")
    if output.exists() and output.stat().st_size > 0 and not args.force and not args.dry_run:
        print("El output ya existe (usá --force para regenerar).")
        return 0
    if args.dry_run:
        for f in files:
            print(f"  [dry] {f.name}")
        return 0

    user_message = prompt_template.replace(PLACEHOLDER, bundle)
    try:
        if cli == "claude":
            raw = _run_claude(user_message, modelo, args.timeout)
        else:
            raw = _run_codex(user_message, modelo, args.timeout, REPO_ROOT)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR al invocar el modelo: {exc}", file=sys.stderr)
        return 1

    body = _clean_body(raw)
    n_eco = len(ECO_RE.findall(body))
    n_ideas = len(IDEA_RE.findall(body))
    frontmatter = "\n".join([
        "---",
        f"fuentes: {len(files)}",
        f"ecosistemas: {n_eco}",
        f"ideas: {n_ideas}",
        f"generado_por: {prompt_id}",
        f"modo: {MODO}",
        f"agente: {agente}",
        f"modelo: {modelo}",
        "---",
    ])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f"{frontmatter}\n\n{body}\n", encoding="utf-8")
    print(f"-> {output.name} ({n_eco} ecosistemas, {n_ideas} ideas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
