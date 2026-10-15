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

Controls (record/IA/controls-2026-10-15/prompt-tester.md; 7.S19 as D-2026-10-15-a generalized it,
L9.14): an entry of `"kind": "Control"` is a law's run on a model broken on purpose (tester.py).
It is part of no certificate: the grade, the state, `serves` and `refuse` read the law's own
entries only, so a control's refutation never refutes the law. What it gives is the law's control
status, reported beside its grade by `certify` and `check -v` (`control_status`): controlled (a
control refuted at the law's current cone hash), control failed (a control the law held on at that
hash, reported loudly), or uncontrolled, untested against any wrong model. The grade is unchanged
by it (the demand's business later). [proposed] A law and its control are matched by the hash of
the law's cone, which names the law; the controls read are those of the files `certify` or
`check -v` is given, so a law certified without its control file is reported uncontrolled.

Statistical laws (record/IA/statistical-2026-10-15/prompt-tester.md; laws.lth §4, 7.S17, L9.15): an
entry whose evidence is `Tested` holds the sequential test's verdict with alpha, beta, delta, the
samples spent, and the cutoffs' `initial` and `budget` (`tested_text` reads them). A pass is graded
as any (sampled, over `Drawn seed`); `standing` adds the rates and what was spent to the grade, so
that the certificate shows the price of a sampled grade (7.S17). An unresolved test is a
`Unresolved` outcome carrying the test's record (older stores wrote `NotRunFor "unresolved at ..."`, still read).
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
    """The interpreter's revision (6.S8): the last tag reachable from HEAD of this repository
    (`git describe --tags --abbrev=0`), with no dirty marker, so that the stores stay current
    between tags [proposed: night default for decision 2 of record/IA/certification-2026-10-14/
    report-run.md; before it, the last commit touching src/luthier/*.py plus a dirty hash made
    every store stale at each commit; the host code behind a cone's externs is hashed by file,
    host_hash, 6.S8's other part; the libraries under lib/ enter by the code of each cone]. The
    package's version when it is installed without its repository (or the repository has no tag)."""
    try:
        tag = subprocess.run(["git", "-C", str(_PACKAGE), "describe", "--tags", "--abbrev=0"],
                             capture_output=True, text=True, check=True).stdout.strip()
        if not tag:
            raise OSError("no tag")
        return tag
    except (OSError, subprocess.CalledProcessError):
        try:
            return "luthier " + importlib.metadata.version("luthier")
        except importlib.metadata.PackageNotFoundError:
            return "luthier unversioned " + _python_files_hash()[:19]


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
                # the references by the names the program calls them (`apart@plot`, not `apart`), so
                # that the cone reaches the definitions the name reaches and no other of the same
                # plain name; the tags go only from the code that is hashed
                out = {"constructors": set(), "routes": set()}
                _walk(term, out)
                refs |= set(kernel.free_names(term)) | out["constructors"]
                routes |= out["routes"]
                code.append((name.partition("@")[0], kernel.canonical(_plain(term))))
            self.memo[name] = (code, refs, routes)
        return self.memo[name]

    def names(self, name):
        """The names the cone of `name` reaches, itself included (as the program calls them)."""
        # each reference by its exact name: a definition of the same plain name in another file (the
        # loader's `name@file`) is another name, and the importer's names never enter the cone of a
        # library name (6.S8, 12.S22; record/IA/certification-2026-10-14/prompt-scope.md item 2)
        seen, pending = set(), [name]
        while pending:
            n = pending.pop()
            if n in seen or n not in self.acts:
                continue
            seen.add(n)
            _, refs, _ = self._part(n)
            for r in refs:
                for m in (r, self.owner.get(r)):
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
CONTROL = "Control"  # the kind of a control's entry (tester.py); a law's entry has no kind


def is_control(entry):
    return entry.get("kind") == CONTROL


def _laws_own(entries):
    """The entries that are the law's evidence: every entry but the controls."""
    return [e for e in entries if not is_control(e)]


def identity(entry):
    """certification.lth's `identity`: the law, the cone's hash, the binding expanded, the seed and
    `n` (7.S9, 7.S13), as one comparable key; a control's kind is part of it [proposed]."""
    key = [entry[k] for k in IDENTITY] + ([entry["kind"]] if "kind" in entry else [])
    return json.dumps(key, sort_keys=True, ensure_ascii=False)


def passed(entry):
    return entry["outcome"] == "Passed"


def _failed(entry):
    """certification.lth's `isFailure`: the outcome is `Failed` (not `NotRunFor`)."""
    return isinstance(entry["outcome"], dict) and "Failed" in entry["outcome"]


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
        tested = _tested(e)
        if passed(e) and tested and not (tested.get("verdict") == "Holds" and e["grade"] == "Sampled"):
            errors.append(f"entry {k} ({e['law']}): a statistical pass is a Holds graded sampled")
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


KEEP = 4


def _group(entry):
    """(law, binding without the fingerprints): the identity without the seed and `n` and without
    the hashes of the census' cones, which change when a cone does."""
    binding = entry["binding"]
    if isinstance(binding, list):
        binding = [{k: v for k, v in d.items() if k != "fingerprint"} if isinstance(d, dict) else d
                   for d in binding]
    key = [entry["law"], binding] + ([entry["kind"]] if "kind" in entry else [])
    return json.dumps(key, sort_keys=True, ensure_ascii=False)


def _stamp(entry):
    """What makes an entry current: its cone's hash and the fingerprints of its binding."""
    binding = entry["binding"]
    prints = [d.get("fingerprint") for d in binding if isinstance(d, dict)] if isinstance(binding, list) else []
    return json.dumps([entry["cone"], prints])


def prune(entries, current=None, keep=KEEP):
    """The store bounded [proposed, 6.S8 "up to four" and 12.S11]: per (law, binding without
    fingerprints), the `keep` most recent entries at the current cone hash and fingerprints (by date,
    the store's order breaking ties), and no stale entry once a current one exists; a group with no
    current entry keeps its most recent entry only. `current` maps a group's key to a `_stamp`, and a
    group not in it takes the stamp of its most recent entry. What stays keeps the store's order
    (latest in front)."""
    current = dict(current or {})
    order = sorted(range(len(entries)), key=lambda k: (entries[k].get("date", ""), -k), reverse=True)
    groups = {}
    for k in order:
        groups.setdefault(_group(entries[k]), []).append(k)
    dropped = set()
    for g, ks in groups.items():
        stamp = current.get(g)
        if stamp is None:
            stamp = _stamp(entries[ks[0]])
        at = [k for k in ks if _stamp(entries[k]) == stamp]
        if at:
            dropped.update(at[keep:])
            dropped.update(k for k in ks if _stamp(entries[k]) != stamp)
        else:
            dropped.update(ks[1:])
    return [e for k, e in enumerate(entries) if k not in dropped]


def record(entries, entry):
    """certification.lth's `record`: a new entry in front, the store unchanged on a known identity;
    the entry's (law, binding) is then pruned at its cone hash (`prune`)."""
    if known(entries, identity(entry)) is not None:
        return entries
    return prune([entry] + list(entries), {_group(entry): _stamp(entry)})


def prune_stores(paths, out=print):
    """`luthier certify --prune FILES`: each file is a store (x.cert.json) or the x.lut beside one;
    it is rewritten bounded, nothing is run."""
    for path in paths:
        where = store_path(path) if not str(path).endswith(".cert.json") else Path(path)
        if not where.exists():
            out(f"{where}: no store")
            continue
        entries = json.loads(where.read_text(encoding="utf-8"))
        kept = prune(entries)
        if len(kept) != len(entries):
            write_store(where.with_name(where.name[:-len(".cert.json")]), kept)
        out(f"{where}: {len(entries)} -> {len(kept)} entries")
    return 0


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
    counts = [e for e in _laws_own(entries) if e["law"] == law and e["cone"] == current]
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
    the current hash), ("stale", the latest other hash), or ("uncertified", None). Controls aside."""
    entries = _laws_own(entries)
    at = next((e for e in entries if e["law"] == law and e["cone"] == current), None)
    if at is not None:
        return "current", at["outcome"]
    other = next((e for e in entries if e["law"] == law), None)
    if other is not None:
        return "stale", other["cone"]
    return "uncertified", None


def _number(x):
    return f"{x:g}" if isinstance(x, float) else str(x)


def tested_text(tested):
    """A sequential test's verdict as the lines and the certificate print it: the samples spent of
    their size, and its rates against its budget (laws.lth §4's `Rates` and `Sequential`)."""
    return (f"{tested['spent']} samples of {tested['initial']} by the sequential test (alpha "
            f"{_number(tested['alpha'])}, beta {_number(tested['beta'])}, delta {_number(tested['delta'])}, "
            f"budget {tested['budget']})")


def _tested(entry):
    evidence = entry.get("evidence")
    return evidence.get("Tested") if isinstance(evidence, dict) else None


def show_outcome(outcome):
    if outcome == "Passed":
        return "passed"
    (kind, why), = outcome.items()
    if kind == "Unresolved":
        return "unresolved at " + (tested_text(why) if isinstance(why, dict) else str(why))
    if kind == "NotRunFor" and why.startswith("unresolved at "):
        return why  # entries written before `Unresolved` was an outcome
    if kind == "ControlRefuted":
        return f"refuted at {why}: the control passed"
    if kind == "ControlConfirmed":
        return f"{CONTROL_FAILED} ({why})"
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
        # a statistical law's pass carries its rates and what it spent (7.S17), the latest's
        tested = next((_tested(e) for e in _laws_own(entries) if e["law"] == law and e["cone"] == current
                       and passed(e) and _tested(e)), None)
        return f"supported, {GRADE_WORDS[g]}: held at {tested_text(tested)}" if tested else GRADE_WORDS[g]
    failed = next((e for e in _laws_own(entries) if e["law"] == law and e["cone"] == current
                   and isinstance(e["outcome"], dict) and "Failed" in e["outcome"]), None)
    if failed is not None:
        return "refuted at " + failed["outcome"]["Failed"]
    return show_outcome(what)


def standings(path):
    """Per law a test line of the file names: its standing from the store, against the current
    hash of its cone (12.S11, 12.S14). Control lines aside (`control_standings`)."""
    from .tester import law_cones
    entries = read_store(path)
    return [(law, standing(entries, law, current)) for law, current in law_cones(path)]


# ---------------------------------------------------------------------- controls (7.S19, L9.14)

CONTROL_FAILED = "CONTROL FAILED: the law held on the model broken on purpose, too weak to see the break (7.S19)"
UNCONTROLLED = "uncontrolled: untested against any wrong model (7.S19)"


def _refuted(entry):
    return isinstance(entry["outcome"], dict) and "ControlRefuted" in entry["outcome"]


def _held(entry):
    return isinstance(entry["outcome"], dict) and "ControlConfirmed" in entry["outcome"]


def control_status(controls, law, current):
    """A law's control status from control entries (any store's, or a run's): "control failed" when
    one at the law's current cone hash came out confirmed, else "controlled" when one there was
    refuted, else uncontrolled (with what the controls of other hashes, or not run, were). The
    law is matched by its cone's hash, which names it; `law` names the stale ones only."""
    at = [e for e in controls if is_control(e) and e["cone"] == current]
    held = [e for e in at if _held(e)]
    if held:
        on = "; ".join(", ".join(d["generator"] for d in e["binding"]) for e in held) or "no binding"
        return f"{CONTROL_FAILED}, on {on}"
    refuted = [e for e in at if _refuted(e)]
    if refuted:
        cases = "; ".join(dict.fromkeys(e["outcome"]["ControlRefuted"] for e in refuted))
        return f"controlled (refuted on its control{'s' if len(refuted) > 1 else ''} at {cases})"
    if at:
        return f"{UNCONTROLLED}; its control did not run ({show_outcome(at[0]['outcome'])})"
    if any(is_control(e) and e["law"] == law for e in controls):
        return f"{UNCONTROLLED}; its controls are at another hash of its cone"
    return UNCONTROLLED


def control_standing(entries, law, current):
    """The standing of a law's control lines in a store: of its control entries at the law's
    current cone hash, a failed one first, else a refuted one, else the latest, as `show_outcome`
    reads it; stale or no entry otherwise."""
    at = [e for e in entries if is_control(e) and e["law"] == law and e["cone"] == current]
    if at:
        return show_outcome(next((e for e in at if _held(e)), next((e for e in at if _refuted(e)), at[0]))["outcome"])
    if any(is_control(e) and e["law"] == law for e in entries):
        return "stale (its entries are at another hash of the law's cone)"
    return "no entry"


def controls_in(paths):
    """The control entries of the stores of `paths` (a file without a store has none)."""
    return [e for p in paths for e in read_store(p) if is_control(e)]


def control_standings(path):
    """Per law a control line of the file names: its control's standing from the store."""
    from .tester import law_cones
    entries = read_store(path)
    return [(law, control_standing(entries, law, current)) for law, current in law_cones(path, control=True)]


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
    return all(h in drawn.get(p, "").split(",") for p, h in demand.get("fingerprints", {}).items()
               if covers_all(entry["reach"], [(p, given[p])]))


def serves(demand, entry):
    """certification_model's `serves`: the law's entry at the current hash, passed, at or above the
    grade the demand accepts, its reach covering what the run gives."""
    return (entry["law"] == demand["law"] and at(demand, entry) and passed(entry)
            and entry["grade"] is not None and GRADE_RANK[demand["accepts"]] <= GRADE_RANK[entry["grade"]]
            and covers_all(entry["reach"], demand["given"]))


def state_of(demand, entries):
    """certification_model's `stateOf`: ("Current", the outcome of the latest entry at the current
    hash), else ("Stale", the hash of the law's latest entry), else ("Uncertified", None). Controls
    aside."""
    entries = _laws_own(entries)
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
    with its state (`RefusalSaysWhy`, `RefusalIsPerLaw`, `ProvisionalIsRefused`). A law with a
    failure at the demand's hash (`at`) is refused whatever serves, listed with that failure
    (certification_model's `refuseLaws` at 82c4cb4, `ACurrentFailureIsRefused`, C5 of the layer 3
    review: record/IA/layer-3-review-2026-10-15/report-fix-certification.md)."""
    refusals = []
    for c in cone:
        if c["provisional"]:
            refusals.append({"name": c["name"], "law": None, "state": ("Provisional", None)})
            continue
        for d in c["laws"]:
            failure = next((e for e in _laws_own(entries) if e["law"] == d["law"] and at(d, e) and _failed(e)),
                           None)
            if failure is not None:
                refusals.append({"name": c["name"], "law": d["law"], "state": ("Current", failure["outcome"]),
                                 "demand": d})
            elif not any(serves(d, e) for e in entries):
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

def certify_file(path, seed=None, deep=False, fuel=1_000_000, store=True):
    """Run one file's test lines, writing its store (reading and writing none without `store`); per
    law its certificate's grade (the weakest across bindings) and the hash of its cone, the entries
    of its control lines, with the counts of lines run and known. Runs in its own process."""
    from .tester import run_tests
    try:
        outcomes = run_tests(path, seed, fuel, deep=deep, store=store)
        entries = read_store(path) if store else [o.entry for o in reversed(outcomes) if o.entry is not None]
    except Exception as exc:  # the file's failure is reported with the file, the others go on
        return {"path": str(path), "error": f"{type(exc).__name__}: {exc}"}
    laws = {}
    for o in outcomes:
        if not o.spec.control:
            laws.setdefault(o.spec.law, o.cone)
    # each control line with its own entry's outcome (the run's, or the store's when known)
    controls = [(o.spec.law, ", ".join(d["generator"] for d in o.entry["binding"]), show_outcome(o.entry["outcome"]))
                for o in outcomes if o.spec.control and o.entry is not None]
    return {"path": str(path),
            "laws": [(law, cone, standing(entries, law, cone)) for law, cone in laws.items()],
            "controls": controls,
            "control entries": [e for e in entries if is_control(e)],
            "ran": sum(1 for o in outcomes if o.known is None),
            "known": sum(1 for o in outcomes if o.known is not None),
            "graded": all(certificate_grade(entries, law, cone) is not None for law, cone in laws.items())}


def certify(paths, jobs=1, seed=None, deep=False, fuel=1_000_000, out=print, store=True):
    """`luthier certify`: each file in its own process, `jobs` at a time; prints per file its laws,
    their grades and their control status, read from the control lines of every file given
    (7.S19, L9.14), and its control lines. True when every law of every file has a grade and no
    control failed."""
    from concurrent.futures import ProcessPoolExecutor
    import multiprocessing
    context = multiprocessing.get_context("spawn")
    ok = True
    with ProcessPoolExecutor(max_workers=max(1, jobs), mp_context=context, max_tasks_per_child=1) as pool:
        futures = [pool.submit(certify_file, str(p), seed, deep, fuel, store) for p in paths]
        results = [future.result() for future in futures]
    controls = [e for r in results for e in r.get("control entries", [])]
    for result in results:
        if "error" in result:
            out(f"{result['path']}: {result['error']}")
            ok = False
            continue
        counted = f", {len(result['controls'])} controls" if result["controls"] else ""
        out(f"{result['path']}: {len(result['laws'])} laws{counted}, {result['ran']} lines ran, "
            f"{result['known']} known")
        for law, cone, s in result["laws"]:
            status = control_status(controls, law, cone)
            ok &= not status.startswith("CONTROL FAILED")
            out(f"  {law}: {s}; {status}")
        for law, on, s in result["controls"]:
            ok &= not s.startswith("CONTROL FAILED")
            out(f"  control of {law} on {on}: {s}")
        ok &= result["graded"]
    return ok
