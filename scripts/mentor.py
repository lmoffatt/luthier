#!/usr/bin/env python3
"""Invocar al mentor sobre el ecosistema de ideas de diseño de Luthier (modo mentor).

Es una invocación explícita (conforme a PRINCIPIOS.md): toma el archivo
consolidado de ideas, lo pasa al prompt `mentor_disenio_v1` vía `claude` (o
`codex`) y produce `_mentor_<prompt_id>_<agente>_<modelo>.md`.

El mentor produce fricción sobre el *proceso* de diseño; no diseña el lenguaje.
El frontmatter del output lo construye el script (no el modelo).
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
DEFAULT_IDEAS_DIR = REPO_ROOT / "record" / "ideas"
DEFAULT_PROMPT = REPO_ROOT / "prompts" / "mentor_disenio_v1.md"
PLACEHOLDER = "<<<INPUT>>>"
MODO = "mentor"

DEFAULT_CLAUDE_MODEL = "opus"
DEFAULT_CODEX_MODEL = "gpt-5.4"

FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
FENCE_OPEN_RE = re.compile(r"\A\s*```[a-zA-Z]*\s*\n")
FENCE_CLOSE_RE = re.compile(r"\n```\s*\Z")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", type=Path, nargs="?", default=None,
                   help="Archivo consolidado de ideas. Default: el _luthier_ideas_*.md más reciente en record/ideas.")
    p.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT,
                   help=f"Archivo del prompt (debe contener {PLACEHOLDER}).")
    p.add_argument("--output", type=Path, default=None,
                   help="Archivo de salida. Default: record/ideas/_mentor_<tag>.md")
    p.add_argument("--cli", choices=("auto", "claude", "codex"), default="auto",
                   help="CLI a usar. 'auto' prioriza claude y usa codex de fallback.")
    p.add_argument("--model", default=None, help="Modelo. Default según el CLI.")
    p.add_argument("--agente", default=None, help="Nombre del agente en el frontmatter. Default según el CLI.")
    p.add_argument("--force", action="store_true", help="Regenerar aunque exista el output.")
    p.add_argument("--dry-run", action="store_true", help="Reportar input/salida sin llamar al modelo.")
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
    return re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-") or "x"


def _pick_input(ideas_dir: Path) -> Path | None:
    # Los consolidados archivados a mano llevan sufijo de fecha
    # (_luthier_ideas_..._YYYY-MM-DD.md); no son candidatos válidos.
    candidates = [p for p in ideas_dir.glob("_luthier_ideas_*.md")
                  if p.is_file() and not re.search(r"\d{4}-\d{2}-\d{2}$", p.stem)]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


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

    if not args.prompt.is_file():
        print(f"ERROR: prompt no encontrado: {args.prompt}", file=sys.stderr)
        return 2
    prompt_template = args.prompt.read_text(encoding="utf-8")
    if PLACEHOLDER not in prompt_template:
        print(f"ERROR: el prompt no contiene {PLACEHOLDER}", file=sys.stderr)
        return 2

    input_path = args.input or _pick_input(DEFAULT_IDEAS_DIR)
    if input_path is None:
        print("ERROR: no encontré ningún _luthier_ideas_*.md. Corré consolidate_ideas.py primero "
              "o pasá el archivo como argumento.", file=sys.stderr)
        return 1
    if not input_path.is_file():
        print(f"ERROR: input no encontrado: {input_path}", file=sys.stderr)
        return 2

    try:
        cli = _resolve_cli(args.cli)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    modelo = args.model or (DEFAULT_CLAUDE_MODEL if cli == "claude" else DEFAULT_CODEX_MODEL)
    agente = args.agente or ("claude-code" if cli == "claude" else "codex")
    prompt_id = args.prompt.stem

    output = args.output or (DEFAULT_IDEAS_DIR / f"_mentor_{prompt_id}_{_slug(agente)}_{_slug(modelo)}.md")

    print(f"Input: {input_path.name}")
    print(f"CLI: {cli} | modelo: {modelo} | agente: {agente} | prompt: {prompt_id}")
    print(f"Salida: {output}")
    if output.exists() and output.stat().st_size > 0 and not args.force and not args.dry_run:
        print("El output ya existe (usá --force para regenerar).")
        return 0
    if args.dry_run:
        print("[dry-run] no se llama al modelo.")
        return 0

    content = input_path.read_text(encoding="utf-8")
    user_message = prompt_template.replace(PLACEHOLDER, content)
    try:
        if cli == "claude":
            raw = _run_claude(user_message, modelo, args.timeout)
        else:
            raw = _run_codex(user_message, modelo, args.timeout, REPO_ROOT)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR al invocar el modelo: {exc}", file=sys.stderr)
        return 1

    body = _clean_body(raw)
    frontmatter = "\n".join([
        "---",
        f"fuente: {input_path.name}",
        f"generado_por: {prompt_id}",
        f"modo: {MODO}",
        f"agente: {agente}",
        f"modelo: {modelo}",
        "---",
    ])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f"{frontmatter}\n\n{body}\n", encoding="utf-8")
    print(f"-> {output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
