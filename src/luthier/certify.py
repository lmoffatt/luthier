"""Certificates: the hash of a cone, the store of entries `x.cert.json`, and `luthier certify`.

Sources: src/luthier/lib/certification.lth (§1 the entry and the store, §2 the certificate, §4 the
hash of a cone) and its model certification_model.lut; spec 6.S8, 7.S9, 7.S13, 12.S11, 12.S16;
term.lth §4 through kernel.canonical. Derivation: record/IA/certification-2026-10-14/
prompt-certify.md (step 5.3 of the plan from zero), by a Claude agent of the coordinating session,
2026-10-14. What the theory left open is marked [proposed] where it is chosen.

The cone of a name is every definition of the runtime program the name reaches (its type and its
body, the data of each constructor it names), each in canonical form: binders renamed by
kernel.canonical, module prefixes and the `@file` tag the loader gives a clashing name not seen,
an extern by its route only. With it go the host code behind each extern of the cone, by route,
and the interpreter's revision. `cone_hash` is certification.lth §4's `ConeHashing.hash`, the
route `python:luthier.certify.cone_hash` certification_model.lut names; `Cones` builds the cone of
a name from a program.

The store `x.cert.json` beside `x.lut` is a JSON list of entries, the latest in front, each as
certification.lth's `Entry` reads them. Its predicate (`Store`: one outcome per identity, a grade
exactly when passed) is checked on every store read or written; `record` never edits an entry and
leaves the store as it is on a known identity; a stale entry is kept, and is stale only as read
against the current hash of its law's cone (12.S11), never marked in the file.

§3, what a run requires (`contains`, `covers_all`, `serves`, `state_of`, `refuse`), is the reading
of the store `run` makes before evaluating (run.py's `certification`), after
record/IA/certification-2026-10-14/prompt-run.md; it writes nothing.
"""
from __future__ import annotations

import functools
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import platform
import subprocess
import sys
import sysconfig
from dataclasses import fields, is_dataclass, replace
from datetime import datetime, timezone
from pathlib import Path

from . import kernel, term as t

_PACKAGE = Path(__file__).resolve().parent

# test.lth's `gradeRank`
GRADE_RANK = {"Proved": 4, "ExhaustiveGrade": 3, "Cases": 2, "Sampled": 1, "AssumedGrade": 0}
GRADE_WORDS = {"Proved": "proved", "ExhaustiveGrade": "exhaustive", "Cases": "cases", "Sampled": "sampled",
               "AssumedGrade": "assumed"}


def _sha(text):
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------- §4 the hash of a cone

def _plain(x):
    """A term as the hash sees it before canonical form: each name without the `@file` the loader
    gives a name two files define (run.py's `Loaded`), an extern by its route (the type the Runner
    gives it is the definition's, already in the code). Literals are kept as written."""
    if isinstance(x, str):
        return x.partition("@")[0]
    if isinstance(x, t.Extern):
        return t.Extern(x.route)
    if isinstance(x, (t.Lit, t.Primitive, t.Axiom)):
        return x
    if isinstance(x, tuple):
        return tuple(_plain(y) for y in x)
    if is_dataclass(x) and not isinstance(x, type):
        return replace(x, **{f.name: _plain(getattr(x, f.name)) for f in fields(x) if f.init})
    return x


def canon(term):
    """term.lth §4's canonical form as the hash reads it: `kernel.canonical` (binders renamed in
    preorder, free names unqualified) of the term without file tags."""
    return kernel.canonical(_plain(term))


def canon_code(code):
    """certification.lth's `canonCode`: each name unqualified, each term canonical."""
    return [(kernel.unqualify(_plain(name)), canon(term)) for name, term in code]


def _items(cone):
    """The three parts of a cone given as a mapping (a dict, the bridge's record) or an object."""
    get = (lambda k: cone[k]) if isinstance(cone, dict) else (lambda k: getattr(cone, k))
    return list(get("code")), list(get("hosts")), get("interpreter")


def _shown(term):
    """A term's text for the hash: the repr of the kernel's frozen dataclasses (each string quoted,
    so injective on terms); a value the bridge gives in another form, its repr too."""
    return repr(term)


def cone_hash(cone, name=None):
    """certification.lth §4's `hash`: sha256 of the cone's code in canonical form, its hosts by
    route and the interpreter's revision, in the order the cone lists them (the order is the
    builder's, `Cones.cone`: by name, by route). With a `name`, `cone` is a program (a Runner, a
    tuple of kernel acts or a `Cones`) and the hash is that of the cone of `name` in it."""
    if name is not None:
        cones = cone if isinstance(cone, Cones) else Cones(cone)
        return cones.hash(name)
    code, hosts, interpreter = _items(cone)
    # a cone of kernel terms is put in canonical form here; a cone the bridge gives (term.lth's
    # `Term` as the host reads it) is hashed as given [proposed: its canonical form is term_model's]
    code = canon_code(code) if _kernel_code(code) else [(str(n), term) for n, term in code]
    payload = {
        "code": [[n, _shown(term)] for n, term in code],
        "hosts": [[str(r), str(h)] for r, h in hosts],
        "interpreter": str(interpreter),
    }
    return _sha(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))


_TERMS = tuple(c for c in vars(t).values() if isinstance(c, type) and is_dataclass(c))


def _kernel_code(code):
    return all(isinstance(term, _TERMS) for _, term in code)


@functools.cache
def interpreter_revision():
    """The interpreter's revision (6.S8): the commit of this repository that last changed the Python
    of src/luthier/ [proposed: the libraries under lib/ enter by the code of each cone, not here],
    followed by `+` and the hash of those files when the working tree changes them; the package's
    version when it is installed without its repository."""
    try:
        def git(*args):
            return subprocess.run(["git", "-C", str(_PACKAGE), *args], capture_output=True, text=True,
                                  check=True).stdout.strip()
        commit = git("log", "-1", "--format=%H", "--", "*.py")
        if not commit:
            raise OSError("not in a repository")
        dirty = git("status", "--porcelain", "--", "*.py")
    except (OSError, subprocess.CalledProcessError):
        try:
            return "luthier " + importlib.metadata.version("luthier")
        except importlib.metadata.PackageNotFoundError:
            return "luthier unversioned " + _python_files_hash()[:19]
    return commit if not dirty else f"{commit}+{_python_files_hash()[7:19]}"


def _python_files_hash():
    h = hashlib.sha256()
    for p in sorted(_PACKAGE.rglob("*.py")):
        h.update(str(p.relative_to(_PACKAGE)).encode())
        h.update(p.read_bytes())
    return "sha256:" + h.hexdigest()


@functools.cache
def host_hash(route):
    """The host code behind an extern (6.S8): the source file of the route's module, by its bytes;
    for a module of an installed package, the package and its version; for the standard library or
    a built-in module, Python's version. A route that names no module found is its own text."""
    if not route.startswith("python:"):
        return "route " + route
    module = route[len("python:"):].rsplit(".", 1)[0]
    try:
        spec = importlib.util.find_spec(module)
    except (ImportError, ValueError):
        spec = None
    if spec is None:
        return "missing " + module
    origin = spec.origin
    if origin in (None, "built-in", "frozen") or not os.path.exists(origin):
        return f"python {platform.python_version()}"
    path = Path(origin).resolve()
    paths = sysconfig.get_paths()
    sites = {Path(paths[k]).resolve() for k in ("purelib", "platlib") if k in paths}
    sites |= {Path(p).resolve() for p in sys.path if p.endswith(("site-packages", "dist-packages"))}
    if any(path.is_relative_to(s) for s in sites):
        top = module.split(".")[0]
        dists = importlib.metadata.packages_distributions().get(top, [])
        for dist in dists:
            try:
                return f"{dist} {importlib.metadata.version(dist)}"
            except importlib.metadata.PackageNotFoundError:
                continue
    stdlib = {Path(paths[k]).resolve() for k in ("stdlib", "platstdlib") if k in paths}
    if any(path.is_relative_to(s) for s in stdlib) and not any(path.is_relative_to(s) for s in sites):
        return f"python {platform.python_version()}"
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _walk(x, out):
    """The constructors a term's patterns name and the routes of its externs."""
    if isinstance(x, t.PCon):
        out["constructors"].add(x.name)
    if isinstance(x, t.Extern):
        if x.route.startswith("python:"):
            out["routes"].add(x.route)
        return
    if isinstance(x, (str, t.Lit)):
        return
    if isinstance(x, tuple):
        for y in x:
            _walk(y, out)
    elif is_dataclass(x) and not isinstance(x, type):
        for f in fields(x):
            _walk(getattr(x, f.name), out)


class Cones:
    """The cones of a program's names (6.S8): the program is the runtime program a run or a test
    reduces (kernel acts, a Runner's `program`)."""

    def __init__(self, program):
        program = getattr(program, "program", program)
        self.acts = {}
        for act in program:
            if isinstance(act, (t.Define, t.Declare)):
                self.acts.setdefault(act.name, []).append(act)
        # the data a constructor belongs to
        self.owner = {}
        for name, acts in self.acts.items():
            for act in acts:
                for data in _datas(getattr(act, "body", None)):
                    for c, _ in data.constructors:
                        self.owner.setdefault(c, name)
        self.memo = {}

    def _part(self, name):
        """One name's code, references and routes, computed once."""
        if name not in self.memo:
            code, refs, routes = [], set(), set()
            for act in self.acts.get(name, ()):
                term = t.Pair(act.type, act.body) if isinstance(act, t.Define) else act.type
                term = _plain(term)
                out = {"constructors": set(), "routes": set()}
                _walk(term, out)
                refs |= set(kernel.free_names(term)) | out["constructors"]
                routes |= out["routes"]
                code.append((name.partition("@")[0], kernel.canonical(term)))
            self.memo[name] = (code, refs, routes)
        return self.memo[name]

    def names(self, name):
        """The names the cone of `name` reaches, itself included (as the program calls them)."""
        seen, pending = set(), [name]
        tags = {}
        for n in self.acts:
            tags.setdefault(n.partition("@")[0], []).append(n)
        while pending:
            n = pending.pop()
            if n in seen or n not in self.acts:
                continue
            seen.add(n)
            _, refs, _ = self._part(n)
            for r in refs:
                for m in (r, self.owner.get(r)) + tuple(tags.get(r, ())):
                    if m is not None and m not in seen and m in self.acts:
                        pending.append(m)
        return seen

    def cone(self, name):
        """certification.lth's `Cone` of `name`: the code by name (then by its text), the hosts by
        route, the interpreter's revision."""
        code, routes = [], set()
        for n in self.names(name):
            c, _, r = self._part(n)
            code.extend(c)
            routes |= r
        code.sort(key=lambda item: (item[0], repr(item[1])))
        return {"code": code, "hosts": [(r, host_hash(r)) for r in sorted(routes)],
                "interpreter": interpreter_revision()}

    def hash(self, name):
        return cone_hash(self.cone(name))

    def hosts(self, name):
        return self.cone(name)["hosts"]


def _datas(term):
    if isinstance(term, t.Data):
        yield term
    elif isinstance(term, t.Lam):
        yield from _datas(term.body)


# ---------------------------------------------------------------------- §1 the entry and the store

def store_path(path):
    """`x.cert.json` beside `x.lut` (12.S10)."""
    path = Path(path)
    return path.with_name(path.stem + ".cert.json")


IDENTITY = ("law", "cone", "binding", "seed", "cases")


def identity(entry):
    """certification.lth's `identity`: the law, the cone's hash, the binding expanded, the seed and
    `n` (7.S9, 7.S13), as one comparable key."""
    return json.dumps([entry[k] for k in IDENTITY], sort_keys=True, ensure_ascii=False)


def passed(entry):
    return entry["outcome"] == "Passed"


def store_errors(entries):
    """What breaks `Store`'s predicate: two entries of one identity with different outcomes
    (`determined`), or a grade without a pass or a pass without a grade (`gradedAsOutcome`)."""
    errors, seen = [], {}
    for k, e in enumerate(entries):
        missing = [f for f in IDENTITY + ("outcome", "grade") if f not in e]
        if missing:
            errors.append(f"entry {k} lacks {', '.join(missing)}")
            continue
        if passed(e) != (e["grade"] is not None):
            errors.append(f"entry {k} ({e['law']}): a grade exactly when passed")
        i = identity(e)
        if i in seen and entries[seen[i]]["outcome"] != e["outcome"]:
            errors.append(f"entries {seen[i]} and {k} ({e['law']}): one identity, two outcomes")
        seen.setdefault(i, k)
    return errors


class StoreError(ValueError):
    pass


def read_store(path):
    """The entries of `x.cert.json`, the latest in front; [] when there is none. A store that breaks
    `Store`'s predicate is refused."""
    where = store_path(path)
    if not where.exists():
        return []
    entries = json.loads(where.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise StoreError(f"{where}: not a list of entries")
    errors = store_errors(entries)
    if errors:
        raise StoreError(f"{where}: " + "; ".join(errors))
    return entries


def write_store(path, entries):
    errors = store_errors(entries)
    if errors:
        raise StoreError(f"{store_path(path)}: " + "; ".join(errors))
    where = store_path(path)
    tmp = where.with_name(where.name + ".tmp")
    tmp.write_text(json.dumps(entries, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(where)
    return where


def known(entries, key):
    """certification.lth's `known`: the latest entry with the identity asked, whatever its outcome."""
    return next((e for e in entries if identity(e) == key), None)


def record(entries, entry):
    """certification.lth's `record`: a new entry in front, the store unchanged on a known identity."""
    if known(entries, identity(entry)) is not None:
        return entries
    return [entry] + list(entries)


def add_entry(path, entry):
    """`record` into the store of another file (a model's, beside its definition): read, record and
    write under a lock, since several test programs may add to one store at once."""
    import fcntl
    where = store_path(path)
    with open(where.with_name(where.name + ".lock"), "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        entries = read_store(path)
        recorded = record(entries, entry)
        if recorded is not entries:
            write_store(path, recorded)
    return where


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------- §2 the certificate, and the state

def stale(current, entry):
    """certification_model's `stale`: the entry's hash is not the current hash of its cone."""
    return entry["cone"] != current


def certificate_grade(entries, law, current):
    """certification_model's `grade`: over the law's entries at the current hash, none when one
    failed or none passed; under one binding the strongest pass, across bindings the weakest."""
    counts = [e for e in entries if e["law"] == law and e["cone"] == current]
    if any(isinstance(e["outcome"], dict) and "Failed" in e["outcome"] for e in counts):
        return None
    best = {}
    for e in counts:
        if passed(e) and e["grade"] is not None:
            b = json.dumps(e["binding"], sort_keys=True)
            g = e["grade"]
            if b not in best or GRADE_RANK[g] > GRADE_RANK[best[b]]:
                best[b] = g
    if not best:
        return None
    return min(best.values(), key=GRADE_RANK.__getitem__)


def state(entries, law, current):
    """certification_model's `stateOf` without a demand: ("current", outcome of the latest entry at
    the current hash), ("stale", the latest other hash), or ("uncertified", None)."""
    at = next((e for e in entries if e["law"] == law and e["cone"] == current), None)
    if at is not None:
        return "current", at["outcome"]
    other = next((e for e in entries if e["law"] == law), None)
    if other is not None:
        return "stale", other["cone"]
    return "uncertified", None


def show_outcome(outcome):
    if outcome == "Passed":
        return "passed"
    (kind, why), = outcome.items()
    return f"failed at {why}" if kind == "Failed" else f"not run: {why}"


def standing(entries, law, current):
    """One law's standing as `check -v` and `certify` print it."""
    kind, what = state(entries, law, current)
    if kind == "uncertified":
        return "uncertified"
    if kind == "stale":
        return f"stale (its entries are at {what[7:19]}, the cone is now at {current[7:19]})"
    g = certificate_grade(entries, law, current)
    if g is not None:
        return GRADE_WORDS[g]
    failed = next((e for e in entries if e["law"] == law and e["cone"] == current
                   and isinstance(e["outcome"], dict) and "Failed" in e["outcome"]), None)
    if failed is not None:
        return "refuted at " + failed["outcome"]["Failed"]
    return show_outcome(what)


def standings(path):
    """Per law a test line of the file names: its standing from the store, against the current
    hash of its cone (12.S11, 12.S14)."""
    from .tester import law_cones
    entries = read_store(path)
    return [(law, standing(entries, law, current)) for law, current in law_cones(path)]


# ---------------------------------------------------------------------- §3 what a run requires

# the grades a demand may accept, as `--accept` names them (test.lth's `Grade`)
GRADES = {word: grade for grade, word in GRADE_WORDS.items()}


def contains(reach, value):
    """certification_model's `contains`: the support holds every value, an interval the numbers
    between its ends (ends included), a census its members."""
    if reach == "Support":
        return True
    (kind, what), = reach.items()
    if kind == "Interval":
        return "Number" in value and what[0] <= value["Number"] <= what[1]
    return kind == "Members" and value in what


def covers_all(reach, given):
    """certification.lth's `coversAll`: each value given is in the reach recorded for its parameter
    (the first recorded, as `reachOf`); a parameter with no reach recorded covers nothing."""
    reaches = {}
    for r in reach:
        reaches.setdefault(r["parameter"], r["reach"])
    return all(p in reaches and contains(reaches[p], v) for p, v in given)


def at(demand, entry):
    """Whether the entry is at the demand's hash: its law's cone, and [proposed] the cone of each
    model the demand names (`fingerprints`: parameter -> the current hash of the name the run gives
    it), as the fingerprint the entry's binding recorded for that parameter, when the entry's reach
    holds that model. The tester hashes the
    law's cone and keeps the model's in the binding (7.S9); an entry whose model has changed since
    is at another hash, so stale for this demand."""
    if entry["cone"] != demand["cone"]:
        return False
    drawn = {d["parameter"]: d["fingerprint"] for d in entry["binding"]}
    given = dict(demand["given"])
    # an entry whose reach does not hold the model given is about another model: its fingerprint
    # says nothing of this one, and `serves` refuses it by its reach
    return all(drawn.get(p) == h for p, h in demand.get("fingerprints", {}).items()
               if covers_all(entry["reach"], [(p, given[p])]))


def serves(demand, entry):
    """certification_model's `serves`: the law's entry at the current hash, passed, at or above the
    grade the demand accepts, its reach covering what the run gives."""
    return (entry["law"] == demand["law"] and at(demand, entry) and passed(entry)
            and entry["grade"] is not None and GRADE_RANK[demand["accepts"]] <= GRADE_RANK[entry["grade"]]
            and covers_all(entry["reach"], demand["given"]))


def state_of(demand, entries):
    """certification_model's `stateOf`: ("Current", the outcome of the latest entry at the current
    hash), else ("Stale", the hash of the law's latest entry), else ("Uncertified", None)."""
    e = next((e for e in entries if e["law"] == demand["law"] and at(demand, e)), None)
    if e is not None:
        return "Current", e["outcome"]
    f = next((e for e in entries if e["law"] == demand["law"]), None)
    if f is not None:
        return "Stale", f["cone"]
    return "Uncertified", None


def refuse(entries, cone):
    """certification_model's `refuse`: per name of the cone (`name`, `provisional`, `laws`, each
    law a demand), a provisional name refused whole, otherwise each law no entry serves, listed
    with its state (`RefusalSaysWhy`, `RefusalIsPerLaw`, `ProvisionalIsRefused`)."""
    refusals = []
    for c in cone:
        if c["provisional"]:
            refusals.append({"name": c["name"], "law": None, "state": ("Provisional", None)})
            continue
        for d in c["laws"]:
            if not any(serves(d, e) for e in entries):
                refusals.append({"name": c["name"], "law": d["law"], "state": state_of(d, entries),
                                 "demand": d})
    return refusals


def show_refusal(refusal, entries):
    """One line of `run`'s refusal: the name, the law and its state; for a law whose latest entry
    at the current hash passed, why it does not serve [proposed, certification.lth's `State`]."""
    kind, what = refusal["state"]
    head = refusal["name"] if refusal["law"] is None else f"{refusal['name']}: {refusal['law']}"
    if kind == "Provisional":
        return f"{head}: provisional (built on an extern not yet validated)"
    if kind == "Uncertified":
        return f"{head}: uncertified (no entry)"
    d = refusal["demand"]
    if kind == "Stale":
        if what == d["cone"]:
            return f"{head}: stale (the model's code changed since its entries)"
        return f"{head}: stale (its entries are at {what[7:19]}, the cone is now at {d['cone'][7:19]})"
    if what != "Passed":
        return f"{head}: {show_outcome(what)}"
    current = [e for e in entries if e["law"] == d["law"] and at(d, e) and passed(e)]
    if all(GRADE_RANK[e["grade"]] < GRADE_RANK[d["accepts"]] for e in current):
        best = max((e["grade"] for e in current), key=GRADE_RANK.__getitem__)
        return f"{head}: passed, {GRADE_WORDS[best]}, below the grade accepted ({GRADE_WORDS[d['accepts']]})"
    shown = ", ".join(f"{p} = {_shown_value(v)}" for p, v in d["given"])
    return f"{head}: passed, but no passed entry's reach covers {shown}"


def _shown_value(v):
    return repr(v["Number"]) if "Number" in v else v["Printed"]


# ---------------------------------------------------------------------- `luthier certify` (12.S16)

def certify_file(path, seed=None, deep=False, fuel=1_000_000):
    """Run one file's test lines, writing its store; per law its certificate's grade (the weakest
    across bindings), with the counts of lines run and known. Runs in its own process."""
    from .tester import run_tests
    try:
        outcomes = run_tests(path, seed, fuel, deep=deep, store=True)
    except Exception as exc:  # the file's failure is reported with the file, the others go on
        return {"path": str(path), "error": f"{type(exc).__name__}: {exc}"}
    entries = read_store(path)
    laws = {}
    for o in outcomes:
        laws.setdefault(o.spec.law, o.cone)
    return {"path": str(path),
            "laws": [(law, standing(entries, law, cone)) for law, cone in laws.items()],
            "ran": sum(1 for o in outcomes if o.known is None),
            "known": sum(1 for o in outcomes if o.known is not None),
            "graded": all(certificate_grade(entries, law, cone) is not None for law, cone in laws.items())}


def certify(paths, jobs=1, seed=None, deep=False, fuel=1_000_000, out=print):
    """`luthier certify`: each file in its own process, `jobs` at a time; prints per file its laws
    and their grades. True when every law of every file has a grade."""
    from concurrent.futures import ProcessPoolExecutor
    import multiprocessing
    context = multiprocessing.get_context("spawn")
    ok = True
    with ProcessPoolExecutor(max_workers=max(1, jobs), mp_context=context, max_tasks_per_child=1) as pool:
        futures = [pool.submit(certify_file, str(p), seed, deep, fuel) for p in paths]
        for future in futures:
            result = future.result()
            if "error" in result:
                out(f"{result['path']}: {result['error']}")
                ok = False
                continue
            out(f"{result['path']}: {len(result['laws'])} laws, {result['ran']} lines ran, "
                f"{result['known']} known")
            for law, s in result["laws"]:
                out(f"  {law}: {s}")
            ok &= result["graded"]
    return ok
