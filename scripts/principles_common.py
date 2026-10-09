"""What find_principles, match_principles and compare_principles share: the lineages shown to a
model under short labels (l<n>, q<n>), an optional redaction of names, the check of a quote against
its row, and the call that asks again with the errors of a rejected answer."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_ideas  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
ELLIPSIS_RE = re.compile(r"\s*(?:\.\.\.|…|\[\.\.\.\]|\[…\])\s*")
AXES = ("aesthetic", "ethical", "emotive", "conceptual")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def fill(template: str, pairs: list[str]) -> tuple[str, list[str]]:
    """{KEY} filled from KEY=VALUE pairs; returns the text and the fields left unfilled."""
    for kv in pairs:
        k, _, v = kv.partition("=")
        template = template.replace("{" + k + "}", v)
    return template, sorted(set(re.findall(r"\{([a-z_]+)\}", template)))


def redactor(pairs: list[str]):
    """A function that replaces each TERM by its REPLACEMENT (TERM=REPLACEMENT, whole words, any case),
    longest terms first, so that a model cannot read the language's name in what it is shown."""
    subs = []
    for kv in pairs:
        k, _, v = kv.partition("=")
        if k:
            subs.append((re.compile(r"(?<!\w)" + re.escape(k) + r"(?!\w)", re.IGNORECASE), v))
    subs.sort(key=lambda s: -len(s[0].pattern))

    def red(text: str) -> str:
        for pat, v in subs:
            text = pat.sub(v, text)
        return text
    return red


def words(text: str) -> str:
    text = unicodedata.normalize("NFC", str(text)).replace("\\n", " ")
    text = "".join(" " if unicodedata.category(c)[0] in "PS" else c for c in text)
    return " ".join(text.casefold().split())


def quote_in(quote: str, source: str) -> bool:
    hay, pos = words(source), 0
    pieces = [words(p) for p in ELLIPSIS_RE.split(quote) if words(p)]
    if not pieces:
        return False
    for piece in pieces:
        i = hay.find(piece, pos)
        if i < 0:
            return False
        pos = i + len(piece)
    return True


def wrap(text: str, width: int = 100, indent: str = "            ") -> str:
    out, line = [], ""
    for w in str(text).split():
        if line and len(line) + 1 + len(w) > width - len(indent):
            out.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    if line:
        out.append(line)
    return ("\n" + indent).join(out)


def pick_quotes(members: list[dict], n: int) -> list[dict]:
    """Deterministic: the first row, the first of Luciano's or a designer's, corrections and
    rejections, the last."""
    chosen: list[dict] = []

    def add(m):
        if m is not None and m not in chosen and len(chosen) < n:
            chosen.append(m)
    add(members[0])
    add(next((m for m in members if m.get("who") not in ("model", "pasted")), None))
    for m in members:
        if m["relation"] in ("corrects", "rejects"):
            add(m)
    add(members[-1])
    for m in members:
        add(m)
    return sorted(chosen, key=lambda m: (m.get("time_utc", ""), m["id"]))


def labels_for(der: dict[str, dict]) -> dict[str, str]:
    """l<n> -> lineage id, in order of first appearance."""
    order = sorted(der.values(), key=lambda d: (d["first"].get("time_utc", ""), d["id"]))
    return {f"l{i}": d["id"] for i, d in enumerate(order, 1)}


def lineage_blocks(der: dict[str, dict], n_quotes: int, quote_chars: int, red=lambda t: t,
                   qlabels: dict | None = None, qtext: dict | None = None) -> str:
    """The lineages as the model sees them; fills qlabels (q<n> -> row id) and qtext (q<n> -> the
    quote as shown, after redaction), so a quote can be checked against what the model read."""
    qlabels = {} if qlabels is None else qlabels
    qtext = {} if qtext is None else qtext
    out = []
    for lab, lid in labels_for(der).items():
        d = der[lid]
        head = f"scope: {d['scope']} | origin: {red(str(d['origin']))} | first seen: {d['first'].get('time_local', '')[:10]}"
        lines = [f"### {lab} {red(d['id'])}", head, f"statement: {red(d['statement'])}", "quotes:"]
        for m in pick_quotes(d["members"], n_quotes):
            q = f"q{len(qlabels) + 1}"
            qlabels[q] = m["id"]
            qtext[q] = red(m.get("quote", ""))
            lines.append(f"- {q} | {m.get('time_local', '')[:16]} | {red(str(m.get('who')))} | {m['relation']} | "
                         f"\"{link_ideas.clip(qtext[q], quote_chars)}\"")
        out.append("\n".join(lines))
    return "\n\n".join(out)


def ask(cli: str, prompt_text: str, args, expand_check, label: str = "") -> tuple[dict | None, list[dict]]:
    """Call the model; expand_check(raw_json) -> (answer, errors). A rejected answer is asked again
    with its errors, up to args.retries times. Returns the accepted answer (or None) and the attempts."""
    attempts, text, ans = [], prompt_text, None
    model = args.model
    for _ in range(args.retries + 1):
        t0 = time.time()
        try:
            raw = link_ideas.call(cli, text, model, args.effort, args.timeout, args.max_output_tokens,
                                  args.max_thinking_tokens)
        except link_ideas.OutputLimit as exc:
            attempts.append({"error": f"output limit: {exc}", "seconds": round(time.time() - t0)})
            print(f"{label}the answer hit the output token limit; raise it with --max-output-tokens", file=sys.stderr)
            break
        except Exception as exc:
            attempts.append({"error": str(exc)[:500], "seconds": round(time.time() - t0)})
            print(f"{label}call failed: {str(exc)[:200]}", file=sys.stderr)
            continue
        try:
            cand, errors = expand_check(link_ideas.parse_json(raw))
        except (ValueError, json.JSONDecodeError) as exc:
            cand, errors = None, [f"not valid JSON: {exc}"]
        attempts.append({"answer": raw, "answer_sha256": sha256_bytes(raw.encode()), "errors": errors,
                         "seconds": round(time.time() - t0),
                         "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
        if not errors:
            ans = cand
            break
        print(f"{label}answer rejected ({len(errors)} errors): {errors[0][:160]}\n{label}the answer began: "
              f"{raw.strip()[:200]!r}", file=sys.stderr)
        text = (prompt_text + "\n\n## Your previous answer was rejected\n\n" + "\n".join(f"- {e}" for e in errors)
                + "\n\nAnswer again, the whole JSON object.\n")
    return ans, attempts


def common_args(p, default_prompt: Path) -> None:
    p.add_argument("--prompt", type=Path, default=default_prompt)
    p.add_argument("--var", action="append", default=[], metavar="KEY=VALUE", help="fills {KEY} in the prompt")
    p.add_argument("--cli", choices=("auto", "claude", "codex"), default="auto")
    p.add_argument("--model", default=None)
    p.add_argument("--agent", default=None)
    p.add_argument("--effort", choices=("low", "medium", "high", "xhigh", "max"), default="low",
                   help="passed to claude; codex ignores it")
    p.add_argument("--retries", type=int, default=2)
    p.add_argument("--timeout", type=float, default=1800.0)
    p.add_argument("--max-output-tokens", type=int, default=0, help="CLAUDE_CODE_MAX_OUTPUT_TOKENS (0: the CLI's default)")
    p.add_argument("--max-thinking-tokens", type=int, default=0, help="MAX_THINKING_TOKENS (0: the CLI's default)")
    p.add_argument("--force", action="store_true", help="redo a run that exists")
    p.add_argument("--dry-run", action="store_true", help="assemble and measure the input; call no model")
    p.add_argument("--show-input", type=Path, default=None, help="write the assembled prompt here and stop")


def resolve(args) -> tuple[str, str, str]:
    cli = link_ideas.resolve_cli(args.cli)
    model = args.model or ("gpt-5" if cli == "codex" else "opus")
    agent = args.agent or ("codex" if cli == "codex" else "claude-code")
    args.model = model
    return cli, model, agent
