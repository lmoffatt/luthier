"""Certificates: the hash of a cone, the store of entries `x.cert.json`, and `luthier certify`.

Sources: src/luthier/lib/certification.lth (§1 the entry and the store, §2 the certificate, §4 the
hash of a cone) and its model certification_model.lut; spec 6.S8, 7.S9, 7.S13, 12.S11, 12.S16;
term.lth §4 through kernel.canonical. Derivation: record/IA/certification-2026-10-14/
prompt-certify.md (step 5.3 of the plan from zero), by a Claude agent of the coordinating session,
2026-10-14. What the theory left open is marked [proposed] where it is chosen.

The cone of a name is every definition of the runtime program the name reaches (its type and its
body, the data of each constructor it names), each in canonical form: binders renamed by
kernel.canonical, module prefixes and the `@file` tag the loader gives a clashing name not seen,
an extern by its route only, and the type annotation of each `Lam` and `Let` erased (`erase`,
D-2026-10-15-e: the hash is the strict level of equality, and an annotation the elaborator writes
changes nothing the term does). With it go the host code behind each extern of the cone, by route,
and the interpreter's revision. `cone_hash` is certification.lth §4's `ConeHashing.hash`, the
route `python:luthier.certify.cone_hash` certification_model.lut names; `Cones` builds the cone of
a name from a program.

The store `x.cert.json` beside `x.lut` is a JSON list of entries, the latest in front, each as
certification.lth's `Entry` reads them. Its predicate (`Store`: a grade exactly when passed) is
checked on every store read or written; `record` (the store law, certification.lth's `Recording`)
never edits an entry. [D-2026-10-15-f] An exact replay that agrees with the latest entry of its
identity leaves the store as it is; one that disagrees is written in front of it, both kept, and
the law is refused (`disputes`: no grade, `refuse` and `standing` say "replay disagrees", naming
both entries) until a later run agrees with the latest (a later agreeing pair) or one of the two is
removed from the store by hand. [proposed] A failure among them still refutes the law after a later
agreeing pair (6.S3, L10.3): only its removal by hand lifts that. [D-2026-10-15-g] A not-run for lack of fuel (`out_of_fuel`) is
never written, so the next run of the line runs it again; the fuel given is in no identity. A stale
entry is kept, and is stale only as read against the current hash of its law's cone (12.S11), never
marked in the file. [D-2026-10-16-b,
L10.12] The stores are partitioned by the files that make the claims: an entry lives only in the
store of the file that defines the model of the library its binding names, or else of the file
that states its law (tester.py's `claim_file`); a test program keeps none, and `certify` and
`check -v` read the stores of its lines' claims (`read_stores`), never one beside it.

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
the law's cone, which names the law; the controls read are those in the stores of the claims of
the files `certify` or `check -v` is given (a control lives beside the claim it controls), so a law
certified without its control file is reported uncontrolled.

Statistical laws (record/IA/statistical-2026-10-15/prompt-tester.md; laws.lth §4, 7.S17, L9.15): an
entry whose evidence is `Tested` holds the sequential test's verdict with alpha, beta, delta, the
samples spent, and the cutoffs' `initial` and `budget` (`tested_text` reads them). A pass is graded
as any (sampled, over `Drawn seed`); `standing` adds the rates and what was spent to the grade, so
that the certificate shows the price of a sampled grade (7.S17). An unresolved test is a
`Unresolved` outcome carrying the test's record (older stores wrote `NotRunFor "unresolved at ..."`, still read).

The union of a law's stretches (record/IA/code-follows-2026-10-16/prompt-pool-seeds.md; D-2026-10-16-g,
L10.3; certification.lth's `pooledCases` and `Pooling`): a stretch is one run of a law under one binding
and one seed. The grade is the fold of §2, unchanged; `pooled` counts the union under a binding, each
seed once at its largest `n` (a replay is no new stretch), the passes and, for a statistical law, the
stretches it left unresolved; a run over every value or a census is one stretch whatever its seed.
`standing` adds the union when it holds two stretches or more. A statistical stretch records the ratio
it stopped at (`"ratio"` in its evidence), the parameter of its cutoffs (`"cutoffs"`) and, when it
continued earlier stretches, where it started (`"from"`: their ratio, samples and seeds); its `spent`
is its own samples. The budget is the demand's for the whole test, so a statistical stretch's union
key is its binding without its cutoffs' drawing (`union_key`): stretches run under two budgets are one
test. `continuation` is where the next one starts (tester.py).
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


# [D-2026-10-15-e] what an erased binder annotation becomes in the hash
ERASED = t.Hole("erased")


def erase(x):
    """certification.lth's `eraseBinders`: the term with the type annotation of each `Lam` and each
    `Let` replaced by `ERASED`, everywhere in it (a type's `Pi`, `Sigma`, `Subtype` and record fields
    are kept: they are types, read by the tester and the bridge, and no annotation of a binder). The
    elaborator writes those annotations (from a parameter's written type, from the expected type, or
    inferred for a `Let`) and no step of the kernel or of the Runner reads them, so the hash, the
    strict level of equality, does not see them (D-2026-10-15-e). The condition, that no erased
    annotation changes what the term does, is the law `ErasureKeepsTheStep` (certification.lth §4)
    and tests/test_certify.py's step-by-step check of the library's code."""
    if isinstance(x, t.Lam):
        return t.Lam(x.name, ERASED, erase(x.body))
    if isinstance(x, t.Let):
        return t.Let(x.name, ERASED, erase(x.value), erase(x.body))
    if isinstance(x, (str, t.Lit, t.Primitive, t.Axiom, t.Extern)):
        return x
    if isinstance(x, tuple):
        return tuple(erase(y) for y in x)
    if is_dataclass(x) and not isinstance(x, type):
        return replace(x, **{f.name: erase(getattr(x, f.name)) for f in fields(x) if f.init})
    return x


def canon(term):
    """term.lth §4's canonical form as the hash reads it: `kernel.canonical` (binders renamed in
    preorder, free names unqualified) of the term without file tags and with its binders'
    annotations erased (`erase`, D-2026-10-15-e)."""
    return kernel.canonical(erase(_plain(term)))


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

    @staticmethod
    def _predicate_reads(ty, bound=frozenset()):
        """Refinement predicates are values even inside a type (P10)."""
        if isinstance(ty, t.Subtype):
            return (set(kernel.free_names(erase(ty.predicate))) - bound - {ty.name}
                    | Cones._predicate_reads(ty.type, bound))
        if isinstance(ty, (t.Pi, t.Sigma)):
            return (Cones._predicate_reads(ty.domain, bound)
                    | Cones._predicate_reads(ty.codomain, bound | {ty.name}))
        if isinstance(ty, t.Lam):
            return Cones._predicate_reads(ty.body, bound | {ty.name})
        if isinstance(ty, tuple):
            return set().union(*(Cones._predicate_reads(x, bound) for x in ty))
        if is_dataclass(ty) and not isinstance(ty, type):
            return set().union(*(Cones._predicate_reads(getattr(ty, f.name), bound) for f in fields(ty)))
        return set()

    def _part(self, name, bodies=True):
        """One name's code, type references, value references and routes.

        A theory used as a type denotes its declared record. Its predicate definition belongs
        to a value dependency, not to every model's runtime cone (bite 6).
        """
        key = (name, bodies)
        if key not in self.memo:
            code, types, values, routes = [], set(), set(), set()
            for act in self.acts.get(name, ()):
                if not bodies and isinstance(act, t.Define):
                    continue
                term = t.Pair(act.type, act.body) if isinstance(act, t.Define) else act.type
                result = act.type
                while isinstance(result, t.Pi):
                    result = result.codomain
                body_type = isinstance(result, t.Universe)
                values.update(self._predicate_reads(act.type) & set(kernel.free_names(act.type)))
                if isinstance(act, t.Define) and body_type:
                    values.update(self._predicate_reads(erase(act.body)) & set(kernel.free_names(erase(act.body))))
                for value, refs in [(act.type, types)] + ([(erase(act.body), types if body_type else values)] if isinstance(act, t.Define) else []):
                    out = {"constructors": set(), "routes": set()}
                    _walk(value, out)
                    refs.update(kernel.free_names(value))
                    refs.update(out["constructors"])
                    routes.update(out["routes"])
                code.append((name.partition("@")[0], canon(term)))
            self.memo[key] = (code, types, values, routes)
        return self.memo[key]

    def _reach(self, name):
        def record(ty):
            while isinstance(ty, t.Pi):
                ty = ty.codomain
            return isinstance(ty, t.Record)
        theories = {n for n, acts in self.acts.items()
                    if any(isinstance(a, t.Declare) and record(a.type) for a in acts)}
        seen, pending = {}, [(name, True)]
        while pending:
            n, bodies = pending.pop()
            if n not in self.acts or n in seen and (seen[n] or not bodies):
                continue
            seen[n] = bodies
            _, types, values, _ = self._part(n, bodies)
            for refs, term_position in ((types, False), (values, True)):
                for ref in refs:
                    for target in (ref, self.owner.get(ref)):
                        if target is not None:
                            pending.append((target, term_position or target not in theories))
        return seen

    def names(self, name):
        """The names reached by the value and type dependencies of `name` (12.S22)."""
        return set(self._reach(name))

    def cone(self, name):
        """The code by name, retaining a theory's predicate only when used as a value."""
        code, routes = [], set()
        for n, bodies in self._reach(name).items():
            c, _, _, r = self._part(n, bodies)
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

LIBRARY = Path(__file__).resolve().parent / "lib"
LIBRARY_STORES = "LUTHIER_LIBRARY_STORES"


def store_path(path):
    """`x.cert.json` beside `x.lut` (12.S10). [proposed, 2026-10-15, record/IA/controls-2026-10-15/
    prompt-tail.md] When the environment names a directory in `LUTHIER_LIBRARY_STORES`, the store
    of a file of the library (src/luthier/lib) is that directory's of the same name: the test suite
    reads and writes a copy of the library's stores there (tests/conftest.py), so that a run of it
    beside `luthier certify` neither reverts nor sees what certify writes. A file under a directory
    of the library (lib/core/core.lut, the core's bite 1) keeps its path under lib/ there."""
    path = Path(path)
    where = path.with_name(path.stem + ".cert.json")
    elsewhere = os.environ.get(LIBRARY_STORES)
    if elsewhere and where.parent.resolve().is_relative_to(LIBRARY):
        return Path(elsewhere) / where.parent.resolve().relative_to(LIBRARY) / where.name
    return where


IDENTITY = ("law", "cone", "binding", "seed", "cases")
CONTROL = "Control"  # the kind of a control's entry (tester.py); a law's entry has no kind
# [proposed] the kind of an entry a run writes when it validates a host action at its first
# application (run.py's `FirstActions`, 10.S10), and of the demand that action makes: such a demand
# is served only by such an entry, never by a tester's listed cases (report-e.md, finding 2)
FIRST_ACTION = "FirstAction"


def entry_kind(entry):
    """The entry's kind: `Control`, `FirstAction`, or None for a law's entry from a test line. An
    entry a first action wrote before the kind existed is read by its evidence's protocol."""
    if "kind" in entry:
        return entry["kind"]
    evidence = entry.get("evidence")
    if isinstance(evidence, dict) and evidence.get("protocol") == "first action (10.S10)":
        return FIRST_ACTION
    return None


def is_control(entry):
    return entry.get("kind") == CONTROL


def _laws_own(entries):
    """The entries that are the law's evidence: every entry but the controls."""
    return [e for e in entries if not is_control(e)]


# [bite 13c, the coordinator's reading of D-2026-10-16-g; spec 7.S8] The budgets of 7.S8 by what they
# change. A field that changes what is drawn, which cases are checked or what the regions read is
# part of the sampling (`sampling`), so of the identity and of the union a stretch pools into: the
# masses of the special values and of the atom at 0, the product above which a covering array
# chooses the cases, the counts of runs, seeds and draws that size a level, a control's power or a
# generator's distribution, and the classifier's two bounds. A field that only cuts a run stays out
# (D-2026-10-15-g): the fuel, the tries of a filter (a value found within fewer tries is the same
# value), the redraws, the probes and the draws per case.
SAMPLING = ("specialMass", "atomAtZero", "coveringAbove", "levelRuns", "seedsPerControl", "distributionDraws",
            "regionNumbers", "regionEntries")
LIMITS = ("fuel", "tries", "redraws", "probes", "drawsPerCase")


def sampling(entry):
    """The budgets of the entry that change what it samples (`SAMPLING`); None when it records no
    budgets (a first action's entry)."""
    budgets = entry.get("budgets")
    if not isinstance(budgets, dict):
        return None
    return {k: budgets[k] for k in SAMPLING if k in budgets}


def identity(entry):
    """certification.lth's `identity`: the law, the cone's hash, the binding expanded, the seed and
    `n` (7.S9, 7.S13), as one comparable key; a control's kind is part of it [proposed], and the
    conjunct of a conjunction's entry (tester.py's `_run_conjunction`, D-2026-10-18-f). A field an
    entry lacks reads as null (`store_errors` reports it in a store; a demand's reading may hold
    entries built in part). [bite 13c] And the budgets that change what is sampled (`sampling`):
    two runs of one seed under another mass of special values are two samples, not a replay."""
    key = [entry.get(k) for k in IDENTITY] + ([entry["kind"]] if "kind" in entry else [])
    if "conjunct" in entry:
        key.append({"conjunct": entry["conjunct"]})
    if sampling(entry) is not None:
        key.append({"sampling": sampling(entry)})
    return json.dumps(key, sort_keys=True, ensure_ascii=False)


def passed(entry):
    return entry["outcome"] == "Passed"


# certification.lth's `fuelSpent`: the reason of a not-run cut by its fuel, never written to a store
FUEL_SPENT = "fuel spent"


def out_of_fuel(entry):
    """certification.lth's `outOfFuel`: the entry's outcome is `NotRunFor fuelSpent`."""
    return entry.get("outcome") == {"NotRunFor": FUEL_SPENT}


def agree(e, f):
    """certification.lth's `agree`: the same outcome and the same grade."""
    return e["outcome"] == f["outcome"] and e.get("grade") == f.get("grade")


def disputes(entries):
    """certification.lth's `disputes`: for each identity, in the store's order, its latest entry
    and the one of the same identity behind it, when the two disagree (D-2026-10-15-f)."""
    latest, found = {}, []
    for e in entries:
        i = identity(e)
        if i not in latest:
            latest[i] = e
        elif latest[i] is not None:
            if not agree(latest[i], e):
                found.append((latest[i], e))
            latest[i] = None  # the latest two are read
    return found


def disputed_at(entries, key):
    """certification.lth's `disputedAt`: whether the latest two entries of the identity disagree."""
    two = [e for e in entries if identity(e) == key][:2]
    return len(two) == 2 and not agree(*two)


def dispute_of(entries, law, here):
    """certification.lth's `disputeAt`: the first disagreement among the law's own entries (no
    control) for which `here` holds (at the current hash, or at a demand's), or None."""
    return next(iter(disputes([e for e in _laws_own(entries) if e["law"] == law and here(e)])), None)


def show_entry(entry):
    """An entry as a disagreement names it: its date and its outcome, with its grade."""
    grade = f", {GRADE_WORDS[entry['grade']]}" if entry.get("grade") in GRADE_WORDS else ""
    return f"the entry of {entry.get('date', '?')} ({show_outcome(entry['outcome'])}{grade})"


def show_dispute(latest, before):
    """The words of a disagreement in `standing`, `show_refusal` and a test line."""
    return (f"replay disagrees at seed {latest['seed']}, n {latest['cases']}: {show_entry(latest)} and "
            f"{show_entry(before)}; refused until a later run agrees with the latest or one is removed by hand "
            f"(D-2026-10-15-f)")


def _failed(entry):
    """certification.lth's `isFailure`: the outcome is `Failed` (not `NotRunFor`)."""
    return isinstance(entry["outcome"], dict) and "Failed" in entry["outcome"]


# certification.lth's `admits` over the coverage of `Points` (test.lth's `grade` of a confirming or a
# supporting verdict): the grades each coverage admits, `None` for evidence with no coverage
ADMITTED = {"Exhaustive": {"ExhaustiveGrade", "Cases"}, "Bounded": {"ExhaustiveGrade"}, "Listed": {"Cases"},
            "Drawn": {"Cases", "Sampled"}, None: {"Cases"}}


def _coverage(evidence):
    """The constructor of the coverage of a `Points` evidence (`Drawn 3` is `Drawn`), else None."""
    points = evidence.get("Points") if isinstance(evidence, dict) else None
    coverage = points.get("coverage") if isinstance(points, dict) else None
    return coverage.strip("()").split(" ", 1)[0] if isinstance(coverage, str) else None


def admits(evidence, grade):
    """certification.lth's `admits`: the grades a pass's evidence admits. A citation proved, an
    assumption assumed, a not-run none, a statistical pass a `Holds` graded sampled, and points
    the grades their coverage admits (`ADMITTED`)."""
    if isinstance(evidence, dict):
        if "Cited" in evidence:
            return grade == "Proved"
        if "Assumed" in evidence:
            return grade == "AssumedGrade"
        if "NotRun" in evidence:
            return False
        if "Tested" in evidence:
            return evidence["Tested"].get("verdict") == "Holds" and grade == "Sampled"
    elif evidence == "Assumed":
        return grade == "AssumedGrade"
    return grade in ADMITTED[_coverage(evidence)]


def held_as_listed(entry):
    """certification.lth's `censusOfAtMost` for a pass over listed cases: each parameter reaches a
    census of no more values than the cases evaluated (6.S7). [proposed, bite 13c] Two readings the
    theory's text does not state yet, both met by what the tester writes: a parameter enumerated
    whole (`ExhaustiveMode`) reaches its support, and a pass that evaluated no case (a domain with
    an empty parameter, `x : Empty`) bounds no census by its count."""
    points = entry["evidence"]["Points"]
    n = points.get("evaluated")
    whole = {b["parameter"] for b in entry["binding"]
             if isinstance(b, dict) and str(b.get("generator", "")).startswith("ExhaustiveMode")}
    for r in entry.get("reach") or ():
        reach = r["reach"]
        if reach == "Support" and r["parameter"] in whole:
            continue
        if not (isinstance(reach, dict) and "Members" in reach):
            return False
        if n and len(reach["Members"]) > n:
            return False
    return True


def store_errors(entries):
    """What breaks `Store`'s predicate: a grade without a pass or a pass without a grade
    (`gradedAsOutcome`); a grade the pass's evidence does not admit, or a pass over listed cases
    whose reach is more than the cases it evaluated (`heldAsRun`, `admits`, `held_as_listed`; bite
    13c, on the audit of 2026-10-22, 1.8). Two entries of one identity that disagree are a
    disagreement the store records (D-2026-10-15-f), read by `disputes`, not an error of the store.
    [proposed] `latestInFront` stays unchecked here, as in the theory, whose `notBefore` is a hole."""
    errors = []
    for k, e in enumerate(entries):
        missing = [f for f in IDENTITY + ("outcome", "grade") if f not in e]
        if missing:
            errors.append(f"entry {k} lacks {', '.join(missing)}")
            continue
        if passed(e) != (e["grade"] is not None):
            errors.append(f"entry {k} ({e['law']}): a grade exactly when passed")
            continue
        if e["grade"] is None:
            continue
        if e["grade"] not in GRADE_RANK:
            errors.append(f"entry {k} ({e['law']}): no grade {e['grade']!r}")
        elif _tested(e) and not admits(e.get("evidence"), e["grade"]):
            errors.append(f"entry {k} ({e['law']}): a statistical pass is a Holds graded sampled")
        elif not admits(e.get("evidence"), e["grade"]):
            errors.append(f"entry {k} ({e['law']}): its evidence does not admit the grade {e['grade']}")
        elif _coverage(e.get("evidence")) == "Listed" and not held_as_listed(e):
            errors.append(f"entry {k} ({e['law']}): a pass over listed cases reaches more than its cases")
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


def read_stores(paths):
    """The entries of the stores of `paths` (each read once), the latest in front across them, as a
    run reads the stores of its files."""
    entries = [e for p in dict.fromkeys(Path(p) for p in paths) for e in read_store(p)]
    return sorted(entries, key=lambda e: e.get("date", ""), reverse=True)


def write_store(path, entries):
    errors = store_errors(entries)
    if errors:
        raise StoreError(f"{store_path(path)}: " + "; ".join(errors))
    where = store_path(path)
    where.parent.mkdir(parents=True, exist_ok=True)  # a directory of the library in the suite's copy
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
    if "conjunct" in entry:
        key.append({"conjunct": entry["conjunct"]})
    return json.dumps(key, sort_keys=True, ensure_ascii=False)


def _stamp(entry):
    """What makes an entry current: its cone's hash and the fingerprints of its binding."""
    binding = entry["binding"]
    prints = [d.get("fingerprint") for d in binding if isinstance(d, dict)] if isinstance(binding, list) else []
    return json.dumps([entry["cone"], prints])


def _negative(entry):
    """Evidence no later pass undoes: a failure (`isFailure`), or a control whose broken model held."""
    return _failed(entry) or (isinstance(entry["outcome"], dict) and "ControlConfirmed" in entry["outcome"])


def prune(entries, current=None, keep=KEEP):
    """The store bounded [proposed, 6.S8 "up to four" and 12.S11]: per (law, binding without
    fingerprints), the `keep` most recent entries at the current cone hash and fingerprints (by date,
    the store's order breaking ties), and no stale entry once a current one exists; a group with no
    current entry keeps its most recent entry only. A current failure or confirmed control, and the
    two entries of a current disagreement, stay beyond the `keep` (bite 13c: pruning preserves
    refusal and unresolved conflict, 6.S15). `current` maps a group's key to a `_stamp`, and a
    group not in it takes the stamp of its most recent entry. What stays keeps the store's order
    (latest in front)."""
    current = dict(current or {})
    order = sorted(range(len(entries)), key=lambda k: (entries[k].get("date", ""), -k), reverse=True)
    # [D-2026-10-15-f] the two entries of a disagreement at the current stamp stay until it is resolved
    disputing = {id(e) for pair in disputes(entries) for e in pair}
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
            # [bite 13c, audit 1.4 A] a current refutation stays too: a failure refuses the law
            # whatever passes follow (6.S15), and a confirmed control fails the law's control
            dropped.update(k for k in at[keep:] if id(entries[k]) not in disputing and not _negative(entries[k]))
            dropped.update(k for k in ks if _stamp(entries[k]) != stamp)
        else:
            dropped.update(ks[1:])
    return [e for k, e in enumerate(entries) if k not in dropped]


def record(entries, entry):
    """certification.lth's `recordEntry`, the store law `Recording`: a new identity in front; an
    exact replay that agrees with the latest entry of its identity, where no disagreement stands,
    leaves the store as it is (6.S15); one that disagrees, or that agrees with the latest of an
    identity in disagreement, goes in front (D-2026-10-15-f); a not-run for lack of fuel is never
    written (D-2026-10-15-g). The entry's (law, binding) is then pruned at its cone hash (`prune`)."""
    if out_of_fuel(entry):
        return entries
    key = identity(entry)
    found = known(entries, key)
    # [proposed, 3j j2a] an agreeing replay whose regions differ from the known entry's (written before
    # the regions were kept, D-2026-10-16-i, or classified by an earlier reading of them) records that
    # evidence: it goes in front, and the regions of an identity are its latest entry's (`law_regions`)
    new_regions = "regions" in entry and entry["regions"] != found.get("regions") if found is not None else False
    if found is not None and agree(entry, found) and not disputed_at(entries, key) and not new_regions:
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
    where.parent.mkdir(parents=True, exist_ok=True)
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


def _or_weakest(m, n):
    """certification.lth's `orWeakest`: the weaker of two grades, `None` (no grade) the unit."""
    if m is None:
        return n
    if n is None:
        return m
    return m if GRADE_RANK[m] <= GRADE_RANK[n] else n


def _or_strongest(m, n):
    """certification.lth's `orStrongest`: the stronger of two grades, `None` the unit."""
    if m is None:
        return n
    if n is None:
        return m
    return m if GRADE_RANK[m] >= GRADE_RANK[n] else n


# The combinations of the grades over regions and bindings a demand may choose (5.S8,
# D-2026-10-16-i), by the name `Demand.combine` gives; the weakest by default (certification_model's
# `regioning`). [proposed] The two the theory states, `orWeakest` and `orStrongest`.
COMBINATIONS = {"weakest": _or_weakest, "strongest": _or_strongest}
COMBINATION = "weakest"


def grades(region):
    """certification.lth's `grades`: a region enters the grade unless it is a label."""
    return region.get("source") != "Label"


def _key(region):
    return (region["source"], region["name"])


def law_regions(entries):
    """The grading regions the entries recorded (7.S9), each once in the order first recorded: the
    law's regions, `rs` of certification.lth's `regionedGrade`. Entries written before the regions
    were kept recorded none. Of the entries of one identity only the latest is read (`known`): a
    replay that classified its cases again replaces what the earlier one recorded."""
    found, seen = {}, set()
    for e in entries:
        i = identity(e)
        if i in seen:
            continue
        seen.add(i)
        for r in e.get("regions") or ():
            if grades(r["region"]):
                found.setdefault(_key(r["region"]), r["region"])
    return list(found.values())


def binding_evidence(entries, law, current, binding):
    """certification.lth's `casesAt` for one binding: per region, the cases of the passes under it at
    the current hash, each stretch once (`stretches`: a seed at its largest `n`)."""
    counts = {}
    key = binding if isinstance(binding, list) else None
    for e in _laws_own(entries):
        if e["law"] == law and e["cone"] == current and e["binding"] == binding:
            key = union_key(e)
            break
    if key is None:
        return counts
    for _, e in stretches(entries, law, current, key).values():
        if e["binding"] != binding:
            continue
        for r in e.get("regions") or ():
            counts[_key(r["region"])] = counts.get(_key(r["region"]), 0) + int(r["n"])
    return counts


def _capped(g):
    """certification.lth's `capped`: at most sampled."""
    return None if g is None else _or_weakest(g, "Sampled")


def regioned(entries, law, current, binding, base, combine=COMBINATION):
    """certification.lth's `overRegions`: the binding's grade `base` combined over the law's regions,
    each the binding's grade where it has cases under the binding and at most sampled where it has
    none (`regionGrade`); with no region, `base`. With the empty regions that capped it."""
    comb = COMBINATIONS[combine]
    rs = law_regions([e for e in _laws_own(entries) if e["law"] == law and e["cone"] == current])
    if not rs:  # `NoRegionsLeaveTheGrade`, and no stretch is read (a demand's entries may be built in part)
        return base, []
    counts = binding_evidence(entries, law, current, binding)
    g, empty = base, []
    for r in reversed(rs):
        if counts.get(_key(r), 0):
            g = comb(base, g)
        else:
            g = comb(_capped(base), g)
            empty.insert(0, r["name"])
    return g, empty


def certificate_grade(entries, law, current, combine=COMBINATION):
    """certification_model's `grade` read over the regions (certification.lth's `regionedGrade`,
    D-2026-10-16-i): over the law's entries at the current hash, none when one failed or none passed
    (or a disagreement stands); under one binding the strongest pass, combined over the law's regions
    (`regioned`), and across bindings with the same combination, the demand's (5.S8), the weakest by
    default. A law whose entries recorded no regions keeps the grade of the fold before regions."""
    return certificate_grade_and_empty(entries, law, current, combine)[0]


def certificate_grade_and_empty(entries, law, current, combine=COMBINATION):
    """`certificate_grade` with the empty regions of each binding whose grade they lowered. A law
    whose body is a conjunction of laws has an entry per conjunct (tester.py's `_run_conjunction`,
    D-2026-10-18-f): its grade is the demand's combination (5.S8) of its conjuncts' grades, each read
    as a law's over its own entries, and none while a conjunct its entries list has none."""
    counts = [e for e in _laws_own(entries) if e["law"] == law and e["cone"] == current]
    conjuncts = list(dict.fromkeys(c for e in counts for c in e.get("conjuncts") or ()))
    if not conjuncts:
        return _grade_and_empty(entries, law, current, combine)
    comb, grade, lowered = COMBINATIONS[combine], None, []
    for c in conjuncts:
        g, empty = _grade_and_empty([e for e in counts if e.get("conjunct") == c], law, current, combine)
        if g is None:
            return None, []
        grade = comb(g, grade)
        lowered += [n for n in empty if n not in lowered]
    return grade, lowered


def _grade_and_empty(entries, law, current, combine=COMBINATION):
    """`certificate_grade_and_empty` over the entries of one law or one conjunct."""
    counts = [e for e in _laws_own(entries) if e["law"] == law and e["cone"] == current]
    if any(isinstance(e["outcome"], dict) and "Failed" in e["outcome"] for e in counts) or disputes(counts):
        return None, []
    best, bindings = {}, {}
    for e in counts:
        if passed(e) and e["grade"] is not None:
            b = json.dumps(e["binding"], sort_keys=True)
            g = e["grade"]
            bindings.setdefault(b, e["binding"])
            if b not in best or GRADE_RANK[g] > GRADE_RANK[best[b]]:
                best[b] = g
    if not best:
        return None, []
    comb, grade, lowered = COMBINATIONS[combine], None, []
    for b, g in best.items():
        h, empty = regioned(entries, law, current, bindings[b], g, combine)
        if GRADE_RANK[h] < GRADE_RANK[g]:
            lowered += [n for n in empty if n not in lowered]
        grade = comb(h, grade)
    return grade, lowered


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


# ---------------------------------------------------------------------- the union of the stretches

def _drawn(entry):
    """certification.lth's `drawnStretch`: the cases are a sample of the seed (a statistical test, or
    points over `Drawn`), so another seed is another sample."""
    evidence = entry.get("evidence")
    if not isinstance(evidence, dict):
        return False
    if "Tested" in evidence:
        return True
    coverage = (evidence.get("Points") or {}).get("coverage")
    return isinstance(coverage, str) and coverage.lstrip("(").startswith("Drawn")


def _in_union(entry):
    """certification.lth's `inTheUnion`: a pass, or a statistical stretch left unresolved."""
    return passed(entry) or (isinstance(entry["outcome"], dict) and "Unresolved" in entry["outcome"])


def stretch_size(entry):
    """certification.lth's `stretchSize`: the samples a statistical stretch spent, else its `n`."""
    tested = _tested(entry)
    return tested["spent"] if tested else entry["cases"]


def union_key(entry):
    """The binding a stretch is pooled under: its binding, without the drawing of a statistical
    stretch's cutoffs (the parameter its evidence names), whose budget is the demand's for the whole
    test and not part of the distribution (D-2026-10-16-g, D-2026-10-15-b). [bite 13c] With the budgets
    that change the distribution (`sampling`), the last element: one union is one distribution."""
    evidence = entry.get("evidence")
    cutoffs = evidence.get("cutoffs") if isinstance(evidence, dict) else None
    return _without(entry, cutoffs)


def _without(entry, parameter):
    """The entry's binding without the drawing of `parameter`, with its `sampling` last."""
    key = [d for d in entry["binding"] if not (isinstance(d, dict) and d.get("parameter") == parameter)]
    return key + ([{"sampling": sampling(entry)}] if sampling(entry) is not None else [])


def stretches(entries, law, current, key):
    """certification.lth's `stretchesUnder`, each seed once at its largest: {seed (None when not
    drawn): (n, entry)} of the law's own entries at the current hash whose `union_key` is `key` (an
    exact law's: its binding) (D-2026-10-16-g)."""
    found = {}
    for e in _laws_own(entries):
        if e["law"] == law and e["cone"] == current and union_key(e) == key and _in_union(e):
            seed, n = (e["seed"] if _drawn(e) else None), stretch_size(e)
            if seed not in found or n > found[seed][0]:
                found[seed] = (n, e)
    return found


def pooled(entries, law, current, key):
    """certification.lth's `pooledCases`, the specimen of `Pooling`: the size of the union of the
    law's stretches under the key (`union_key`), a replay counted once."""
    return sum(n for n, _ in stretches(entries, law, current, key).values())


def pools(entries, law, current):
    """Per binding of the law at the current hash whose union holds two stretches or more, the words
    of the union: its seeds and its total."""
    words, seen = [], []
    for e in _laws_own(entries):
        if e["law"] == law and e["cone"] == current and union_key(e) not in seen:
            seen.append(union_key(e))
            union = stretches(entries, law, current, union_key(e))
            if len(union) > 1:
                seeds = ", ".join(str(k) for k in sorted(k for k in union if k is not None))
                unit = "samples" if any(_tested(f) for _, f in union.values()) else "cases"
                words.append(f"pooled over seeds {seeds}: {sum(n for n, _ in union.values())} {unit} in all")
    return words


CUTOFFS = ("alpha", "beta", "delta", "initial")  # one test: the same rates and sample size; the budget aside


def continuation(entries, entry, cutoffs, parameter):
    """Where a statistical stretch starts (laws.lth's `ratioAfter`, D-2026-10-16-g), among the
    stretches of its law, cone, kind and union key (its binding without the drawing of `parameter`,
    its cutoffs) run at the same alpha, beta, delta and sample size, whatever their budget: where a
    stretch of its own seed started (a replay, or the same seed under another budget, which draws
    the same stream further), its `"from"`, None when it started the test; else from the latest
    stretch, with the samples and seeds of the test so far; None when there is none. The budget
    bounds the whole test (`cutoffs["budget"]` against the samples so far), so a new seed buys none."""
    key = _without(entry, parameter)
    same = []
    for e in entries:
        evidence = e.get("evidence")
        if (e["law"] == entry["law"] and e["cone"] == entry["cone"] and e.get("kind") == entry.get("kind")
                and isinstance(evidence, dict) and "ratio" in evidence and "Tested" in evidence
                and union_key(e) == key
                and all(evidence["Tested"].get(c) == cutoffs.get(c) for c in CUTOFFS)):
            same.append(e)
    own = next((e for e in same if e["seed"] == entry["seed"]), None)
    if own is not None:
        return own["evidence"].get("from")
    if not same:
        return None
    last = same[0]
    before = last["evidence"].get("from") or {"ratio": 1.0, "spent": 0, "seeds": []}
    return {"ratio": last["evidence"]["ratio"], "spent": before["spent"] + last["evidence"]["Tested"]["spent"],
            "seeds": before["seeds"] + [last["seed"]]}


def continued_text(start, spent):
    """A continued stretch as a line says it: the seeds it continues and the samples in all."""
    seeds = ", ".join(str(k) for k in start["seeds"])
    return f"continuing the test of seed{'s' if len(start['seeds']) > 1 else ''} {seeds} ({start['spent'] + spent} samples in all)"


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
    dispute = dispute_of(entries, law, lambda e: e["cone"] == current)
    if dispute is not None:
        return show_dispute(*dispute)
    g, lowered = certificate_grade_and_empty(entries, law, current)
    if g is not None:
        # a statistical law's pass carries its rates and what it spent (7.S17), the latest's
        tested = next((_tested(e) for e in _laws_own(entries) if e["law"] == law and e["cone"] == current
                       and passed(e) and _tested(e)), None)
        shown = f"supported, {GRADE_WORDS[g]}: held at {tested_text(tested)}" if tested else GRADE_WORDS[g]
        if lowered:  # the regions with no case that held the grade at sampled (D-2026-10-16-i)
            shown += f" (no case in {', '.join(lowered)})"
        # the union of its stretches, when it pools two or more (D-2026-10-16-g)
        return "; ".join([shown] + pools(entries, law, current))
    failed = next((e for e in _laws_own(entries) if e["law"] == law and e["cone"] == current
                   and isinstance(e["outcome"], dict) and "Failed" in e["outcome"]), None)
    if failed is not None:
        return "refuted at " + (f"{failed['conjunct']}: " if "conjunct" in failed else "") + failed["outcome"]["Failed"]
    return show_outcome(what)


def standings(path):
    """Per law a test line of the file names: its standing from the stores of its lines' claims,
    against the current hash of its cone (12.S11, 12.S14). Control lines aside (`control_standings`)."""
    from .tester import line_claims
    lines, claims = line_claims(path)
    entries = read_stores(claims)
    return [(law, standing(entries, law, current)) for law, current, control in lines if not control]


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
    law and cone must both match: mutually dependent laws can share one cone hash."""
    at = [e for e in controls if is_control(e) and e["law"] == law and e["cone"] == current]
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


def controls_in(stores):
    """The control entries of the stores of `stores`, files that make claims (a file without a
    store has none)."""
    return [e for e in read_stores(stores) if is_control(e)]


def control_standings(path):
    """Per law a control line of the file names: its control's standing from the stores of its
    lines' claims."""
    from .tester import line_claims
    lines, claims = line_claims(path)
    entries = read_stores(claims)
    return [(law, control_standing(entries, law, current)) for law, current, control in lines if control]


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
    grade the demand accepts, its reach covering what the run gives. [proposed] And of the demand's
    kind: a first action's demand (`FIRST_ACTION`) only by an entry a first action wrote, any other
    demand only by an entry of no kind (a control's has its own, and never passes). The entry's own
    grade; `serves_over` reads it over the law's regions."""
    return (entry["law"] == demand["law"] and entry_kind(entry) == demand.get("kind") and at(demand, entry)
            and passed(entry)
            and entry["grade"] is not None and GRADE_RANK[demand["accepts"]] <= GRADE_RANK[entry["grade"]]
            and covers_all(entry["reach"], demand["given"]))


def serves_over(demand, entry, entries):
    """`serves` with the entry's grade read over the law's regions under its binding, with the
    demand's combination (`served_grade`, D-2026-10-16-i; 3j j2a): what a run asks of the store's
    `entries`. [proposed] A second function and not a third argument of `serves`, which keeps the
    reference's signature."""
    if not serves(demand, entry):
        return False
    grade = served_grade(demand, entry, entries)
    return grade is not None and GRADE_RANK[demand["accepts"]] <= GRADE_RANK[grade]


def served(demand, entries):
    """Whether the entries serve the demand of a law (`serves_over`): one of them does, or, for a law
    whose body is a conjunction of laws (D-2026-10-18-f), one entry of each conjunct its entries at
    the demand's hash list does; a conjunct's entry never serves the conjunction alone."""
    if demand.get("byModel"):
        # a law of the model's theory that takes no model parameter (`doubles: Commutative`): an
        # entry of the law itself is about whatever model its line bound, so only the theory's
        # entries about the run's model serve it (the coordinator, 2026-10-22, on report-bite-12a.md)
        return "conjunction" in demand and _served_by_conjuncts(demand["conjunction"], entries)
    at_hash = [e for e in _laws_own(entries) if e["law"] == demand["law"] and at(demand, e)]
    conjuncts = list(dict.fromkeys(c for e in at_hash for c in e.get("conjuncts") or ()))
    if not conjuncts:
        return (any(serves_over(demand, e, entries) for e in entries)
                or "conjunction" in demand and _served_by_conjuncts(demand["conjunction"], entries))
    return all(any(serves_over(demand, e, [f for f in entries if f.get("conjunct") == c])
                   for e in entries if e.get("conjunct") == c) for c in conjuncts)


def _served_by_conjuncts(conjunction, entries):
    """[proposed, core bite 12a] A law demanded by its own name as one of a theory's laws
    (`doubles: Neutral`), served by the entries the tester records under the theory's law for the
    conjuncts the law stands for (`conjunction["heads"]`, the conjunct's text headed by one of
    them; D-2026-10-18-f): each such conjunct served at the theory law's hash, for the model the run
    gives. Not served when no conjunct of the theory is headed so."""
    at_hash = [e for e in _laws_own(entries) if e["law"] == conjunction["law"] and at(conjunction, e)]
    texts = dict.fromkeys(c for e in at_hash for c in e.get("conjuncts") or ())
    mine = [c for c in texts if _text_head(c) in conjunction["heads"]]
    return bool(mine) and all(any(serves_over(conjunction, e, [f for f in entries if f.get("conjunct") == c])
                                  for e in entries if e.get("conjunct") == c) for c in mine)


def _text_head(text):
    """The law a conjunct's printed text applies (`Neutral Float64 ...` is `Neutral`)."""
    return text.lstrip("(").split(" ", 1)[0].rstrip(")")


def served_grade(demand, entry, entries=None):
    """The grade an entry serves a demand at: its own, combined over the law's regions under its
    binding with the demand's combination (`regioned`; the weakest by default), so a region the
    binding never reached holds it at sampled (D-2026-10-16-i). Without `entries`, its own."""
    if not entries or entry_kind(entry) is not None:
        return entry["grade"]
    g, _ = regioned(entries, entry["law"], entry["cone"], entry["binding"], entry["grade"],
                    demand.get("combine", COMBINATION))
    return _or_weakest(g, entry["grade"])


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
    disagreement at the demand's hash is refused first, whatever serves, its state `Disagrees` with
    both entries (`ADisagreementIsRefused`, D-2026-10-15-f). Else a law with a
    failure at the demand's hash (`at`) is refused whatever serves, listed with that failure
    (certification_model's `refuseLaws` at 82c4cb4, `ACurrentFailureIsRefused`, C5 of the layer 3
    review: record/IA/layer-3-review-2026-10-15/report-fix-certification.md)."""
    refusals = []
    for c in cone:
        if c["provisional"]:
            refusals.append({"name": c["name"], "law": None, "state": ("Provisional", None)})
            continue
        for d in c["laws"]:
            if d.get("byModel"):
                # read against the theory's entries about the run's model (`served`); the law's own
                # entries are about other models, so neither their failures nor their states count
                if not served(d, entries):
                    m = d.get("conjunction")
                    mine = [e for e in entries if m is not None and covers_all(e.get("reach") or [], m["given"])]
                    refusals.append({"name": c["name"], "law": d["law"],
                                     "state": state_of(m, mine) if m is not None else ("Uncertified", None),
                                     "demand": m if m is not None else d})
                continue
            dispute = dispute_of(entries, d["law"], lambda e: at(d, e))
            failure = next((e for e in _laws_own(entries) if e["law"] == d["law"] and at(d, e) and _failed(e)),
                           None)
            if dispute is not None:
                refusals.append({"name": c["name"], "law": d["law"], "state": ("Disagrees", dispute), "demand": d})
            elif failure is not None:
                refusals.append({"name": c["name"], "law": d["law"], "state": ("Current", failure["outcome"]),
                                 "demand": d})
            elif not served(d, entries):
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
    if kind == "Disagrees":
        return f"{head}: {show_dispute(*what)}"
    d = refusal["demand"]
    if kind == "Stale":
        if what == d["cone"]:
            return f"{head}: stale (the model's code changed since its entries)"
        return f"{head}: stale (its entries are at {what[7:19]}, the cone is now at {d['cone'][7:19]})"
    if what != "Passed":
        return f"{head}: {show_outcome(what)}"
    current = [e for e in entries if e["law"] == d["law"] and at(d, e) and passed(e)]
    served = [served_grade(d, e, entries) for e in current]
    if all(GRADE_RANK[g] < GRADE_RANK[d["accepts"]] for g in served):
        best = max(served, key=GRADE_RANK.__getitem__)
        lowered = [e for e, g in zip(current, served) if g != e["grade"]]
        why = ""
        if lowered:  # the regions that held it at sampled (D-2026-10-16-i)
            _, empty = regioned(entries, d["law"], lowered[0]["cone"], lowered[0]["binding"], lowered[0]["grade"],
                                d.get("combine", COMBINATION))
            why = f" (no case in {', '.join(empty)})"
        return f"{head}: passed, {GRADE_WORDS[best]}{why}, below the grade accepted ({GRADE_WORDS[d['accepts']]})"
    shown = ", ".join(f"{p} = {_shown_value(v)}" for p, v in d["given"])
    return f"{head}: passed, but no passed entry's reach covers {shown}"


def _shown_value(v):
    return repr(v["Number"]) if "Number" in v else v["Printed"]


# ---------------------------------------------------------------------- `luthier certify` (12.S16)



def certify_file(path, seed=None, deep=False, fuel=None, store=True):
    """Run one file's test lines, each with the fuel of its budgets or `fuel` when given (7.S8),
    writing the stores of their claims (reading and writing none without `store`); per
    law its certificate's grade (the weakest across bindings) and the hash of its cone, the entries
    of its control lines, with the counts of lines run and known. Runs in its own process."""
    from .tester import run_tests
    try:
        outcomes = run_tests(path, seed, fuel, deep=deep, store=store)
        # a conjunction's line holds its conjuncts' entries (tester.py's `_run_conjunction`)
        entries = (read_stores(o.store for o in outcomes) if store
                   else [e for o in reversed(outcomes) for e in [o.entry] + [p.entry for p in o.parts or ()]
                         if e is not None])
    except Exception as exc:  # the file's failure is reported with the file, the others go on
        return {"path": str(path), "error": f"{type(exc).__name__}: {exc}"}
    laws = {}
    for o in outcomes:
        if not o.spec.control:
            laws.setdefault(o.spec.law, o.cone)
    # each control line with its own entry's outcome (the run's, or the store's when known)
    controls = [(o.spec.law, ", ".join(d["generator"] for d in o.entry["binding"]), show_outcome(o.entry["outcome"]))
                for o in outcomes if o.spec.control and o.entry is not None]
    # the controls are the law's (D-2026-10-22-a): read also from the stores of the files that state
    # the laws, where a control line writes, though no line of this file wrote there (core bite 13a)
    stated = read_stores({o.law_store for o in outcomes if o.law_store is not None} - {o.store for o in outcomes}) \
        if store else []
    return {"path": str(path),
            "laws": [(law, cone, standing(entries, law, cone)) for law, cone in laws.items()],
            "controls": controls,
            "control entries": [e for e in entries + stated if is_control(e)],
            "ran": sum(1 for o in outcomes if o.known is None),
            "known": sum(1 for o in outcomes if o.known is not None),
            "graded": all(certificate_grade(entries, law, cone) is not None for law, cone in laws.items())}


def certify(paths, jobs=1, seed=None, deep=False, fuel=None, out=print, store=True):
    """`luthier certify`: each file in its own process, `jobs` at a time; prints per file its laws,
    their grades and their control status, read from the control lines of every file given
    (7.S19, L9.14), and its control lines. True when every law of every file has a grade and no
    control failed. Every file is a test program (`x.test.lut`, 12.R2): another kind refuses the
    command before any line runs."""
    from concurrent.futures import ProcessPoolExecutor
    import multiprocessing
    from .run import RunError, require_kind
    refused = []
    for p in paths:
        try:
            require_kind(p, "test")
        except RunError as exc:
            refused.append(f"{p}: {exc}")
    if refused:
        for line in refused:
            out(line)
        return False
    context = multiprocessing.get_context("spawn")
    ok = True
    with ProcessPoolExecutor(max_workers=max(1, jobs), mp_context=context, max_tasks_per_child=1) as pool:
        futures = [pool.submit(certify_file, str(p), seed, deep, fuel, store) for p in paths]
        results = [future.result() for future in futures]
    # two files' lines may share a claim's store: each control entry once
    controls = list({identity(e): e for r in results for e in r.get("control entries", [])}.values())
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
