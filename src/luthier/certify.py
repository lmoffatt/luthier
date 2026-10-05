"""Certificates: what was tested, over which code.

A certificate entry carries a hash of what the test ran (05 §7): the definition's dependency cone
(the definition and everything it refers to, rendered with the module prefix removed), the Python
behind every extern of the cone, and the interpreter. It also records the generators the laws drew
from, the case count and the mode. An entry is trusted only when all of them still match and the
count reaches the file's directive; otherwise the obligation is pending again, and the loader says
why. The hashes are compared once the whole program is loaded, with the holes filled, so a library
with holes is certified per filling: a certificate keeps one entry per filling of a name.
"""
from __future__ import annotations
import hashlib
import importlib
import json
import os
import sys
import sysconfig
from dataclasses import asdict, fields, is_dataclass

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


# ------------------------------------------------------------------ the Python behind the code

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
_FILE_HASHES: dict = {}
_DIR_HASHES: dict = {}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def _file_hash(path: str) -> str:
    st = os.stat(path)
    key = (path, st.st_mtime_ns, st.st_size)
    h = _FILE_HASHES.get(key)
    if h is None:
        with open(path, "rb") as f:
            h = _sha(f.read())
        _FILE_HASHES[key] = h
    return h


def _directory_hash(directory: str, suffixes=(".py",)) -> str:
    """The hash of the source files of a directory, not recursive: what a module there can import
    from its neighbours, so editing any of them changes it."""
    names = sorted(n for n in os.listdir(directory) if n.endswith(suffixes))
    key = (directory, tuple((n, os.stat(os.path.join(directory, n)).st_mtime_ns) for n in names))
    h = _DIR_HASHES.get(key)
    if h is None:
        h = _sha("\n".join(f"{n} {_file_hash(os.path.join(directory, n))}" for n in names).encode())
        _DIR_HASHES[key] = h
    return h


def interpreter_fingerprint() -> str:
    """The interpreter that ran a test: its Python sources and core.lut. Changing it changes what a
    law's evaluation means (phase 1 changed what a generator gives), so it invalidates certificates."""
    return _directory_hash(PACKAGE_DIR, (".py", ".lut"))


def _installed(path: str) -> bool:
    path = os.path.realpath(path)
    roots = {os.path.realpath(p) for k, p in sysconfig.get_paths().items() if k in ("stdlib", "platstdlib", "purelib", "platlib")}
    return "site-packages" in path or "dist-packages" in path or any(path.startswith(r + os.sep) for r in roots)


def module_fingerprint(module_name: str) -> str:
    """What the Python behind an extern is: for a module of the project or of the interpreter, the
    hash of the source files of its directory; for an installed package, its name and version; for
    a builtin module, the version of Python."""
    try:
        mod = sys.modules.get(module_name) or importlib.import_module(module_name)
    except ImportError:
        return f"missing module {module_name}"
    path = getattr(mod, "__file__", None)
    if path is None:
        return f"python {sys.version.split()[0]}"
    if _installed(path):
        top = module_name.split(".")[0]
        try:
            from importlib.metadata import version
            return f"{top} {version(top)}"
        except Exception:
            return f"python {sys.version.split()[0]}"
    return f"source {_directory_hash(os.path.dirname(os.path.realpath(path)))}"


def extern_module(target: str) -> str:
    """The module of an extern's target, `python:mod.attr` or `python:mod:attr`, as registered
    (`...@type`); "" for a target that is not Python (a filled hole)."""
    spec = target.split("@", 1)[0]
    if not spec.startswith("python:"):
        return ""
    spec = spec[len("python:"):]
    if ":" in spec:
        return spec.split(":", 1)[0]
    mod, _, _ = spec.rpartition(".")
    return mod


def _externs_in(t, acc: set):
    if isinstance(t, Extern):
        acc.add(t.target)
        return
    if isinstance(t, (list, tuple)):
        for x in t:
            _externs_in(x, acc)
        return
    if is_dataclass(t) and not isinstance(t, type):
        for f in fields(t):
            _externs_in(getattr(t, f.name), acc)


def externs_of_cone(env: Env, qname: str) -> list:
    """Every extern the cone of a definition calls: the bodies that are externs and the externs
    written inside other bodies (a field of a record literal)."""
    acc: set = set()
    for n in cone(env, qname):
        d = env.defs.get(n)
        if d is not None and d.body is not None:
            _externs_in(d.body, acc)
    return sorted(acc)


def fingerprint(env: Env, qname: str, prefix: str = "") -> dict:
    """The parts of what a test of `qname` ran: the code of its cone, the Python of each extern it
    calls, the interpreter."""
    externs = {}
    for target in externs_of_cone(env, qname):
        mod = extern_module(target)
        externs[target.split("@", 1)[0]] = module_fingerprint(mod) if mod else "filled"
    return {"code": _sha(canonical_text(env, qname, prefix).encode("utf-8")),
            "externs": dict(sorted(externs.items())),
            "interpreter": interpreter_fingerprint()}


def hash_of(fp: dict) -> str:
    return _sha(json.dumps(fp, sort_keys=True).encode("utf-8"))


def definition_hash(env: Env, qname: str, prefix: str = "") -> str:
    return hash_of(fingerprint(env, qname, prefix))


def why_different(old: dict, new: dict) -> str:
    """Which part of a fingerprint changed, for a reader: the code, the Python behind an extern, or
    the interpreter."""
    if not old:
        return "certified before fingerprints were recorded"
    if old.get("interpreter") != new.get("interpreter"):
        return "the interpreter changed"
    if old.get("code") != new.get("code"):
        return "the code of its cone changed"
    oe, ne = old.get("externs", {}), new.get("externs", {})
    changed = sorted(t for t in set(oe) | set(ne) if oe.get(t) != ne.get(t))
    if changed:
        return "the Python behind " + ", ".join(changed[:3]) + (" and more" if len(changed) > 3 else "") + " changed"
    return "the fingerprint changed"


def generator_fingerprint(checker, key: str) -> str:
    """What a generator is: the Python of a registered one, the code of a Luthier one."""
    g = checker.gens.get(key)
    if g is None:
        return "missing"
    kind, label, term = g
    if kind == "extern":
        mod = extern_module(label)
        return module_fingerprint(mod) if mod else "filled"
    names = sorted(n for n in names_in(term) if n in checker.env.defs)
    text = "\n".join(canonical_text(checker.env, n, "") for n in names)
    return _sha((pp(term) + "\n" + text).encode("utf-8"))


def cert_path(lut_path: str) -> str:
    return os.path.splitext(lut_path)[0] + ".cert.json"


def read_certificate(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def entries_of(value) -> list:
    """The entries a certificate keeps for one name: one per filling of the holes its cone depends on,
    most recent first. An entry of the first format is a list of one."""
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [e for e in value if isinstance(e, dict)]
    return []


MAX_ENTRIES = 4


def write_certificate(path: str, reports: list, names: dict, keep: set = None):
    """`names`: report.definition (qualified) -> name as written in that file. An entry replaces the
    one with the same hash and joins the others (another filling of the holes), up to MAX_ENTRIES.
    `keep`, when given, is the set of names the file still defines with laws: the others are pruned."""
    import fcntl
    with open(path + ".lock", "w") as lock:
        # several `luthier test` processes may write one file's certificate (the imports of each)
        fcntl.flock(lock, fcntl.LOCK_EX)
        _write_certificate(path, reports, names, keep)


def _write_certificate(path: str, reports: list, names: dict, keep: set = None):
    data = read_certificate(path)
    if keep is not None:
        data = {k: v for k, v in data.items() if k in keep}
    for r in reports:
        local = names.get(r.definition, r.definition)
        entry = {
            "hash": r.hash,
            "when": r.when,
            "passed": r.passed,
            "outcome": r.outcome,
            "n": r.n,
            "mode": r.mode,
            "seed": r.seed,
            "run_seed": r.run_seed,
            "fingerprint": r.fingerprint,
            "generators": r.generators,
            "provisional": r.provisional,
            "generation": r.generation,
            "laws": [asdict(l) for l in r.laws],
        }
        # entries of another filling are kept; those written before fingerprints can match nothing
        others = [e for e in entries_of(data.get(local)) if e.get("hash") != r.hash and e.get("fingerprint")]
        data[local] = ([entry] + others)[:MAX_ENTRIES]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
