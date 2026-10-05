"""Certificates: what was tested, over which code.

A certificate entry carries a hash of the definition's dependency cone (the
definition and everything it refers to, rendered with the module prefix
removed). When a file is imported, an entry is trusted only if its hash still
matches; otherwise the obligation is pending again.
"""
from __future__ import annotations
import hashlib
import json
import os
from dataclasses import asdict

from .syntax import *
from .subst import map_names, alpha_normalize
from .pretty import pp
from .evaluator import Env


def names_in(t: Term) -> set:
    acc = set()

    def f(n):
        acc.add(n)
        return n
    map_names(t, f)
    return acc


def cone(env: Env, qname: str) -> list:
    """All global names the definition depends on, itself included, sorted."""
    seen = set()
    todo = [qname]
    while todo:
        n = todo.pop()
        if n in seen:
            continue
        if n in env.cons:
            n = env.cons[n][0]        # a constructor stands for its data type
            if n in seen:
                continue
        seen.add(n)
        d = env.defs.get(n)
        if d is None:
            continue
        refs = set()
        if d.type is not None:
            refs |= names_in(d.type)
        if d.data is not None:
            for c in d.data.constructors:
                refs |= names_in(c.type)
        elif d.body is not None and not isinstance(d.body, (Extern, Primitive, Axiom)):
            refs |= names_in(d.body)
        for r in refs:
            if r in env.defs or r in env.cons:
                todo.append(r)
    return sorted(seen)


def _strip(prefix: str):
    head = prefix + "." if prefix else None

    def f(name: str) -> str:
        if head and name.startswith(head):
            return name[len(head):]
        return name
    return f


def canonical_text(env: Env, qname: str, prefix: str) -> str:
    strip = _strip(prefix)

    def show(t: Term) -> str:
        return pp(alpha_normalize(map_names(t, strip)))
    lines = []
    for n in sorted(cone(env, qname), key=strip):   # order by canonical name, so the prefix does not matter
        d = env.defs.get(n)
        if d is None:
            continue
        ty = show(d.type) if d.type is not None else "?"
        if d.data is not None:
            cons = " ; ".join(f"{strip(c.name)} : {show(c.type)}" for c in d.data.constructors)
            body = "data { " + cons + " }"
        elif d.body is None:
            body = "?"
        elif isinstance(d.body, Extern):
            body = f'extern "{d.body.target}"'
        else:
            body = show(d.body)
        lines.append(f"{strip(n)} : {ty} := {body}")
    return "\n".join(lines)


def definition_hash(env: Env, qname: str, prefix: str = "") -> str:
    text = canonical_text(env, qname, prefix)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def cert_path(lut_path: str) -> str:
    return os.path.splitext(lut_path)[0] + ".cert.json"


def read_certificate(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def write_certificate(path: str, reports: list, names: dict):
    """`names`: report.definition (qualified) -> name as written in that file."""
    data = read_certificate(path)
    for r in reports:
        data[names.get(r.definition, r.definition)] = {
            "hash": r.hash,
            "when": r.when,
            "passed": r.passed,
            "seed": r.seed,
            "run_seed": r.run_seed,
            "generation": r.generation,
            "laws": [asdict(l) for l in r.laws],
        }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
