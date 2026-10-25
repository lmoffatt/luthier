"""certify.py and the store (record/IA/certification-2026-10-14/prompt-certify.md): the four laws of
certification.lth's `ConeHashing`, the store `x.cert.json` and `Store`'s predicate, a known
outcome reused by `luthier test` (7.S13), `--deep`, a changed definition making an entry stale
(12.S11), and `luthier certify` (12.S16)."""
import itertools
import json
import os
import shutil
from pathlib import Path

import pytest

from luthier import certify, term as t, tester
from luthier.cli import main

ROOT = Path(__file__).resolve().parents[1]
LAWS = ROOT / "tests" / "tester" / "laws.test.lut"
INT = t.Var("Int")


# ---------------------------------------------------------------------- the hash of a cone (§4)

def identity_on(x):
    return t.Lam(x, INT, t.Var(x))


def plus_one(x):
    return t.Lam(x, INT, t.App(t.App(t.Var("+"), t.Var(x)), t.Lit(t.IntConst(1))))


# a census of codes: alpha-variants, module prefixes and file tags, and codes that differ
CODES = [
    [("f", identity_on("x"))],
    [("f", identity_on("y"))],                      # alpha-equivalent to the first
    [("m.f", identity_on("z"))],                    # a module prefix, not seen
    [("f@numbers", identity_on("x"))],              # the loader's file tag, not seen
    [("f", plus_one("x"))],
    [("f", plus_one("w")), ("g", t.Var("f"))],
    [("g", t.Var("f")), ("f", plus_one("w"))],      # the same definitions in another order
    [("f", t.Lit(t.StringConst("a@b")))],           # a literal is kept as written
    [("f", t.Lit(t.StringConst("a")))],
]
HOSTS = [[], [("python:math.log", "python 3.13.5")], [("python:math.log", "sha256:00")]]
INTERPRETERS = ["abc", "abc+123", "luthier 0.2"]
CONES = [{"code": c, "hosts": h, "interpreter": i} for c in CODES for h in HOSTS for i in INTERPRETERS]


def with_(cone, **parts):
    return {**cone, **parts}


def test_hash_of_the_canonical_form():
    for c in CONES:
        assert certify.cone_hash(with_(c, code=certify.canon_code(c["code"]))) == certify.cone_hash(c)


def test_hash_sees_the_code():
    for c, code in itertools.product(CONES, CODES):
        assert (certify.canon_code(code) == certify.canon_code(c["code"])
                or certify.cone_hash(with_(c, code=code)) != certify.cone_hash(c))
    # and alpha-renaming, a module prefix, a file tag are not seen
    first = CONES[0]
    assert {certify.cone_hash(with_(first, code=code)) for code in CODES[:4]} == {certify.cone_hash(first)}


def test_hash_sees_the_host():
    for c, hosts in itertools.product(CONES, HOSTS):
        assert hosts == c["hosts"] or certify.cone_hash(with_(c, hosts=hosts)) != certify.cone_hash(c)


def test_hash_sees_the_interpreter():
    for c, r in itertools.product(CONES, INTERPRETERS):
        assert r == c["interpreter"] or certify.cone_hash(with_(c, interpreter=r)) != certify.cone_hash(c)


# ---------------------------------------------------------------------- the erasure (D-2026-10-15-e)

def _erase_names(x):
    """A control: an erasure that also erases each `Lam`'s binder, leaving its occurrences free. It
    goes past the annotations into what the term does, so the law below must refute it."""
    if isinstance(x, t.Lam):
        return t.Lam("erased", certify.ERASED, _erase_names(x.body))
    if isinstance(x, t.Let):
        return t.Let(x.name, certify.ERASED, _erase_names(x.value), _erase_names(x.body))
    if isinstance(x, (str, t.Lit, t.Primitive, t.Axiom, t.Extern)):
        return x
    if isinstance(x, tuple):
        return tuple(_erase_names(y) for y in x)
    if certify.is_dataclass(x) and not isinstance(x, type):
        return certify.replace(x, **{f.name: _erase_names(getattr(x, f.name)) for f in certify.fields(x) if f.init})
    return x


def _erased_program(program, erasure):
    return tuple(certify.replace(a, type=erasure(a.type), body=erasure(a.body)) if isinstance(a, t.Define) else a
                 for a in program)


def _one_step(program, x):
    from luthier import kernel
    try:
        return ("step", kernel.step(program, x))
    except Exception as exc:  # a step that raises (a zero divisor) must raise on both sides
        return ("raised", type(exc).__name__)


def _step_disagreement(program, terms, erasure):
    """certification.lth's `ErasureKeepsTheStep` on the host: for each term, one kernel step in the
    program, erased, agrees up to alpha with one step from the erased term in the erased program
    (both none, both raising, or the same term). By induction on the steps the erased term then
    reduces as the term does at any fuel. The first term where they disagree, or None."""
    from luthier import kernel
    erased = _erased_program(program, erasure)
    before = [_one_step(program, x) for x in terms]       # the kernel caches one program's tables
    after = [_one_step(erased, erasure(x)) for x in terms]
    for x, (k, u), (j, v) in zip(terms, before, after):
        if k != j or (k == "raised" and u != v):
            return x
        if k == "step" and (u is None) != (v is None):
            return x
        if k == "step" and u is not None and not kernel.alpha_equal(erasure(u), v):
            return x
    return None


def _library_terms(path, steps=200):
    """The terms the law is checked at, from the runtime program of a test program: every subterm of
    every definition (one step each: delta, stuck, a redex where the code holds one), and the
    trajectory of each definition without parameters, reduced step by step (beta through the
    annotated lambdas of the functions that build the program's censuses, the `Let`s of blocks)."""
    from luthier import kernel
    runner, _, _ = tester.load_program(path, 100_000)
    program = tuple(a for a in runner.program)
    terms, pending = [], [a.body for a in program if isinstance(a, t.Define)]
    while pending:
        x = pending.pop()
        terms.append(x)
        pending.extend(kernel._subterms(x))
    for a in program:
        if isinstance(a, t.Define) and not isinstance(a.body, t.Lam) and not isinstance(a.type, t.Pi):
            x = t.Var(a.name)
            for _ in range(steps):
                terms.append(x)
                try:
                    x = kernel.step(program, x)
                except Exception:
                    break
                if x is None:
                    break
    return program, terms


ERASURE_PROGRAMS = [ROOT / "tests" / "tester" / "certification_laws.test.lut",
                    ROOT / "tests" / "tester" / "numbers_laws.test.lut",
                    ROOT / "tests" / "tester" / "probability_laws.test.lut",   # blocks: their `Let`s
                    ROOT / "tests" / "tester" / "optimization_laws.test.lut"]


@pytest.fixture(scope="module")
def library_terms():
    return [_library_terms(p) for p in ERASURE_PROGRAMS]


def test_erasure_keeps_the_step_on_the_library(library_terms):
    # D-2026-10-15-e's condition, as a law: no erased annotation changes what the term does
    for program, terms in library_terms:
        assert any(isinstance(x, (t.Lam, t.Let)) for x in terms)
        assert _step_disagreement(program, terms, certify.erase) is None


def test_erasure_keeps_the_step_control_is_refuted(library_terms):
    # the control: erasing a binder with its annotation changes what the term does, and the law sees it
    assert any(_step_disagreement(program, terms, _erase_names) is not None for program, terms in library_terms)


def test_the_hash_does_not_see_a_binder_annotation(tmp_path):
    """Two elaborations that differ only in the annotations the elaborator writes (a parameter
    typed by hand or from the expected type, a block's `Let` typed or inferred) have one cone hash;
    a change to what the term does still changes it."""
    def hash_of(text):
        path = tmp_path / "p.lut"
        path.write_text(text, encoding="utf-8")
        runner, _, _ = tester.load_program(path, 10000, ("Law",))
        return certify.Cones(runner).hash("Law")
    typed = "Law (x : Int) : Bool := (fn (k : Int) { k + 1 }) x > x\n"
    expected = "Law (x : Int) : Bool := (fn k { k + 1 }) x > x\n"
    assert hash_of(typed) == hash_of(expected)
    # a block's `Let`, its type inferred by the elaborator or not (the six laws of report-sugar.md)
    let = lambda a: [("Law", t.Lam("x", INT, t.Let("y", a, t.Var("x"), t.Var("y"))))]
    cone = lambda code: certify.cone_hash({"code": code, "hosts": [], "interpreter": "i"})
    assert cone(let(INT)) == cone(let(t.Hole("type"))) == cone(let(t.Var("Float64")))
    assert cone(let(INT)) != cone([("Law", t.Lam("x", INT, t.Let("y", INT, t.Var("x"), t.Var("x"))))])
    assert hash_of(typed) != hash_of(typed.replace("k + 1", "k + 2"))
    # the definition's own type is no binder annotation: it says what the tester draws
    assert hash_of(typed) != hash_of(typed.replace("(x : Int)", "(x : Nat)"))
    # the erasure itself: a Lam's and a Let's annotation go, a Pi's domain stays
    lam = t.Lam("x", INT, t.Let("y", INT, t.Var("x"), t.Pi("z", INT, t.Var("y"))))
    assert certify.erase(lam) == t.Lam("x", certify.ERASED, t.Let("y", certify.ERASED, t.Var("x"),
                                                                   t.Pi("z", INT, t.Var("y"))))


def test_the_cone_of_a_name_in_a_program(tmp_path):
    """A definition the law reaches changes its hash; one it does not reach leaves it."""
    def hashes(text):
        path = tmp_path / "p.lut"
        path.write_text(text, encoding="utf-8")
        runner, _, loaded = tester.load_program(path, 10000, ("Law", "other"))
        cones = certify.Cones(runner)
        return cones.hash("Law"), cones.names("Law")
    base = "helper (x : Int) : Int := x + 1\nother : Int := 3\nLaw (x : Int) : Bool := helper x > x\n"
    h, names = hashes(base)
    assert {"Law", "helper"} <= names and "other" not in names
    assert hashes(base.replace("other : Int := 3", "other : Int := 4"))[0] == h
    assert hashes(base.replace("x + 1", "x + 2"))[0] != h
    assert hashes(base.replace("helper (x : Int) : Int := x + 1", "helper (y : Int) : Int := y + 1"))[0] == h


def _run_cones(path, roots=()):
    """The cones of the runtime program `run` builds for the file's `main` (run.py's pipeline), with
    `roots` kept beside it."""
    from luthier import run
    loaded = run.Loaded(path)
    entry = loaded.name(loaded.top, "main")
    return certify.Cones(run._elaborated(run.runtime_slice(loaded.acts, entry, run.core_data(loaded) + roots)))


def test_an_import_beside_a_library_name_leaves_its_cone(tmp_path):
    """prompt-scope.md item 2 (plots.py's report, finding 1): importing plot.lth's `text` (a
    definition the loader calls `text@plot`, since `text` is a label of tables.lth's `Cell`) left
    csv's cone, and the cones of Codec's laws, as they are without it (6.S8, 12.S22)."""
    head = 'import "tables.lth" Table Codec\nimport "tables_model.lut" csv : Codec\n'
    main = 'main (s : String) (p : Plot) : Maybe Table := match drawn p { q -> csv.parse s }\n'
    without = tmp_path / "without.lut"
    without.write_text(head + 'import "plot.lth" Plot addLayer texts\n'
                       'drawn (p : Plot) : Plot := addLayer p { geom := texts { size := 8.0 }, mapping := nil, table := "t" }\n'
                       + main, encoding="utf-8")
    with_text = tmp_path / "with_text.lut"
    with_text.write_text(head + 'import "plot.lth" Plot text\ndrawn (p : Plot) : Plot := text "t" nil 8.0 p\n' + main,
                         encoding="utf-8")
    # Codec's laws by the names the loader gives them: since world.lth imports term.lth (2ac8f12),
    # grammar.lth's RoundTrip and Canonical are loaded too, and tables.lth's are `RoundTrip@tables`
    from luthier import run
    loaded = run.Loaded(without)
    tables = next(p for p in loaded.by_file if Path(p).name == "tables.lth")
    laws = tuple(loaded.internal(tables, n) for n in ("RoundTrip", "Canonical", "Tolerant", "Rejects"))
    a, b = _run_cones(without, laws), _run_cones(with_text, laws)
    assert "text@plot" in b.acts and "text@plot" not in b.names("csv")
    assert a.hash("csv") == b.hash("csv")
    assert all(n in a.acts and n in b.acts for n in laws)
    assert [a.hash(n) for n in laws] == [b.hash(n) for n in laws]


def test_a_local_name_beside_a_library_law_leaves_its_cone(tmp_path):
    """prompt-scope.md item 2: a test program defining `apart` (plot.lth has one, then called
    `apart@plot`) left LayerOrderInvariant's cone as it is without it."""
    def law_hash(text):
        path = tmp_path / "p.lut"
        path.write_text(text, encoding="utf-8")
        runner, _, loaded = tester.load_program(path, 10000, ("LayerOrderInvariant", "apart"))
        cones = certify.Cones(runner)
        return cones.hash("LayerOrderInvariant"), cones.names("LayerOrderInvariant")
    base = 'import "plot.lth" LayerOrderInvariant\n'
    h, names = law_hash(base)
    h2, names2 = law_hash(base + "apart (x : Int) : Int := x + 1\n")
    assert "apart" in names and "apart@plot" in names2 and "apart" not in names2
    assert h == h2


def test_the_host_code_behind_an_extern(tmp_path, monkeypatch):
    module = tmp_path / "hostmod_certify.py"
    module.write_text("def f(x):\n    return x\n", encoding="utf-8")
    monkeypatch.syspath_prepend(str(tmp_path))
    certify.host_hash.cache_clear()
    first = certify.host_hash("python:hostmod_certify.f")
    module.write_text("def f(x):\n    return x + 0\n", encoding="utf-8")
    certify.host_hash.cache_clear()
    assert first.startswith("sha256:") and certify.host_hash("python:hostmod_certify.f") != first
    assert certify.host_hash("python:math.log").startswith("python ")   # the standard library
    np_hash = certify.host_hash("python:numpy.linalg.solve")             # an installed package
    assert np_hash.startswith("numpy ") or np_hash.startswith("python ") or np_hash.startswith("sha256:")
    certify.host_hash.cache_clear()


def test_the_route_the_model_names():
    # certification_model.lut: hashing's hash is extern "python:luthier.certify.cone_hash"
    text = (ROOT / "src" / "luthier" / "lib" / "certification_model.lut").read_text(encoding="utf-8")
    assert 'extern "python:luthier.certify.cone_hash"' in text
    assert callable(certify.cone_hash)


# ---------------------------------------------------------------------- the store (§1)

def entry(law="L", cone="sha256:1", seed=0, outcome="Passed", grade="Sampled", binding=()):
    # [bite A6] a sampled entry records its sampling budgets (`certify.formed_errors`)
    return {"law": law, "cone": cone, "binding": list(binding), "seed": seed, "cases": 100,
            "budgets": dict.fromkeys(certify.SAMPLED_REQUIRES, 1),
            "reach": [], "evidence": {"Points": {"evaluated": 100, "coverage": "Drawn 0"}}, "grade": grade, "outcome": outcome,
            "date": "2026-10-14T00:00:00+00:00", "interpreter": "abc", "hosts": []}


def test_a_store_under_a_directory_of_the_library_is_kept_apart_by_the_suite(monkeypatch, tmp_path):
    # the core's bite 1 moved core.lut to lib/core/: its store, and any under lib/core/, goes to the
    # suite's copy at its path under lib/, never to the library's own
    monkeypatch.setenv(certify.LIBRARY_STORES, str(tmp_path))
    core = certify.LIBRARY / "core" / "core.lut"
    assert certify.store_path(core) == tmp_path / "core" / "core.cert.json"
    assert certify.store_path(certify.LIBRARY / "numbers.lth") == tmp_path / "numbers.cert.json"
    assert certify.store_path(tmp_path / "x" / "y.lut") == tmp_path / "x" / "y.cert.json"


def test_a_store_round_trip(tmp_path):
    path = tmp_path / "x.lut"
    es = certify.record([], entry())
    es = certify.record(es, entry(seed=1, outcome={"Failed": "x = 3"}, grade=None))
    certify.write_store(path, es)
    assert certify.store_path(path) == tmp_path / "x.cert.json"
    assert certify.read_store(path) == es
    assert [e["seed"] for e in es] == [1, 0]  # the latest in front


def test_record_never_edits_an_entry():
    es = certify.record([], entry())
    assert certify.record(es, entry()) is es                     # an agreeing replay (D-2026-10-15-f)
    replay = entry(outcome={"Failed": "x = 1"}, grade=None)
    assert certify.record(es, replay) == [replay] + es          # a disagreeing one, beside the old
    assert len(certify.record(es, entry(seed=5))) == 2           # a new seed


def test_the_store_predicate_is_checked(tmp_path):
    path = tmp_path / "x.lut"
    # one identity, two outcomes: a disagreement the store records, not an error (D-2026-10-15-f)
    certify.write_store(path, [entry(), entry(outcome={"NotRunFor": "no generator"}, grade=None)])
    with pytest.raises(certify.StoreError, match="a grade exactly when passed"):
        certify.write_store(path, [entry(grade=None)])
    certify.store_path(path).write_text(json.dumps([entry(outcome={"Failed": "x"})]))
    with pytest.raises(certify.StoreError):
        certify.read_store(path)


def test_the_certificate_grade_and_the_state():
    b1, b2 = [{"parameter": "x", "generator": "a", "fingerprint": ""}], [{"parameter": "x", "generator": "b", "fingerprint": ""}]
    es = [entry(grade="Cases", binding=b1), entry(seed=1, grade="ExhaustiveGrade", binding=b1),
          entry(grade="Sampled", binding=b2)]
    # under one binding the strongest, across bindings the weakest
    assert certify.certificate_grade(es, "L", "sha256:1") == "Sampled"
    assert certify.certificate_grade(es[:2], "L", "sha256:1") == "ExhaustiveGrade"
    failed = [entry(seed=9, outcome={"Failed": "x = 1"}, grade=None)] + es
    assert certify.certificate_grade(failed, "L", "sha256:1") is None
    assert certify.standing(failed, "L", "sha256:1") == "refuted at x = 1"
    assert certify.state(es, "L", "sha256:2") == ("stale", "sha256:1")
    assert certify.state(es, "M", "sha256:1") == ("uncertified", None)
    assert certify.standing(es, "L", "sha256:2").startswith("stale")


# ---------------------------------------------------------------------- the tester and the store

@pytest.fixture
def laws(tmp_path):
    path = tmp_path / "laws.test.lut"
    shutil.copy(LAWS, path)
    return path


@pytest.fixture
def counted(monkeypatch):
    calls = []
    real = tester.evaluate

    def evaluate(*args):
        calls.append(args[1])
        return real(*args)
    monkeypatch.setattr(tester, "evaluate", evaluate)
    return calls


def test_a_known_outcome_is_reused(laws, counted):
    first = tester.run_tests(laws, store=True)
    assert counted and all(o.known is None for o in first)
    stored = certify.read_store(laws)
    assert len(stored) == len(first) == 6
    assert [e["law"] for e in stored][::-1] == [o.spec.law for o in first]
    passes = [e for e in stored if e["outcome"] == "Passed"]
    assert all(e["grade"] for e in passes) and all(e["grade"] is None for e in stored if e not in passes)
    counted.clear()
    second = tester.run_tests(laws, store=True)
    assert counted == []  # nothing ran again
    assert all(o.known == e["date"] for o, e in zip(second, stored[::-1]))
    # whatever its outcome: the refuted and the not-run lines are known too, with the same tail
    for a, b in zip(first, second):
        assert tester.line(a).rsplit(" (", 1)[0] == tester.line(b).rsplit(" (", 1)[0]
        assert tester.line(b).endswith(f"(known, {b.known})")
    assert certify.read_store(laws) == stored


def test_deep_runs_again_and_adds_nothing(laws, counted):
    tester.run_tests(laws, store=True)
    stored = certify.store_path(laws).read_text()
    counted.clear()
    again = tester.run_tests(laws, store=True, deep=True)
    assert counted and all(o.known is None for o in again)
    assert certify.store_path(laws).read_text() == stored


def test_a_new_seed_is_a_new_entry(laws):
    tester.run_tests(laws, store=True)
    tester.run_tests(laws, seed=99, store=True)
    stored = certify.read_store(laws)
    assert len(stored) == 12 and {e["seed"] for e in stored[:6]} == {99}


def test_a_changed_definition_makes_the_entry_stale(laws, capsys):
    tester.run_tests(laws, store=True)
    before = certify.read_store(laws)
    laws.write_text(laws.read_text().replace("Small (x : Int) : Bool := x < 50",
                                             "Small (x : Int) : Bool := x < 2000"))
    assert dict(certify.standings(laws))["Small"].startswith("stale")
    assert dict(certify.standings(laws))["NotInvolutive"] == "exhaustive"  # its cone did not change
    outcomes = tester.run_tests(laws, store=True)
    small = [o for o in outcomes if o.spec.law == "Small"]
    assert all(o.known is None and o.stale for o in small)
    assert "is stale, kept" in tester.line(small[0])
    assert all(o.known for o in outcomes if o.spec.law != "Small")
    after = certify.read_store(laws)
    # the stale entries of Small went once its new ones exist (6.S8 bounded); the others stay
    rest = [e for e in before if e["law"] != "Small"]
    assert [e for e in after if e["law"] != "Small"][-len(rest):] == rest
    assert all(e["cone"] == small[0].entry["cone"] for e in after if e["law"] == "Small")
    # its two bindings' samples of 100, each its ε̂, composed by the capped sum (bite B1)
    assert dict(certify.standings(laws))["Small"] == "sampled, ε̂ 0.06 at δ 0.05 (100 + 100 cases)"


def test_the_entry_holds_what_certification_lth_names(laws):
    tester.run_tests(laws, store=True)
    e = next(e for e in certify.read_store(laws) if e["law"] == "IntPlusCommutes" and e["seed"] == 7)
    # 7.S9 (3j j2a): the entry records its regions, here none of a type, a cutoff or a premise
    assert set(e) == {"law", "cone", "binding", "seed", "cases", "budgets", "reach", "evidence", "grade",
                      "outcome", "date", "interpreter", "hosts", "regions"}
    assert e["regions"] == []
    assert e["cases"] == 200 and e["grade"] == "Sampled" and e["outcome"] == "Passed"
    assert [d["parameter"] for d in e["binding"]] == ["x", "y"]
    assert e["reach"][0] == {"parameter": "x", "reach": {"Interval": [-10.0, 10.0]}}
    assert e["interpreter"] == certify.interpreter_revision()


def test_the_cli_test_and_check(laws, capsys):
    assert main(["test", str(laws)]) == 1
    ran = capsys.readouterr().out.splitlines()
    assert all(line.endswith("(ran)") for line in ran)
    main(["test", str(laws)])
    assert all("(known, " in line for line in capsys.readouterr().out.splitlines())
    main(["test", "--deep", str(laws)])
    assert capsys.readouterr().out.splitlines() == ran
    main(["check", "-v", str(laws)])
    out = capsys.readouterr().out
    assert "certificate NotInvolutive: exhaustive" in out and "certificate Small: refuted at x = 552" in out


# ---------------------------------------------------------------------- luthier certify (12.S16)

def test_certify_several_files(tmp_path, capsys):
    paths = []
    for name in ("laws.test.lut", "weakest.test.lut"):
        shutil.copy(ROOT / "tests" / "tester" / name, tmp_path / name)
        paths.append(str(tmp_path / name))
    assert main(["certify", "--jobs", "2", *paths]) == 1  # laws.test.lut has refuted laws
    out = capsys.readouterr().out.splitlines()
    assert out[0] == f"{paths[0]}: 4 laws, 6 lines ran, 0 known"
    # each law with its control status (7.S19): none of these has a control
    out = [line.replace("; uncontrolled: untested against any wrong model (7.S19)", "") for line in out]
    assert "  NotInvolutive: exhaustive" in out and any(o.startswith("  IntPlusCommutes: sampled, ε̂ ") for o in out)
    assert "  Small: refuted at x = 552" in out and "  AndIsOr: refuted at a = true, b = false" in out
    # weakest.test.lut: one law under two bindings, the weakest
    assert out[out.index(f"{paths[1]}: 1 laws, 2 lines ran, 0 known") + 1] == "  NotInvolutive: cases"
    assert main(["certify", paths[1]]) == 0
    assert capsys.readouterr().out.splitlines()[0] == f"{paths[1]}: 1 laws, 0 lines ran, 2 known"


@pytest.mark.skipif(not os.environ.get("LUTHIER_SLOW"), reason="a few minutes; set LUTHIER_SLOW=1")
def test_certify_the_laws_of_numbers(tmp_path, capsys):
    path = tmp_path / "numbers_laws.test.lut"
    shutil.copy(ROOT / "tests" / "tester" / "numbers_laws.test.lut", path)
    main(["certify", str(path)])
    out = capsys.readouterr().out.splitlines()
    assert "lines ran" in out[0] and not any("refuted" in line for line in out), out


CENSUS = '''import "test.lth" test SampledMode
import "generators_model.lut" linear
import "laws.lth" Listed
tol : Float64 := 1.0e-3
names : List String := ["a", "b"]
Close (t : Float64) (s : String) (x : Float64) : Bool := t > 0.0 and x == x
test "Close" (SampledMode linear) (cases <- 10) (whereBindings <- [
  { parameter := just "t", type := nothing, generator := "tol", coverage := Listed },
  { parameter := just "s", type := nothing, generator := "names", coverage := Listed } ])
'''


def test_the_reach_of_a_census_and_of_a_drawn_number(tmp_path):
    path = tmp_path / "census.test.lut"
    path.write_text(CENSUS, encoding="utf-8")
    [outcome] = tester.run_tests(path, store=True)
    e = outcome.entry
    assert e["outcome"] == "Passed"
    assert e["reach"] == [
        {"parameter": "t", "reach": {"Members": [{"Number": 1.0e-3}]}},
        {"parameter": "s", "reach": {"Members": [{"Printed": '"a"'}, {"Printed": '"b"'}]}},
        {"parameter": "x", "reach": {"Interval": [-10.0, 10.0]}}]
    assert [d["generator"] for d in e["binding"][:2]] == ["tol (Listed)", "names (Listed)"]
    # a number drawn under SampledMode: the hash of the code that draws it
    assert e["binding"][0]["fingerprint"].startswith("sha256:")
    assert e["binding"][2]["fingerprint"] == tester.drawing_revision()


def test_the_drawing_code_is_in_a_sampled_entry_s_identity(tmp_path, monkeypatch, counted):
    """The coordinator's addition to the core's bite 1 (j2a's finding 4): a change to the code that
    draws a sampled line's cases makes it a new identity, which runs again, while the interpreter's
    revision (the last tag) stays; a line that draws nothing keeps its identity."""
    path = tmp_path / "census.test.lut"
    path.write_text(CENSUS + EXHAUSTIVE_LINE, encoding="utf-8")
    first = tester.run_tests(path, store=True)
    assert [o.known for o in first] == [None, None] and len(counted) == 12  # 10 cases, then b in {true, false}
    monkeypatch.setattr(tester, "drawing_revision", lambda: "sha256:other draws")
    del counted[:]
    again = tester.run_tests(path, store=True)
    assert again[0].known is None and again[1].known is not None and len(counted) == 10
    assert again[0].entry["binding"][2]["fingerprint"] == "sha256:other draws"
    assert certify.identity(again[0].entry) != certify.identity(first[0].entry)


EXHAUSTIVE_LINE = '''import "test.lth" ExhaustiveMode
Small (b : Bool) : Bool := b or not b
test "Small" ExhaustiveMode
'''


# ---------------------------------------------------------------------- the model's own store

MODEL = '''import "numbers.lth" Doubles
doubles : Doubles Float64 := {
  plus := fn a b { a + b }, minus := fn a b { a - b }, times := fn a b { a * b }, divide := fn a b { a / b },
  less := fn a b { a < b }, leq := fn a b { a <= b }, greater := fn a b { a > b }, geq := fn a b { a >= b },
  unequal := fn a b { a /= b },
  epsilon := 2.220446049250313e-16,
}
'''
LAWS_OF_MODEL = '''import "test.lth" test SampledMode
import "generators_model.lut" linear
import "generators.lth" Binding
import "laws.lth" Listed
import "numbers.lth" Doubles DivideOne
import "m_model.lut" doubles

models : List Binding := [
  { parameter := nothing, type := just "Doubles", generator := "doubles", coverage := Listed } ]

Wrapper (d : Doubles Float64) (x : Float64) : Bool := DivideOne d x

test "DivideOne" (SampledMode linear) (profile <- models)
test "Wrapper" (SampledMode linear) (profile <- models)
'''


def test_an_entry_goes_into_the_store_of_the_file_that_defines_the_model(tmp_path):
    (tmp_path / "m_model.lut").write_text(MODEL, encoding="utf-8")
    top = tmp_path / "t_laws.test.lut"
    top.write_text(LAWS_OF_MODEL, encoding="utf-8")
    outcomes = tester.run_tests(top, store=True)
    home = certify.read_store(tmp_path / "m_model.lut")
    # only the model's store (L10.12, D-2026-10-16-b): the law of the library and the program's
    # own wrapper on the library's model; the test program keeps none
    assert [e["law"] for e in home][::-1] == ["DivideOne", "Wrapper"]
    assert not certify.store_path(top).exists()
    assert [o.store for o in outcomes] == [tmp_path / "m_model.lut"] * 2
    assert home[1]["outcome"] == "Passed" and len(outcomes) == 2
    # again: nothing new
    tester.run_tests(top, store=True, deep=True)
    assert certify.read_store(tmp_path / "m_model.lut") == home and not certify.store_path(top).exists()


LAWS_OF_LIST = LAWS_OF_MODEL.replace(
    '''models : List Binding := [
  { parameter := nothing, type := just "Doubles", generator := "doubles", coverage := Listed } ]''',
    '''census : List (Doubles Float64) := [doubles]
models : List Binding := [
  { parameter := nothing, type := just "Doubles", generator := "census", coverage := Listed } ]''')


def test_a_census_that_lists_a_model_sends_the_entry_to_its_file(tmp_path):
    (tmp_path / "m_model.lut").write_text(MODEL, encoding="utf-8")
    top = tmp_path / "t_laws.test.lut"
    top.write_text(LAWS_OF_LIST, encoding="utf-8")
    assert LAWS_OF_LIST != LAWS_OF_MODEL
    tester.run_tests(top, store=True)
    home = certify.read_store(tmp_path / "m_model.lut")
    assert [e["law"] for e in home][::-1] == ["DivideOne", "Wrapper"] and not certify.store_path(top).exists()
    assert all(e["binding"][0]["generator"].startswith("census") for e in home)


# record/IA/code-follows-2026-10-16/prompt-claim-store.md (L10.12, D-2026-10-16-b): an entry lives
# only beside the file that makes the claim; a test program keeps no store, and none beside it is read

SMALL_MODEL = '''Small : { f : Bool -> Bool }
FixesBool (m : Small) (b : Bool) : Bool := m.f b == b
Small := FixesBool
same : Small := { f := fn b { b } }
'''
SMALL_TEST = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
import "small_model.lut" Small FixesBool same
models : List Binding := [ { parameter := just "m", type := nothing, generator := "same", coverage := Listed } ]
test "FixesBool" ExhaustiveMode (whereBindings <- models)
'''
SMALL_USE = '''import "world_model.lut" HostConsole host : HostConsole
import "small_model.lut" same
show (b : Bool) : String := if b then "true" else "false"
main (w : W) : W * Unit := host.print w (show (same.f true))
'''


def _small(tmp_path):
    for name, text in (("small_model.lut", SMALL_MODEL), ("small_test.test.lut", SMALL_TEST),
                       ("uses.run.lut", SMALL_USE)):
        (tmp_path / name).write_text(text, encoding="utf-8")
    return tmp_path / "small_model.lut", tmp_path / "small_test.test.lut", tmp_path / "uses.run.lut"


def test_a_law_certified_from_a_test_program_is_found_by_a_run_that_imports_only_the_model(tmp_path, capsys):
    from luthier.run import Refused, run_file
    model, test, uses = _small(tmp_path)
    with pytest.raises(Refused, match="same: FixesBool: uncertified"):
        run_file(uses)
    assert main(["certify", str(test)]) == 0
    assert "1 lines ran, 0 known" in capsys.readouterr().out
    # the entry is in the model's store, none beside the test program
    assert [e["law"] for e in certify.read_store(model)] == ["FixesBool"]
    assert not certify.store_path(test).exists()
    # a run that loads the model's file and never the test program finds it
    assert run_file(uses) == "true\n"
    assert main(["certify", str(test)]) == 0
    assert "0 lines ran, 1 known" in capsys.readouterr().out
    assert not certify.store_path(test).exists()


def test_a_store_written_beside_a_test_program_by_hand_is_not_read(tmp_path, counted):
    # the control (L9.14): the same entry, moved by hand beside the test program, serves nothing
    from luthier.run import Refused, run_file
    model, test, uses = _small(tmp_path)
    tester.run_tests(test, store=True)
    entries = certify.read_store(model)
    certify.store_path(model).unlink()
    certify.store_path(test).write_text(json.dumps(entries), encoding="utf-8")
    assert dict(certify.standings(test)) == {"FixesBool": "uncertified"}
    with pytest.raises(Refused, match="same: FixesBool: uncertified"):
        run_file(uses)
    counted.clear()
    again, = tester.run_tests(test, store=True)
    assert again.known is None and counted  # it ran: the store beside the test program was not read
    assert certify.read_store(model) == [again.entry]
    assert json.loads(certify.store_path(test).read_text(encoding="utf-8")) == entries  # untouched


def test_adding_to_a_store_twice_keeps_one_entry(tmp_path):
    path = tmp_path / "m.lut"
    certify.add_entry(path, entry())
    certify.add_entry(path, entry())
    certify.add_entry(path, entry(seed=1))
    assert [e["seed"] for e in certify.read_store(path)] == [1, 0]


def test_a_store_another_process_writes_during_the_suite_survives():
    # record/IA/controls-2026-10-15/prompt-tail.md: the suite reads and writes a copy of the
    # library's stores (conftest.py), so a store that a `luthier certify` beside it rewrites during
    # a test keeps what certify wrote, and the test's own write never reaches the library
    import subprocess
    import sys
    from conftest import library_stores_apart
    probe = certify.LIBRARY / "suite_probe_model.lut"  # no such file is needed: the store is beside its name
    where = certify.LIBRARY / "suite_probe_model.cert.json"
    ours = {"law": "Ours", "cone": "sha256:0", "binding": [], "seed": 1, "cases": 1, "outcome": "Passed", "grade": "Cases"}
    theirs = dict(ours, law="Theirs")
    try:
        where.write_text("[]\n", encoding="utf-8")
        with library_stores_apart() as copy:
            certify.write_store(probe, [ours])
            assert json.loads((copy / where.name).read_text(encoding="utf-8")) == [ours]
            env = {k: v for k, v in os.environ.items() if k != certify.LIBRARY_STORES}
            subprocess.run([sys.executable, "-c",
                            "import json, sys; from luthier import certify; "
                            "certify.write_store(sys.argv[1], [json.loads(sys.argv[2])])",
                            str(probe), json.dumps(theirs)], env=env, check=True)
        assert json.loads(where.read_text(encoding="utf-8")) == [theirs]
    finally:
        where.unlink(missing_ok=True)


def test_interpreter_revision_is_the_last_tag():
    import subprocess
    tag = subprocess.run(["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True,
                         cwd=certify._PACKAGE).stdout.strip()
    assert tag and certify.interpreter_revision() == tag and "+" not in tag


# ---------------------------------------------------------------------- the store bounded (6.S8)

def _entry(law="L", cone="sha256:a", binding="b", seed=0, date="2026-10-15T00:00:00+00:00", outcome="Passed"):
    return {"law": law, "cone": cone, "binding": binding, "seed": seed, "cases": 10, "outcome": outcome,
            "grade": "Cases" if outcome == "Passed" else None, "date": date}


def test_a_store_keeps_four_entries_per_binding_at_the_current_cone():
    entries = []
    for k in range(7):
        entries = certify.record(entries, _entry(seed=k, date=f"2026-10-15T00:00:0{k}+00:00"))
    assert [e["seed"] for e in entries] == [6, 5, 4, 3]
    other = certify.record(entries, _entry(binding="c", seed=1))
    assert len(other) == 5            # another binding is another group


def test_stale_entries_go_once_a_current_one_exists_and_the_latest_stays_before():
    old = [_entry(cone="sha256:a", seed=k, date=f"2026-10-14T00:00:0{k}+00:00") for k in range(3)]
    old = list(reversed(old))
    assert [e["seed"] for e in certify.prune(old, {certify._group(old[0]): certify._stamp(_entry(cone="sha256:b"))})] == [2]  # all stale: the latest only
    store = certify.record(old, _entry(cone="sha256:b", seed=0))
    assert [e["cone"] for e in store] == ["sha256:b"]
    assert certify.store_errors(store) == []
    assert certify.known(store, certify.identity(_entry(cone="sha256:b", seed=0))) is not None
    assert certify.known(store, certify.identity(_entry(cone="sha256:a", seed=0))) is None


def test_prune_stores_rewrites_a_store_and_runs_nothing(tmp_path):
    entries = [_entry(seed=k, date=f"2026-10-15T00:00:0{k}+00:00") for k in range(6)][::-1]
    entries.append(_entry(cone="sha256:z", seed=9, date="2026-10-13T00:00:00+00:00"))
    where = tmp_path / "x.cert.json"
    where.write_text(json.dumps(entries))
    assert main(["certify", "--prune", str(where)]) == 0
    assert len(json.loads(where.read_text())) == 4


def test_a_current_failure_is_refused_whatever_serves():
    # ACurrentFailureIsRefused (certification.lth, C5 of the layer 3 review; certification_model's
    # refuseLaws at 82c4cb4): a passed entry that serves the demand, in front of a failure of the
    # same law at the same hash (two seeds), does not save the law; it is refused with the failure
    def entry(outcome, grade, seed):
        return {"law": "L", "cone": "h", "binding": [{"parameter": "m", "generator": "x", "fingerprint": "f"}],
                "seed": seed, "cases": 1, "reach": [{"parameter": "m", "reach": {"Members": [{"Printed": "x"}]}}],
                "outcome": outcome, "grade": grade}
    demand = {"law": "L", "cone": "h", "given": [("m", {"Printed": "x"})], "accepts": "Sampled",
              "fingerprints": {"m": "f"}}
    passed, failed = entry("Passed", "Proved", 1), entry({"Failed": "m = x"}, None, 2)
    assert certify.serves(demand, passed)
    cone = [{"name": "n", "provisional": False, "laws": [demand]}]
    refusals = certify.refuse([passed, failed], cone)
    assert [(r["name"], r["law"], r["state"]) for r in refusals] == [("n", "L", ("Current", {"Failed": "m = x"}))]
    assert certify.show_refusal(refusals[0], [passed, failed]) == "n: L: failed at m = x"
    # the failure at another hash is stale and the pass serves
    assert certify.refuse([passed, dict(failed, cone="old")], cone) == []


# ---------------------------------------------------------------------- controls (7.S19, L9.14)
# record/IA/controls-2026-10-15/prompt-tester.md: a control's entry is its own kind; it grades and
# refutes nothing, and gives each law its control status in `certify` and `check -v`

def control(outcome, cone="sha256:1", law="L", seed=0):
    return dict(entry(law=law, cone=cone, seed=seed, outcome=outcome, grade=None), kind="Control")


def test_a_control_entry_is_no_evidence_of_the_law():
    es = [dict(entry(), grade="Cases", evidence=_points("Listed"))]  # a pass over listed cases (bite B3)
    refuted = control({"ControlRefuted": "x = 1"})
    assert certify.certificate_grade([refuted] + es, "L", "sha256:1") == "Cases"
    assert certify.state([refuted] + es, "L", "sha256:1") == ("current", "Passed")
    assert certify.standing([refuted], "L", "sha256:1") == "uncertified"
    assert certify.store_errors([refuted] + es) == []
    # its kind is part of its identity: a control and a law line with one binding are two entries
    as_law = {k: v for k, v in refuted.items() if k != "kind"}
    assert certify.identity(refuted) != certify.identity(as_law)
    assert certify.record(es, refuted) == [refuted] + es
    # a run's demand: the control's refutation is no failure, and it serves nothing
    e = dict(es[0], reach=[{"parameter": "x", "reach": "Support"}])
    demand = {"law": "L", "cone": "sha256:1", "given": [], "accepts": "Cases"}
    cone = [{"name": "n", "provisional": False, "laws": [demand]}]
    assert certify.refuse([dict(refuted, reach=[]), e], cone) == []
    assert certify.refuse([dict(refuted, reach=[])], cone)[0]["state"] == ("Uncertified", None)


def test_the_control_status_of_a_law():
    refuted, held = control({"ControlRefuted": "x = 1"}), control({"ControlConfirmed": "cases"}, seed=1)
    assert certify.control_status([refuted], "L", "sha256:1") == "controlled (refuted on its control at x = 1)"
    assert certify.control_status([], "L", "sha256:1") == "uncontrolled: untested against any wrong model (7.S19)"
    assert certify.control_status([refuted, held], "L", "sha256:1").startswith("CONTROL FAILED")
    # A bare theory makes its mutually dependent laws share a cone; another law's control
    # must never certify this one's sensitivity (bite 6: Tables' eight laws exposed this).
    assert certify.control_status([dict(refuted, law="Other")], "L", "sha256:1").startswith("uncontrolled")
    assert certify.control_status([refuted, dict(held, law="Other")], "L", "sha256:1").startswith("controlled")
    # a control at another hash of the law's cone controls nothing now
    stale = certify.control_status([refuted], "L", "sha256:2")
    assert stale.startswith("uncontrolled") and "another hash" in stale
    not_run = certify.control_status([control({"NotRunFor": "why"})], "L", "sha256:1")
    assert not_run.startswith("uncontrolled") and "did not run (not run: why)" in not_run
    # a law entry is no control
    assert certify.control_status([entry(grade="Cases")], "L", "sha256:1").startswith("uncontrolled")


def test_certify_lists_the_laws_of_tables_with_their_controls(capsys):
    # the acceptance of the brief, then every law of tables controlled (prompt-mutants.md); no store
    laws, controls = (ROOT / "tests" / "tester" / f"tables_{n}.test.lut" for n in ("laws", "controls"))
    # the stores of the claims (L10.12): tables_model.lut's and tables.lth's; none beside the programs
    claims = [certify.LIBRARY / n for n in ("tables_model.lut", "tables.lth")]
    stores = [certify.store_path(p).read_bytes() for p in claims]
    assert main(["certify", "--no-cert", str(laws), str(controls)]) == 0
    out = capsys.readouterr().out.splitlines()
    assert [certify.store_path(p).read_bytes() for p in claims] == stores
    assert not any(certify.store_path(p).exists() for p in (laws, controls))
    # core bite 11 added TableIsIndexed and TableIsAnObject, each with its control
    assert out[0] == f"{laws}: 10 laws, 10 lines ran, 0 known"
    assert "  CellsOfTheirKind: cases; controlled (refuted on its control at t = holeT)" in out
    assert all("; controlled (refuted on its control at " in line for line in out[1:11])
    assert out[11] == f"{controls}: 0 laws, 10 controls, 10 lines ran, 0 known"
    assert out[12] == ("  control of CellsOfTheirKind on holes (Listed): refuted at t = holeT: "
                       "the control passed")
    assert all(line.endswith(": the control passed") for line in out[12:22])


# the laws and the functions live in a library (a test program is never imported, 12.R2), whose
# store holds the entries and the controls of the laws it states (L10.12)
PAIR = '''Stable (f : Bool -> Bool) (b : Bool) : Bool := f (f b) == f b
SelfEqual (a : Bool) : Bool := a == a
keep (x : Bool) : Bool := x
toggle (x : Bool) : Bool := if x then false else true
always (x : Bool) : Bool := true
'''
PAIR_LAWS = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
import "pair.lut" Stable SelfEqual keep always
goods : List (Bool -> Bool) := [keep, always]
onGoods : List Binding := [ { parameter := just "f", type := nothing, generator := "goods", coverage := Listed } ]
test "Stable" ExhaustiveMode (whereBindings <- onGoods)
test "SelfEqual" ExhaustiveMode
'''
PAIR_CONTROLS = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
import "pair.lut" Stable toggle always
toggles : List (Bool -> Bool) := [toggle]
alwayss : List (Bool -> Bool) := [always]
onFlip : List Binding := [ { parameter := just "f", type := nothing, generator := "toggles", coverage := Listed } ]
onAlways : List Binding := [ { parameter := just "f", type := nothing, generator := "alwayss", coverage := Listed } ]
test "Stable" ExhaustiveMode (whereBindings <- onFlip) (control <- true)
'''


def test_controls_through_the_stores_in_certify_and_check(tmp_path, capsys):
    laws, controls, pair = tmp_path / "laws.test.lut", tmp_path / "controls.test.lut", tmp_path / "pair.lut"
    pair.write_text(PAIR, encoding="utf-8")
    laws.write_text(PAIR_LAWS, encoding="utf-8")
    controls.write_text(PAIR_CONTROLS, encoding="utf-8")
    assert main(["certify", str(laws), str(controls)]) == 0
    out = capsys.readouterr().out.splitlines()
    assert "  Stable: cases; controlled (refuted on its control at f = toggle, b = true)" in out
    assert "  SelfEqual: exhaustive; uncontrolled: untested against any wrong model (7.S19)" in out
    # the control lives beside the claim it controls, the file that states the law (L10.12): no
    # test program keeps a store
    assert not certify.store_path(laws).exists()
    stored = [e for e in certify.read_store(pair) if certify.is_control(e)]
    assert [(e["kind"], e["outcome"], e["grade"]) for e in stored] == \
        [("Control", {"ControlRefuted": "f = toggle, b = true"}, None)]
    assert not certify.store_path(controls).exists()
    # check -v reads the controls from the stores of the claims of the files it is given
    main(["check", "-v", str(laws), str(controls)])
    out = capsys.readouterr().out
    assert "certificate Stable: cases; controlled (refuted on its control at f = toggle, b = true)" in out
    assert "certificate control of Stable: refuted at f = toggle, b = true: the control passed" in out
    main(["check", "-v", str(laws)])  # the law's store holds its control: controlled without the file
    assert "certificate Stable: cases; controlled" in capsys.readouterr().out
    # a control the law holds on fails, loudly, and certify fails; the grade is unchanged
    controls.write_text(PAIR_CONTROLS + 'test "Stable" ExhaustiveMode (whereBindings <- onAlways) '
                        '(control <- true)\n', encoding="utf-8")
    assert main(["certify", str(laws), str(controls)]) == 1
    out = capsys.readouterr().out.splitlines()
    assert any(line.startswith("  Stable: cases; CONTROL FAILED") and "alwayss" in line for line in out)
    assert any(line.startswith("  control of Stable on alwayss (Listed), ExhaustiveMode over Bool: "
                               "CONTROL FAILED") for line in out)


# ---------------------------------------------------------------------- statistical laws (laws.lth §4)
# record/IA/statistical-2026-10-15/prompt-tester.md: a statistical law's entry holds `Tested` with
# its rates, its grade shows them (7.S17), its control is matched by the law's cone as any

CONSTANT = '''import "generators.lth" Seed
import "laws.lth" Law Statistical StatisticalLaw Sequential byPValue
pv : StatisticalLaw Float64 := byPValue Float64 (fn p { p })
Constant (p : Float64) (c : Sequential) : Law := Statistical Float64 Seed pv (fn n s { (p, s) }) c
'''
STATISTICAL_LAWS = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Sequential Listed
import "constant.lut" Constant
wald : Sequential := { alpha := 0.01, beta := 0.01, delta := 0.9, initial := 1, budget := 100 }
ones : List Float64 := [1.0]
onOnes : List Binding := [ { parameter := just "p", type := nothing, generator := "ones", coverage := Listed },
  { parameter := just "c", type := nothing, generator := "wald", coverage := Listed } ]
test "Constant" ExhaustiveMode (seed <- 5) (profile <- onOnes)
'''
STATISTICAL_CONTROLS = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed Sequential
import "constant.lut" Constant
wald : Sequential := { alpha := 0.01, beta := 0.01, delta := 0.9, initial := 1, budget := 100 }
zeros : List Float64 := [0.0]
onZeros : List Binding := [ { parameter := just "p", type := nothing, generator := "zeros", coverage := Listed },
  { parameter := just "c", type := nothing, generator := "wald", coverage := Listed } ]
test "Constant" ExhaustiveMode (seed <- 5) (profile <- onZeros) (control <- true)
'''


def test_certify_a_statistical_law_with_its_rates_and_its_control(tmp_path, capsys):
    laws, controls = tmp_path / "laws.test.lut", tmp_path / "controls.test.lut"
    (tmp_path / "constant.lut").write_text(CONSTANT, encoding="utf-8")
    laws.write_text(STATISTICAL_LAWS, encoding="utf-8")
    controls.write_text(STATISTICAL_CONTROLS, encoding="utf-8")
    rates = "by the sequential test (alpha 0.01, beta 0.01, delta 0.9, budget 100)"
    for known in (0, 1):  # the second time every line is known, and reads the same
        assert main(["certify", str(laws), str(controls)]) == 0
        out = capsys.readouterr().out.splitlines()
        assert out == [
            f"{laws}: 1 laws, {1 - known} lines ran, {known} known",
            f"  Constant: supported, sampled: held at 2 samples of 1 {rates}; controlled (refuted on its "
            f"control at 8 samples of 1 {rates})",
            f"{controls}: 0 laws, 1 controls, {1 - known} lines ran, {known} known",
            f"  control of Constant on zeros (Listed), wald (Listed): refuted at 8 samples of 1 {rates}: "
            "the control passed",
        ]
    entry, = [e for e in certify.read_store(tmp_path / "constant.lut") if not certify.is_control(e)]
    assert entry["evidence"]["Tested"] == {"verdict": "Holds", "alpha": 0.01, "beta": 0.01, "delta": 0.9,
                                           "spent": 2, "initial": 1, "budget": 100}
    assert certify.store_errors([entry]) == []
    known, = tester.run_tests(laws, store=True)
    assert known.known is not None and (known.verdict, known.evaluated) == ("Supported", 2)
    assert tester.line(known).startswith("Constant: sequential (seed 5), 2 samples, supported, sampled: held at")
    # an unresolved test is no failure and no grade: it says so
    assert certify.show_outcome({"NotRunFor": f"unresolved at 100 samples of 1 {rates}"}) == \
        f"unresolved at 100 samples of 1 {rates}"


def test_an_unresolved_entry_round_trips_and_a_statistical_pass_is_a_holds_graded_sampled(tmp_path):
    tested = {"verdict": "Unresolved", "alpha": 0.01, "beta": 0.01, "delta": 0.9, "spent": 100,
              "initial": 1, "budget": 100}
    unresolved = entry(outcome={"Unresolved": tested}, grade=None)
    unresolved["evidence"] = {"Tested": tested, "coverage": "Drawn"}
    path = tmp_path / "u.lut"
    certify.write_store(path, [unresolved])
    assert certify.read_store(path) == [unresolved]
    assert certify.show_outcome(unresolved["outcome"]) == f"unresolved at {certify.tested_text(tested)}"
    # a store written before: the old NotRunFor text still reads
    old = entry(outcome={"NotRunFor": "unresolved at 100 samples"}, grade=None)
    assert certify.store_errors([old]) == []
    assert certify.show_outcome(old["outcome"]) == "unresolved at 100 samples"
    # a pass over Tested evidence is a Holds graded sampled, no other
    holds = dict(tested, verdict="Holds")
    ok = entry(grade="Sampled")
    ok["evidence"] = {"Tested": holds, "coverage": "Drawn"}
    assert certify.store_errors([ok]) == []
    for grade, verdict in (("Cases", "Holds"), ("Sampled", "Fails")):
        bad = entry(grade=grade)
        bad["evidence"] = {"Tested": dict(tested, verdict=verdict), "coverage": "Drawn"}
        assert "a Holds graded sampled" in certify.store_errors([bad])[0]


# ---------------------------------------------------------------------- an exact replay, and fuel
# record/IA/code-follows-2026-10-16/prompt-replay-fuel.md (step 3c): an exact replay is absorbed
# when it agrees and kept beside the old entry when it disagrees, which refuses the law until a
# later agreeing pair (D-2026-10-15-f); a not-run for lack of fuel is never stored, and the fuel is
# in no identity (D-2026-10-15-g). The store law is certification.lth's `Recording`.

FLAKY_HOST = '''"""A host function whose result the test changes between two runs, the code unchanged."""
MODE = "same"


def answer(b):
    if MODE == "raise":
        raise ValueError("the host is down")
    return (not b) if MODE == "flip" else b
'''
FLAKY_MODEL = '''Small : { f : Bool -> Bool }
FixesBool (m : Small) (b : Bool) : Bool := m.f b == b
Small := FixesBool
answer (b : Bool) : Bool := extern "python:flaky_host.answer" b
same : Small := { f := fn b { answer b } }
'''


def test_an_agreeing_replay_leaves_the_store_byte_identical(tmp_path, capsys):
    model, test, uses = _small(tmp_path)
    assert main(["certify", str(test)]) == 0
    before = certify.store_path(model).read_bytes()
    assert main(["certify", "--deep", str(test)]) == 0
    assert "1 lines ran, 0 known" in capsys.readouterr().out.splitlines()[-2]
    assert certify.store_path(model).read_bytes() == before


def _flaky(tmp_path, monkeypatch):
    model, test, uses = _small(tmp_path)
    model.write_text(FLAKY_MODEL, encoding="utf-8")
    (tmp_path / "flaky_host.py").write_text(FLAKY_HOST, encoding="utf-8")
    monkeypatch.syspath_prepend(str(tmp_path))
    import flaky_host
    return model, test, uses, flaky_host


def test_a_disagreeing_replay_is_kept_and_refuses_the_law(tmp_path, monkeypatch, capsys):
    from luthier.run import Refused, run_file
    model, test, uses, flaky_host = _flaky(tmp_path, monkeypatch)
    first, = tester.run_tests(test, store=True)
    assert first.entry["outcome"] == "Passed" and run_file(uses) == "true\n"
    # the host's result changes, its code does not: the same identity gives another outcome
    monkeypatch.setattr(flaky_host, "MODE", "flip")
    replay, = tester.run_tests(test, store=True, deep=True)
    assert certify.identity(replay.entry) == certify.identity(first.entry)
    assert replay.entry["outcome"] == {"Failed": "m = same, b = true"}
    assert "replay disagrees with the known entry of" in tester.line(replay)
    assert certify.read_store(model) == [replay.entry, first.entry]  # both kept, the replay in front
    standing = dict(certify.standings(test))["FixesBool"]
    assert standing.startswith("replay disagrees at seed")
    assert f"the entry of {replay.entry['date']} (failed at m = same, b = true)" in standing
    assert f"the entry of {first.entry['date']} (passed, cases)" in standing
    main(["check", "-v", str(test)])
    assert "certificate FixesBool: replay disagrees at seed" in capsys.readouterr().out
    with pytest.raises(Refused, match="same: FixesBool: replay disagrees at seed"):
        run_file(uses)
    # a line reused from the store says so too
    known, = tester.run_tests(test, store=True)
    assert known.known == replay.entry["date"] and "replay disagrees with the entry of" in tester.line(known)
    # a later agreeing pair settles the disagreement, not the failure: a counterexample at the
    # current hash still refutes the law (6.S3, L10.3) until it is removed by hand
    monkeypatch.setattr(flaky_host, "MODE", "same")
    tester.run_tests(test, store=True, deep=True)
    with pytest.raises(Refused, match="replay disagrees"):
        run_file(uses)
    tester.run_tests(test, store=True, deep=True)
    assert len(certify.read_store(model)) == 4
    assert dict(certify.standings(test))["FixesBool"] == "refuted at m = same, b = true"
    with pytest.raises(Refused, match="same: FixesBool: failed at m = same, b = true"):
        run_file(uses)


def test_a_later_agreeing_pair_settles_a_disagreement(tmp_path, monkeypatch):
    from luthier.run import Refused, run_file
    model, test, uses, flaky_host = _flaky(tmp_path, monkeypatch)
    tester.run_tests(test, store=True)
    # the host fails: the replay settles nothing, and disagrees with the pass
    monkeypatch.setattr(flaky_host, "MODE", "raise")
    replay, = tester.run_tests(test, store=True, deep=True)
    assert replay.entry["outcome"]["NotRunFor"].startswith("unsettled: 2 cases raised")
    assert dict(certify.standings(test))["FixesBool"].startswith("replay disagrees")
    # the host back: a pass disagrees with the latest (the not-run), kept; still refused
    monkeypatch.setattr(flaky_host, "MODE", "same")
    tester.run_tests(test, store=True, deep=True)
    assert len(certify.read_store(model)) == 3
    with pytest.raises(Refused, match="replay disagrees"):
        run_file(uses)
    # a later agreeing pair settles it
    tester.run_tests(test, store=True, deep=True)
    assert len(certify.read_store(model)) == 4
    assert dict(certify.standings(test))["FixesBool"] == "cases"
    assert run_file(uses) == "true\n"
    # and an agreeing replay of a settled identity writes nothing
    after = certify.store_path(model).read_bytes()
    tester.run_tests(test, store=True, deep=True)
    assert certify.store_path(model).read_bytes() == after


def test_a_disagreement_is_kept_through_pruning():
    # the two entries of a disagreement stay, however many newer seeds the group holds
    old = [entry(seed=0, outcome={"Failed": "x = 1"}, grade=None), entry(seed=0)]
    newer = [dict(entry(seed=s), date=f"2026-10-15T00:00:0{s}+00:00") for s in range(1, 6)]
    kept = certify.prune(newer + old)
    assert all(e in kept for e in old) and len(kept) == 6


def test_the_store_law_holds_on_the_reference_and_its_controls_refute_the_broken_stores():
    # certification.lth's `Recording` and the two laws of a disagreement, on certification_model.lut;
    # the controls (L9.14): a store that absorbs a disagreeing replay, one that keeps a not-run for
    # lack of fuel, and a `certifying` blind to a disagreement, each refuted
    laws = tester.run_tests(ROOT / "tests" / "tester" / "certification_laws.test.lut")
    assert [o.spec.law for o in laws] == ["ANewIdentityGoesInFront", "AnAgreeingReplayAddsNothing",
                                          "ADisagreeingReplayIsKept", "AnAgreeingPairSettles",
                                          "AnExhaustionIsNeverStored", "RecordingKeepsTheOrderWritten",
                                          "ADisagreementRefutes", "ADisagreementIsRefused",
                                          "NoCutoffAcceptsAFailure", "ErasureKeepsTheStep", "IdentityIsTheKey",
                                          "PruningKeepsACurrentFailure", "PruningOnlyDrops", "PruningNeverRaisesAGrade"]
    assert all(o.grade == "ExhaustiveGrade" or o.grade == "Cases" for o in laws), [tester.line(o) for o in laws]
    controls = tester.run_tests(ROOT / "tests" / "tester" / "certification_controls.test.lut")
    assert [(o.spec.law, o.verdict) for o in controls] == [
        ("ADisagreeingReplayIsKept", "Refuted"), ("AnExhaustionIsNeverStored", "Refuted"),
        ("ADisagreementRefutes", "Refuted"), ("ADisagreementIsRefused", "Refuted"),
        ("ANewIdentityGoesInFront", "Refuted"), ("AnAgreeingReplayAddsNothing", "Refuted"),
        ("AnAgreeingPairSettles", "Refuted"), ("IdentityIsTheKey", "Refuted"), ("PruningKeepsACurrentFailure", "Refuted"),
        ("PruningNeverRaisesAGrade", "Refuted"), ("PruningOnlyDrops", "Refuted"), ("ErasureKeepsTheStep", "Refuted"),
        ("RecordingKeepsTheOrderWritten", "Refuted")]
    absorbed, = (o for o in controls if o.spec.law == "ADisagreeingReplayIsKept")
    assert "r = absorbing, e = passOne, es = ((cons failOne) ((cons passOne) nil))" in tester.line(absorbed)


SLOW = '''import "test.lth" test ExhaustiveMode
countDown (n : Int) : Int := if n <= 0 then 0 else countDown (n - 1)
Slow (b : Bool) : Bool := countDown 200 == 0
test "Slow" ExhaustiveMode
'''


def test_a_line_out_of_fuel_leaves_no_entry_and_runs_again_with_enough(tmp_path, counted):
    path = tmp_path / "slow.test.lut"
    path.write_text(SLOW, encoding="utf-8")
    cut, = tester.run_tests(path, fuel=100, store=True)
    assert cut.out_of_fuel == 100 and cut.entry["outcome"] == {"NotRunFor": certify.FUEL_SPENT}
    assert "fuel spent (100 given; nothing stored" in tester.line(cut)
    assert not certify.store_path(path).exists()
    # never written, so the next run runs it again, with the same identity (fuel is in none)
    counted.clear()
    again, = tester.run_tests(path, fuel=100, store=True)
    assert again.known is None and counted and not certify.store_path(path).exists()
    ran, = tester.run_tests(path, store=True)
    assert ran.known is None and ran.entry["outcome"] == "Passed"
    assert certify.identity(ran.entry) == certify.identity(cut.entry)
    assert certify.read_store(path) == [ran.entry]
    # and the store law refuses a fuel not-run whatever the store holds
    assert certify.record([ran.entry], cut.entry) == [ran.entry]
    assert certify.record([], cut.entry) == []


# the core's budgets brief (record/plan/core-2026-10-17/prompt-budgets.md; 7.S8, P11): a line's fuel
# is a budget of the line, test.lth's default unless it gives its own, recorded in its entry, and
# `--fuel` overrides it for a run, recorded too; fuel is in no identity (D-2026-10-15-g)
OWN_FUEL = '''import "test.lth" test ExhaustiveMode withFuel defaultBudgets
countDown (n : Int) : Int := if n <= 0 then 0 else countDown (n - 1)
Slow (b : Bool) : Bool := countDown 200 == 0
test "Slow" ExhaustiveMode (budgets <- withFuel 100 defaultBudgets)
'''


def test_a_line_runs_with_its_own_fuel_and_records_it(tmp_path):
    path = tmp_path / "own.test.lut"
    path.write_text(OWN_FUEL, encoding="utf-8")
    cut, = tester.run_tests(path, store=True)
    assert cut.spec.budgets["fuel"] == 100 and cut.out_of_fuel == 100
    assert cut.entry["budgets"]["fuel"] == 100 and not certify.store_path(path).exists()
    # test.lth's default, without a budget of the line's own
    default, = tester.run_tests(_written(tmp_path / "plain.test.lut", SLOW), store=True)
    assert default.entry["outcome"] == "Passed" and default.entry["budgets"]["fuel"] == 3_000_000


def test_the_fuel_given_overrides_the_line_s_and_is_recorded(tmp_path):
    path = tmp_path / "own.test.lut"
    path.write_text(OWN_FUEL, encoding="utf-8")
    ran, = tester.run_tests(path, fuel=1_000_000, store=True)
    assert ran.entry["outcome"] == "Passed" and ran.entry["budgets"]["fuel"] == 1_000_000
    assert certify.read_store(path)[0]["budgets"]["fuel"] == 1_000_000
    # the line's own fuel would cut it, but the outcome is known: fuel is out of the identity
    known, = tester.run_tests(path, store=True)
    assert known.known is not None and known.entry["outcome"] == "Passed"
    # `luthier certify --fuel`, a file in its own process (certify_file here, in this one)
    other = _written(tmp_path / "plain.test.lut", SLOW)
    cut = certify.certify_file(str(other), fuel=100, store=False)
    assert cut["laws"][0][2] == "not run: fuel spent" and not cut["graded"]
    assert certify.certify_file(str(other), store=False)["laws"][0][2] == "exhaustive"


def _written(path, text):
    path.write_text(text, encoding="utf-8")
    return path


# ---------------------------------------------------------------------- the union of the stretches
# record/IA/code-follows-2026-10-16/prompt-pool-seeds.md (step 3i; D-2026-10-16-g, L10.3): a stretch
# is one run of a law under one binding and one seed; the union of the agreeing stretches is one
# sample of their total size, and a statistical law's stretches continue one sequential test.

POOLED = '''import "test.lth" test SampledMode
import "generators_model.lut" linear
IntPlusCommutes (x y : Int) : Bool := x + y == y + x
test "IntPlusCommutes" (SampledMode linear) (seed <- 1)
test "IntPlusCommutes" (SampledMode linear) (seed <- 2)
'''


def _pooled_law(tmp_path, text=POOLED):
    path = tmp_path / "pooled.test.lut"
    path.write_text(text, encoding="utf-8")
    outcomes = tester.run_tests(path, store=True)
    return path, outcomes, certify.read_store(path)


def test_two_stretches_of_100_cases_with_different_seeds_give_a_grade_over_200(tmp_path):
    path, (one, two), entries = _pooled_law(tmp_path)
    assert [e["cases"] for e in entries] == [100, 100] and {e["seed"] for e in entries} == {1, 2}
    binding = certify.union_key(entries[0])  # the binding with its sampling budgets (bite 13c)
    assert certify.pooled(entries, "IntPlusCommutes", one.cone, binding) == 200
    assert certify.certificate_grade(entries, "IntPlusCommutes", one.cone) == "Sampled"
    assert dict(certify.standings(path))["IntPlusCommutes"] == \
        "sampled, ε̂ 0.015 at δ 0.05 (200 cases); pooled over seeds 1, 2: 200 cases in all"
    # one stretch is the line's own n, and the standing reads as before
    assert certify.pooled(entries[1:], "IntPlusCommutes", one.cone, binding) == 100
    assert certify.standing(entries[1:], "IntPlusCommutes", one.cone) == "sampled, ε̂ 0.03 at δ 0.05 (100 cases)"


def test_a_replayed_seed_does_not_double_n(tmp_path):
    path, (one, _), entries = _pooled_law(tmp_path)
    law, binding = "IntPlusCommutes", certify.union_key(entries[0])
    stored = certify.store_path(path).read_text()
    # an agreeing replay is absorbed by the store (Recording), and counted once if it were kept
    tester.run_tests(path, store=True, deep=True)
    assert certify.store_path(path).read_text() == stored
    replay = dict(entries[0], date="2026-10-17T00:00:00+00:00")
    assert certify.pooled([replay] + entries, law, one.cone, binding) == 200
    # a larger n of one seed holds the smaller as its first cases: the larger counts, once
    larger = dict(entries[0], cases=300, date="2026-10-17T00:00:00+00:00")
    assert certify.pooled([larger] + entries, law, one.cone, binding) == 400
    # a disagreement in any stretch refuses the union
    disagreeing = dict(entries[1], outcome={"Failed": "x = 1, y = 2"}, grade=None, date="2026-10-17T00:00:00+00:00")
    assert certify.certificate_grade([disagreeing] + entries, law, one.cone) is None
    assert certify.standing([disagreeing] + entries, law, one.cone).startswith("replay disagrees")
    # a run over every value is one stretch whatever its seed
    every = [dict(e, evidence={"Points": {"evaluated": 4, "coverage": "Exhaustive"}}, cases=4) for e in entries]
    assert certify.pooled(every, law, one.cone, binding) == 4


# a constant p-value of one: each sample multiplies the ratio by 0.5 at delta 0.5, so the test holds the
# law at its seventh sample (0.5^7 <= 0.01/0.99); under a budget of 3 it is unresolved
STRETCHED = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Seed Binding
import "laws.lth" Law Statistical StatisticalLaw Sequential byPValue Listed
pv : StatisticalLaw Float64 := byPValue Float64 (fn p { p })
Constant (p : Float64) (c : Sequential) : Law := Statistical Float64 Seed pv (fn n s { (p, s) }) c
three : Sequential := { alpha := 0.01, beta := 0.01, delta := 0.5, initial := 1, budget := 3 }
ten : Sequential := { alpha := 0.01, beta := 0.01, delta := 0.5, initial := 1, budget := 10 }
ones : List Float64 := [1.0]
on (c : String) : List Binding := [ { parameter := just "p", type := nothing, generator := "ones", coverage := Listed },
  { parameter := just "c", type := nothing, generator := c, coverage := Listed } ]
test "Constant" ExhaustiveMode (seed <- 5) (profile <- on "three")
test "Constant" ExhaustiveMode (seed <- 6) (profile <- on "three")
test "Constant" ExhaustiveMode (seed <- 7) (profile <- on "ten")
'''


def test_the_budget_bounds_the_test_across_stretches_and_a_larger_one_continues_it(tmp_path):
    path = tmp_path / "stretched.test.lut"
    path.write_text(STRETCHED, encoding="utf-8")
    # alone, each line is its own test: unresolved at the budget of 3, held at 7 under 10
    alone = tester.run_tests(path)
    assert [(o.verdict, o.evidence.spent) for o in alone] == [("Unsettled", 3), ("Unsettled", 3), ("Supported", 7)]
    # with the store, one test: the second seed buys no budget, so it stops at 3 in all, unresolved;
    # the line with a budget of 10 continues from the ratio recorded and holds the law at 7 in all
    first, second, third = tester.run_tests(path, store=True)
    assert (first.verdict, first.evidence.spent) == ("Unsettled", 3)
    assert (second.verdict, second.evidence.spent) == ("Unsettled", 0)
    assert second.entry["evidence"]["from"] == {"ratio": 0.125, "spent": 3, "seeds": [5]}
    assert "unresolved at 0 samples of 1" in tester.line(second)
    assert "continuing the test of seed 5 (3 samples in all)" in tester.line(second)
    assert (third.verdict, third.grade, third.evidence.spent) == ("Supported", "Sampled", 4)
    assert third.entry["evidence"]["from"] == {"ratio": 0.125, "spent": 3, "seeds": [5, 6]}
    assert "continuing the test of seeds 5, 6 (7 samples in all)" in tester.line(third)
    # the union is one test whatever the budgets: its key leaves the cutoffs out
    entries = certify.read_store(path)
    key = certify.union_key(third.entry)
    assert key == certify.union_key(first.entry) and [d["parameter"] for d in key if "parameter" in d] == ["p"]
    assert certify.pooled(entries, "Constant", third.cone, key) == 7
    assert certify.standing(entries, "Constant", third.cone).endswith("; pooled over seeds 5, 6, 7: 7 samples in all")
    # a replay starts where its seed's stretch started: the same outcomes, nothing written
    stored = certify.store_path(path).read_text()
    again = tester.run_tests(path, store=True, deep=True)
    assert [(o.verdict, o.evidence.spent) for o in again] == [("Unsettled", 3), ("Unsettled", 0), ("Supported", 4)]
    assert certify.store_path(path).read_text() == stored


def test_the_union_holds_on_the_reference_and_its_controls_refute_the_broken_ones():
    # certification.lth's `Pooling` on certification_model.lut; the controls (L9.14): a union that
    # counts a replay twice, and one that counts only the latest stretch, each refuted
    laws = tester.run_tests(ROOT / "tests" / "tester" / "pooling_laws.test.lut")
    assert [(o.spec.law, o.verdict) for o in laws] == [("TheUnionIsMonotone", "Supported"),
                                                       ("AReplayIsNotANewStretch", "Supported")]
    controls = tester.run_tests(ROOT / "tests" / "tester" / "pooling_controls.test.lut")
    assert [(o.spec.law, o.verdict) for o in controls] == [("TheUnionIsMonotone", "Refuted"),
                                                           ("AReplayIsNotANewStretch", "Refuted")]
    twice, = (o for o in controls if o.spec.law == "AReplayIsNotANewStretch")
    assert "p = counting" in tester.line(twice)


# core bite 12a, item 5: about 1 s an exhaustive case at HEAD (TheThreeSourcesGrade alone, 270 cases,
# 277 s at 8ef6389, 147 s just before it; 132 s at 3e523d5, which wrote the test), most of it
# kernel.substitute on fresh terms; the two files run without a store, so half an hour or more
@pytest.mark.skipif(not os.environ.get("LUTHIER_SLOW"), reason="half an hour or more; set LUTHIER_SLOW=1")
def test_the_regions_hold_on_the_references_and_their_controls_refute_the_broken_ones():
    # record/IA/regions-2026-10-17/prompt-theory.md (D-2026-10-16-i, D-2026-10-16-j): generators.lth's
    # `Degeneracies` on the declared cases of List, Mat and Symmetric; certification.lth's `Regioning`
    # (the weakest, 5.S8's default) and `Deriving` on certification_model.lut; every control refuted
    laws = tester.run_tests(ROOT / "tests" / "tester" / "regions_laws.test.lut")
    assert [o.spec.law for o in laws] == (
        ["EachWitnessIsItsCase"] * 3 + ["CaseNamesAreDistinct"] * 3
        + ["NoRegionsLeaveTheGrade", "RefutedInEveryRegion", "ALabelEntersNoGrade", "AnEmptyRegionLeavesBelowCases",
           "TheThreeSourcesGrade", "CombinesOverRegions", "CombinesAcrossBindings", "Commutative",
           "NothingIsTheUnit", "CombineNeverRaises", "EachCutoffGivesTwoSides", "EachPremiseGivesItsBoundary",
           "OnlyTheLawsRegions"])
    assert all(o.verdict in ("Confirmed", "Supported") for o in laws), [tester.line(o) for o in laws]
    controls = tester.run_tests(ROOT / "tests" / "tester" / "regions_controls.test.lut")
    assert [o.spec.law for o in controls] == ["EachWitnessIsItsCase", "CaseNamesAreDistinct"] + [o.spec.law for o in laws[6:]]
    assert all(o.verdict == "Refuted" for o in controls), [tester.line(o) for o in controls]
    empty, = (o for o in controls if o.spec.law == "AnEmptyRegionLeavesBelowCases")
    assert "q = ignoringEmpty" in tester.line(empty)


def test_theory_type_dependencies_do_not_execute_its_predicate_or_auxiliary_models():
    from luthier.elaborate import elaborate_program
    from luthier.parse import parse
    source = """T : { f : Bool -> Bool }
aux : Bool := true
Law (m : T) (x : Bool) : Bool := m.f x == aux
T := Law
model : T := { f := fn b { b } }
Claim (x : Bool) : Bool := Law model x
"""
    program = elaborate_program(parse(source).program)
    cones = certify.Cones(program)
    assert 'aux' not in cones.names('model')
    called = t.Define('ByTheory', t.Var('Bool'), t.App(t.Var('T'), t.Var('model')))
    assert 'aux' in certify.Cones(program + (called,)).names('ByTheory')
    refined = t.Define('refined', t.Subtype('m', t.Var('T'), t.App(t.App(t.Var('Law'), t.Var('m')), t.Var('true'))), t.Var('model'))
    assert 'aux' in certify.Cones(program + (refined,)).names('refined')
    assert 'aux' in cones.names('Claim')
    declaration_only = tuple(a for a in program if not (isinstance(a, t.Define) and a.name == 'T'))
    assert cones.hash('model') == certify.Cones(declaration_only).hash('model')
    assert cones.hash('Claim') != certify.Cones(tuple(
        t.Define(a.name, a.type, t.Var('false')) if isinstance(a, t.Define) and a.name == 'aux' else a
        for a in program)).hash('Claim')


# ---------------------------------------------------------------------- core bite 12a, item 3
# A theory whose definition is a conjunction is certified as one law, an entry per conjunct
# (D-2026-10-18-f); a run demands each of its laws by its own name (`doubles: Neutral`), and those
# demands are served by the conjuncts' entries (report-verify-6-11.md, failure 2: validate_graph and
# experiment_zero refused on `doubles: Neutral / Absorbing / Involutive / TotalOrder`). `Unital` is a
# law defined as a conjunction, read through to its conjuncts as `TotalOrder` is.

CONJ_THEORY = '''Ops : { plus : Int -> Int -> Int }
Ops (o : Ops) := Commutative Int Int (structural Int) o.plus & Neutral Int (structural Int) o.plus 0 & Unital Int (structural Int) o.plus 0
Unital (A : U) (s : Object A) (op : A -> A -> A) (e : A) := LeftNeutral A s op e & RightNeutral A s op e
'''
CONJ_MODELS = '''import "ops.lth" Ops
ops : Ops := { plus := fn a b { a + b } }
other : Ops := { plus := fn a b { b + a } }
'''
CONJ_TEST = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
import "ops.lut" ops
import "ops.lth" Ops
smallInts : List Int := [0, 1, 2]
onOps : List Binding := [ { parameter := just "o", type := nothing, generator := "ops", coverage := Listed },
  { parameter := nothing, type := just "Int", generator := "smallInts", coverage := Listed } ]
test "Ops" ExhaustiveMode (profile <- onOps)
'''
CONJ_USE = '''import "ops.lut" ops other
three : Int := ops.plus 1 2
four : Int := other.plus 2 2
'''


def test_a_theory_s_laws_are_served_by_its_conjunction_s_entries(tmp_path, capsys):
    for name, text in [("ops.lth", CONJ_THEORY), ("ops.lut", CONJ_MODELS), ("ops.test.lut", CONJ_TEST),
                       ("use.lut", CONJ_USE)]:
        (tmp_path / name).write_text(text, encoding="utf-8")
    main(["certify", str(tmp_path / "ops.test.lut")])
    entries = json.loads((tmp_path / "ops.cert.json").read_text(encoding="utf-8"))
    assert {e["law"] for e in entries} == {"Ops"} and all("conjunct" in e for e in entries)
    capsys.readouterr()
    main(["eval", str(tmp_path / "use.lut"), "three"])
    out = capsys.readouterr().out
    assert "3 : Int" in out and "uncertified" not in out and "1 certified" in out
    # another model of the theory is not served by `ops`'s entries
    main(["eval", str(tmp_path / "use.lut"), "four"])
    out = capsys.readouterr().out
    assert "other: Neutral: uncertified" in out and "other: Unital: uncertified" in out


# The coordinator, 2026-10-22, on report-bite-12a.md's question: a law demanded without a model
# parameter (`Commutative`, `Neutral` over `o.plus`) is served only by entries about the model the run
# gives; a passed entry of the law about another model (core's own `Commutative` lines) no longer
# serves it. A certificate means the model that runs was tested.
CONJ_RUN_OTHER = '''import "ops.lut" other
main (w : W) : W * Unit := if other.plus 2 2 == 4 then (w, unit) else (w, unit)
'''
CONJ_RUN_OPS = CONJ_RUN_OTHER.replace("other", "ops")


def test_a_law_without_a_model_parameter_is_served_only_by_the_run_s_model(tmp_path, capsys):
    for name, text in [("ops.lth", CONJ_THEORY), ("ops.lut", CONJ_MODELS), ("ops.test.lut", CONJ_TEST),
                       ("other.run.lut", CONJ_RUN_OTHER), ("ops.run.lut", CONJ_RUN_OPS)]:
        (tmp_path / name).write_text(text, encoding="utf-8")
    main(["certify", str(tmp_path / "ops.test.lut")])
    capsys.readouterr()
    assert main(["run", str(tmp_path / "ops.run.lut")]) == 0, capsys.readouterr()
    capsys.readouterr()
    assert main(["run", str(tmp_path / "other.run.lut")]) != 0
    err = capsys.readouterr().err
    assert "other: Commutative: uncertified" in err and "other: Neutral: uncertified" in err


# D-2026-10-22-a: a law's controls are the law's; a run on a model needs that model's passes, not
# controls run at that model. `ops` is certified by its passes; the only control refutes `Ops` on
# `wrong`, another model: the law reads controlled and the run on `ops` is not refused.
CONTROL_MODELS = CONJ_MODELS + 'wrong : Ops := { plus := fn a b { a - b } }\n'
CONTROL_TEST = CONJ_TEST.replace('import "ops.lut" ops', 'import "ops.lut" ops wrong') + '''onWrong : List Binding := [ { parameter := just "o", type := nothing, generator := "wrong", coverage := Listed },
  { parameter := nothing, type := just "Int", generator := "smallInts", coverage := Listed } ]
test "Ops" ExhaustiveMode (profile <- onWrong) (control <- true)
'''


def test_a_model_certified_by_its_passes_needs_no_control_at_that_model(tmp_path, capsys):
    for name, text in [("ops.lth", CONJ_THEORY), ("ops.lut", CONTROL_MODELS), ("ops.test.lut", CONTROL_TEST),
                       ("ops.run.lut", CONJ_RUN_OPS)]:
        (tmp_path / name).write_text(text, encoding="utf-8")
    main(["certify", str(tmp_path / "ops.test.lut")])
    out = capsys.readouterr().out
    assert "controlled (refuted on its control" in out and "control of Ops on wrong" in out, out
    entries = json.loads((tmp_path / "ops.cert.json").read_text(encoding="utf-8"))
    controls = [e for e in entries if certify.is_control(e)]
    assert controls and all("wrong" in json.dumps(e["binding"]) for e in controls)
    assert main(["run", str(tmp_path / "ops.run.lut")]) == 0, capsys.readouterr()


# report-bite-12b.md finding 2: a control that binds a library model besides the broken one
# (`doubles`, beside arrays_controls' own wrong `Arrays`) was written to that model's store, so a
# certify of the laws' program never saw it and read the law "uncontrolled ... its controls are at
# another hash of its cone". A control is the law's (D-2026-10-22-a): it lives with the law's file.
WITHK = '''import "ops.lth" Ops
Konst : { v : Int }
OpsWith (o : Ops) (k : Konst) (x : Int) : Bool := o.plus x k.v == o.plus k.v x
'''
KONST = '''import "withk.lth" Konst
konst : Konst := { v := 3 }
'''
WITHK_LAWS = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
import "ops.lut" ops
import "konst.lut" konst
import "withk.lth" OpsWith
smallInts : List Int := [0, 1, 2]
onOps : List Binding := [ { parameter := just "o", type := nothing, generator := "ops", coverage := Listed },
  { parameter := just "k", type := nothing, generator := "konst", coverage := Listed },
  { parameter := nothing, type := just "Int", generator := "smallInts", coverage := Listed } ]
test "OpsWith" ExhaustiveMode (profile <- onOps)
'''
WITHK_CONTROLS = WITHK_LAWS.replace('import "ops.lut" ops\n', 'import "ops.lth" Ops\nminus : Ops := { plus := fn a b { a - b } }\n') \
    .replace('generator := "ops"', 'generator := "minus"').replace('(profile <- onOps)', '(profile <- onOps) (control <- true)')


def test_a_control_binding_another_library_model_is_kept_with_the_law(tmp_path, capsys):
    for name, text in [("ops.lth", CONJ_THEORY), ("ops.lut", CONJ_MODELS), ("withk.lth", WITHK), ("konst.lut", KONST),
                       ("laws.test.lut", WITHK_LAWS), ("controls.test.lut", WITHK_CONTROLS)]:
        (tmp_path / name).write_text(text, encoding="utf-8")
    main(["certify", str(tmp_path / "controls.test.lut")])
    capsys.readouterr()
    assert [e["kind"] for e in certify.read_store(tmp_path / "withk.lth")] == ["Control"]
    assert not certify.store_path(tmp_path / "konst.lut").exists()
    main(["certify", str(tmp_path / "laws.test.lut")])
    out = capsys.readouterr().out
    assert "OpsWith: cases; controlled (refuted on its control" in out, out


# ---------------------------------------------------------------------- bite 13c (the audit of 2026-10-22)

def _points(coverage, evaluated=10):
    return {"Points": {"evaluated": evaluated, "raised": 0, "coverage": coverage, "verdict": "Supported"}}


def test_the_store_reader_refuses_a_grade_the_evidence_does_not_admit(tmp_path):
    """Audit 1.8: `heldAsRun`'s `admits`. Drawn points graded proved break the store's predicate."""
    bad = dict(_entry(), evidence=_points("Drawn 0"), grade="Proved")
    assert certify.store_errors([bad]) and "does not admit" in certify.store_errors([bad])[0]
    for coverage, grade in [("Drawn 0", "Sampled"), ("Listed", "Cases"),
                            ("Exhaustive", "ExhaustiveGrade"), ("Bounded 4", "ExhaustiveGrade")]:
        formed = dict(_entry(), evidence=_points(coverage), grade=grade, budgets=dict.fromkeys(certify.SAMPLED_REQUIRES, 1))
        assert certify.store_errors([formed]) == [], coverage
    # [bite B3] the grade is derived: a sample is sampled, never cases (a drawn coverage admitted both before)
    for coverage, grade in [("Listed", "ExhaustiveGrade"), ("Bounded 4", "Cases"), ("Exhaustive", "Proved"),
                            ("Drawn 0", "Cases")]:
        assert certify.store_errors([dict(_entry(), evidence=_points(coverage), grade=grade)]), coverage
    assert certify.store_errors([dict(_entry(), evidence={"NotRun": "x"}, grade="Cases")])
    (tmp_path / "x.cert.json").write_text(json.dumps([bad]))
    with pytest.raises(certify.StoreError):
        certify.read_store(tmp_path / "x.lut")


def test_the_store_reader_bounds_a_listed_pass_by_its_cases():
    """`heldAsRun`'s census: a pass over listed cases reaches no more values than it evaluated; a
    parameter enumerated whole reaches its support; a pass over an empty domain bounds nothing."""
    def listed(reach, evaluated=2, binding=None):
        return dict(_entry(), evidence=_points("Listed", evaluated), binding=binding or [], reach=reach)
    three = {"parameter": "x", "reach": {"Members": [{"Number": 1}, {"Number": 2}, {"Number": 3}]}}
    assert certify.store_errors([listed([three])])
    assert certify.store_errors([listed([three], evaluated=3)]) == []
    support = {"parameter": "k", "reach": "Support"}
    assert certify.store_errors([listed([support])])
    whole = [{"parameter": "k", "generator": "ExhaustiveMode over (Fin n)", "fingerprint": ""}]
    assert certify.store_errors([listed([support], binding=whole)]) == []
    assert certify.store_errors([listed([three], evaluated=0)]) == []


def test_pruning_keeps_a_current_failure_so_passes_never_restore_the_grade():
    """Audit 1.4 A, spec 6.S15: one failure then four passes of the same law, cone and binding. The
    bounded store keeps the failure, and the law stays without a grade."""
    entries = certify.record([], _entry(seed=0, outcome={"Failed": "x = 1"}, date="2026-10-15T00:00:00+00:00"))
    for k in range(1, 7):
        entries = certify.record(entries, _entry(seed=k, date=f"2026-10-15T00:00:0{k}+00:00"))
    assert 0 in [e["seed"] for e in entries]
    assert certify.certificate_grade(entries, "L", "sha256:a") is None
    assert [e["seed"] for e in certify.prune(entries)] == [6, 5, 4, 3, 0]
    # a stale failure still goes once a current entry exists: only a current refutation refuses
    assert [e["seed"] for e in certify.record(entries, _entry(cone="sha256:b", seed=9))] == [9]


def test_pruning_keeps_a_confirmed_control():
    """A control whose broken model came out confirmed (the control failed) is kept past four refutations."""
    def control(seed, outcome):
        return dict(_entry(seed=seed, date=f"2026-10-15T00:00:0{seed}+00:00"), kind="Control", outcome=outcome, binding=[],
                    grade=None)
    entries = certify.record([], control(0, {"ControlConfirmed": "held"}))
    for k in range(1, 6):
        entries = certify.record(entries, control(k, {"ControlRefuted": f"x = {k}"}))
    assert 0 in [e["seed"] for e in entries]
    assert certify.control_status(entries, "L", "sha256:a").startswith(certify.CONTROL_FAILED)


def test_the_budgets_that_change_the_distribution_are_in_the_identity():
    """Audit 1.4 B, spec 7.S8: `specialMass` and `atomAtZero` change what is drawn, so two runs of one
    seed under different masses are two identities and never pool; the fuel and the tries only cut a
    run and stay out of the identity."""
    budgets = {"tries": 2000, "fuel": 3000000, "specialMass": 0.05, "atomAtZero": 0.01, "coveringAbove": 20000}
    base = dict(entry(seed=3), budgets=budgets)
    for field, value in [("specialMass", 0.45), ("atomAtZero", 0.2), ("coveringAbove", 10)]:
        other = dict(base, budgets=dict(budgets, **{field: value}))
        assert certify.identity(other) != certify.identity(base), field
        assert certify.union_key(other) != certify.union_key(base), field
    for field, value in [("fuel", 10), ("tries", 3)]:
        assert certify.identity(dict(base, budgets=dict(budgets, **{field: value}))) == certify.identity(base), field
    assert set(certify.SAMPLING).isdisjoint(certify.LIMITS)
    # a replay under another mass is recorded beside the first, not absorbed as known
    moved = dict(base, budgets=dict(budgets, specialMass=0.45), date="2026-10-15T00:00:00+00:00")
    store = certify.record(certify.record([], base), moved)
    assert len(store) == 2 and certify.known(store, certify.identity(base)) is base
    # and the two are two distributions: no union of their stretches
    assert len(certify.stretches(store, "L", "sha256:1", certify.union_key(base))) == 1


def _theory_entry(conjunct, outcome="Passed", seed=1, model="M"):
    return {"law": "T", "cone": "hT", "binding": [{"parameter": "m", "generator": "x", "fingerprint": "f"}],
            "seed": seed, "cases": 1, "reach": [{"parameter": "m", "reach": {"Members": [{"Printed": model}]}}],
            "outcome": outcome, "grade": "Cases" if outcome == "Passed" else None, "conjunct": conjunct,
            "conjuncts": ["P M", "Q M"]}


def _by_model(law):
    return {"law": law, "cone": "h" + law, "given": [], "accepts": "Sampled", "fingerprints": {}, "byModel": True,
            "conjunction": {"law": "T", "cone": "hT", "given": [("m", {"Printed": "M"})], "accepts": "Sampled",
                            "fingerprints": {"m": "f"}, "heads": [law]}}


def test_a_law_served_through_its_theory_s_conjuncts_is_refused_by_their_failure():
    """Audit 1.5 A: a pass and a failure of the conjunct `P M` on the run's model, two seeds. The
    demand of `P` served through its theory's conjuncts is refused, as a direct demand would be; a
    failure on another model refuses nothing."""
    passes = [_theory_entry("P M"), _theory_entry("Q M")]
    failed = _theory_entry("P M", {"Failed": "x = 1"}, seed=2)
    cone = [{"name": "n", "provisional": False, "laws": [_by_model("P")]}]
    assert certify.refuse(passes, cone) == []
    refusals = certify.refuse([failed] + passes, cone)
    assert [(r["law"], r["state"]) for r in refusals] == [("P", ("Current", {"Failed": "x = 1"}))]
    assert certify.show_refusal(refusals[0], [failed] + passes) == "n: P: failed at x = 1"
    # the failure of `Q M` does not refuse `P`, nor one on another model
    assert certify.refuse([_theory_entry("Q M", {"Failed": "x"}, seed=2)] + passes, cone) == []
    assert certify.refuse([_theory_entry("P M", {"Failed": "x"}, seed=2, model="N")] + passes, cone) == []
    # a disagreement of the conjunct refuses too
    again = dict(_theory_entry("P M", {"Failed": "x = 1"}), date="2026-10-22T00:00:01+00:00")
    assert certify.refuse([again] + passes, cone)[0]["state"][0] == "Disagrees"


def test_the_witness_of_a_demand_covers_every_obligation():
    """Audit 1.5 B, 3.1: what admits a demand is what a run records. `P` is witnessed by `P M`, `Q` by
    `Q M`; a conjunction's demand by an entry of each conjunct."""
    p, q = _theory_entry("P M"), _theory_entry("Q M")
    assert certify.witness(_by_model("P"), [p, q]) == [p]
    assert certify.witness(_by_model("Q"), [p, q]) == [q]
    assert certify.witness(_by_model("Q"), [p]) is None
    whole = dict(_by_model("T")["conjunction"], law="T")
    del whole["heads"]
    assert certify.witness(whole, [p, q]) == [p, q]
    assert certify.witness(whole, [p]) is None


def test_a_run_records_the_entry_of_every_conjunct_that_served_it(tmp_path, capsys):
    """Audit 1.5 B, L5.6, 8.S8: `ops` is admitted on `Commutative`, `Neutral` and `Unital` through the
    conjuncts of `Ops`; the run's record lists an entry of each conjunct, not the first one thrice."""
    for name, text in [("ops.lth", CONJ_THEORY), ("ops.lut", CONJ_MODELS), ("ops.test.lut", CONJ_TEST),
                       ("ops.run.lut", CONJ_RUN_OPS)]:
        (tmp_path / name).write_text(text, encoding="utf-8")
    main(["certify", str(tmp_path / "ops.test.lut")])
    capsys.readouterr()
    assert main(["run", str(tmp_path / "ops.run.lut")]) == 0, capsys.readouterr()
    entries = json.loads((tmp_path / "ops.cert.json").read_text(encoding="utf-8"))
    conjuncts = {e["conjunct"] for e in entries}
    record = json.loads((tmp_path / "ops.run.json").read_text(encoding="utf-8"))[-1]
    recorded = set(record["certificates"])
    from luthier.run import _entry_hash
    assert {e["conjunct"] for e in entries if _entry_hash(e) in recorded} == conjuncts and len(conjuncts) > 1


# ---------------------------------------------------------------------- bite 13c's follow-up, D-2026-10-22-d

def _law_entry(model, outcome="Passed", seed=1, law="L", cone="hL", conjunct=None):
    e = {"law": law, "cone": cone, "binding": [{"parameter": "m", "generator": "x", "fingerprint": "f" + model}],
         "seed": seed, "cases": 1, "reach": [{"parameter": "m", "reach": {"Members": [{"Printed": model}]}}],
         "outcome": outcome, "grade": "Cases" if outcome == "Passed" else None}
    if conjunct is not None:
        e.update(conjunct=conjunct, conjuncts=["P " + model])
    return e


def _direct(model="M"):
    given = [("m", {"Printed": model})]
    return {"law": "L", "cone": "hL", "given": given, "accepts": "Sampled", "fingerprints": {"m": "f" + model},
            "conjunction": {"law": "T", "cone": "hT", "given": given, "accepts": "Sampled",
                            "fingerprints": {"m": "f" + model}, "heads": ["L"]}}


def test_a_failure_on_another_model_does_not_refuse_a_direct_demand():
    """D-2026-10-22-d: a failure of `L` on N is evidence about N; the run on M, served by its pass, is
    not refused. A failure on M still is."""
    cone = [{"name": "n", "provisional": False, "laws": [_direct()]}]
    on_n = _law_entry("N", {"Failed": "m = N"}, seed=2)
    assert certify.refuse([on_n, _law_entry("M")], cone) == []
    on_m = _law_entry("M", {"Failed": "m = M"}, seed=2)
    assert [r["state"] for r in certify.refuse([on_m, _law_entry("M")], cone)] == [("Current", {"Failed": "m = M"})]
    # the run on N is refused by it
    cone_n = [{"name": "n", "provisional": False, "laws": [_direct("N")]}]
    assert certify.refuse([on_n, _law_entry("N")], cone_n)[0]["state"] == ("Current", {"Failed": "m = N"})


def test_a_failure_on_a_model_of_the_theory_refuses_every_model():
    """D-2026-10-22-d's exception: N passes the theory's defining laws (`T`'s conjunct entries on N, at
    the fingerprint the failure recorded) and fails `L`: `L` does not follow from `T`, and the run on M
    is refused, its line saying why. Without that evidence, or when N fails `T`, the failure stays N's."""
    cone = [{"name": "n", "provisional": False, "laws": [_direct()]}]
    on_n = _law_entry("N", {"Failed": "m = N"}, seed=2)
    n_is_t = _law_entry("N", law="T", cone="hT", conjunct="P N")
    entries = [on_n, n_is_t, _law_entry("M")]
    refusals = certify.refuse(entries, cone)
    assert [(r["law"], r["state"]) for r in refusals] == [("L", ("Current", {"Failed": "m = N"}))]
    line = certify.show_refusal(refusals[0], entries)
    assert line.startswith("n: L: failed at m = N on N, which passes the defining laws of T") and "D-2026-10-22-d" in line
    # N fails the theory: not a model of it, the failure is N's alone
    n_fails_t = _law_entry("N", {"Failed": "x"}, seed=3, law="T", cone="hT", conjunct="P N")
    assert certify.refuse([on_n, n_fails_t, n_is_t, _law_entry("M")], cone) == []
    # the theory's pass was of another version of N (another fingerprint): nothing shows N is a model
    other = dict(n_is_t, binding=[{"parameter": "m", "generator": "x", "fingerprint": "fN2"}])
    assert certify.refuse([on_n, other, _law_entry("M")], cone) == []


# ---------------------------------------------------------------------- wave A, bite A4 (audit 1.3, 5b1a05e)

def test_a_store_listing_two_of_three_conjuncts_serves_nothing():
    """Bite A4: the obligations are the law's conjuncts as its definition states them, carried by the
    demand (`conjuncts`), the entries only evidence. Entries that list two conjuncts of three serve
    the law neither directly nor through its theory, and its certificate has no grade; without the
    law's conjuncts the reader falls back on the listing (run.py does not give them yet)."""
    p, q = _theory_entry("P M"), _theory_entry("Q M")
    whole = dict(_by_model("T")["conjunction"], law="T")
    del whole["heads"]
    assert certify.witness(dict(whole, conjuncts=["P M", "Q M"]), [p, q]) == [p, q]
    assert certify.witness(dict(whole, conjuncts=["P M", "Q M", "R M"]), [p, q]) is None
    assert certify.witness(whole, [p, q]) == [p, q]  # the fallback: the listing
    # through the theory: `P` stands for two conjuncts of `T` headed by `P`, one listed
    by = _by_model("P")
    by["conjunction"]["conjuncts"] = ["P M", "Q M", "P (M M)"]
    assert certify.witness(by, [p, q]) is None
    by["conjunction"]["conjuncts"] = ["P M", "Q M"]
    assert certify.witness(by, [p, q]) == [p]
    # the certificate and the standing read the law's conjuncts too
    assert certify.certificate_grade([p, q], "T", "hT") == "Cases"
    assert certify.certificate_grade([p, q], "T", "hT", conjuncts=["P M", "Q M", "R M"]) is None
    assert certify.standing([p, q], "T", "hT", ["P M", "Q M", "R M"]) == "no entry for its conjunct R M"


def test_the_cones_give_a_law_s_conjuncts_as_the_tester_names_them(tmp_path):
    """Bite A4: `Cones.conjuncts`, what a run's demand is to carry, names each conjunct as the entries
    the tester writes do."""
    for name, text in [("ops.lth", CONJ_THEORY), ("ops.lut", CONJ_MODELS), ("ops.test.lut", CONJ_TEST)]:
        (tmp_path / name).write_text(text, encoding="utf-8")
    outcomes = tester.run_tests(tmp_path / "ops.test.lut", store=False)
    runner, specs, loaded = tester.prepare(tmp_path / "ops.test.lut")
    cones = certify.Cones(runner)
    split = [o for o in outcomes if o.parts]
    assert split
    for o in split:
        assert cones.conjuncts(tester._as_called(loaded, o.spec.law)) == o.parts[0].entry["conjuncts"]


HELDS = [certify.EMPTY_FOLD, certify.NoEntry("a"), certify.NoEntry("b"), certify.FailedObligation("a"),
         certify.FailedObligation("b")] + [certify.HeldAt(g) for g in certify.GRADE_RANK]


def _at_most(m, n):
    return m is None or n is not None and certify.GRADE_RANK[m] <= certify.GRADE_RANK[n]


def test_the_five_operations_keep_the_laws_of_folding():
    """Bite A4: certify.py's `all_of`, `alternative`, `restrict`, `project_grade` and `admit` against the
    laws of certification.lth's `Folding` (§7), on the cases certification_fold.test.lut lists; that
    file certifies the reference and its controls refute three broken models."""
    c, P = certify, certify.project_grade
    for j in HELDS:
        assert c.all_of(c.EMPTY_FOLD, j) == j == c.all_of(j, c.EMPTY_FOLD)
        assert c.alternative(c.EMPTY_FOLD, j) == j == c.alternative(j, c.EMPTY_FOLD)
        assert _at_most(P(c.restrict(j, True, 0)), "Sampled")
        for o in "ab":
            assert P(c.all_of(c.NoEntry(o), j)) is None and P(c.all_of(j, c.NoEntry(o))) is None
            assert c.all_of(c.FailedObligation(o), j) == c.FailedObligation(o) == c.alternative(c.FailedObligation(o), j)
        for n in (0, 1, 7):
            for covers in (True, False):
                assert _at_most(P(c.restrict(j, covers, n)), P(j))
        for g in c.GRADE_RANK:
            assert c.admit(g, j) == (P(j) is not None and c.GRADE_RANK[g] <= c.GRADE_RANK[P(j)])
        for k in HELDS:
            assert _at_most(P(c.all_of(j, k)), P(c.alternative(j, k)))
            for m in HELDS:
                assert c.all_of(c.all_of(j, k), m) == c.all_of(j, c.all_of(k, m))
                assert c.alternative(c.alternative(j, k), m) == c.alternative(j, c.alternative(k, m))
    for g in c.GRADE_RANK:
        assert P(c.restrict(c.HeldAt(g), False, 1)) is None
        for h in c.GRADE_RANK:
            assert c.alternative(c.HeldAt(g), c.HeldAt(h)) == c.HeldAt(c._or_strongest(g, h))
        assert c.alternative(c.NoEntry("a"), c.HeldAt(g)) == c.HeldAt(g) == c.alternative(c.HeldAt(g), c.NoEntry("a"))
    laws = tester.run_tests(ROOT / "tests" / "tester" / "certification_fold.test.lut", store=False)
    assert all(o.verdict in ("Confirmed", "Supported") for o in laws) and len(laws) == 10, [tester.line(o) for o in laws]
    controls = tester.run_tests(ROOT / "tests" / "tester" / "certification_fold_controls.test.lut", store=False)
    assert [o.verdict for o in controls] == ["Refuted"] * 3, [tester.line(o) for o in controls]


def test_the_route_s_obligations_come_from_the_law_and_its_control_is_refuted():
    """Bite A4: `Routing` on certification_model.lut with the obligations the demand carries; the
    control that reads them from the entries' listing (certify.py's reading before) is refuted at the
    store that lists two of `T`'s three conjuncts."""
    laws = tester.run_tests(ROOT / "tests" / "tester" / "certification_route.test.lut", store=False)
    assert all(o.verdict in ("Confirmed", "Supported") for o in laws), [tester.line(o) for o in laws]
    controls = tester.run_tests(ROOT / "tests" / "tester" / "certification_route_controls.test.lut", store=False)
    assert all(o.verdict == "Refuted" for o in controls), [tester.line(o) for o in controls]
    listing = controls[-1]
    assert "witness := fromListing" in tester.line(listing) and '"R M"' in tester.line(listing)


# ---------------------------------------------------------------------- wave A, bite A5 (audit 1.4 C)

def _stretch(conjunct, seed, n=100, statistical=False):
    e = {"law": "T", "cone": "hT", "binding": [{"parameter": "x", "generator": "g", "fingerprint": ""}], "seed": seed,
         "cases": n, "reach": [], "outcome": "Passed", "grade": "Sampled", "conjunct": conjunct, "conjuncts": ["P x", "Q x"],
         "evidence": {"Points": {"evaluated": n, "raised": 0, "coverage": f"(Drawn {seed})", "verdict": "Supported"}},
         "date": "2026-10-23T00:00:00+00:00"}
    if statistical:
        e["evidence"] = {"Tested": {"verdict": "Holds", "alpha": 0.01, "beta": 0.01, "delta": 0.5, "spent": n,
                                    "initial": 50, "budget": 400}, "ratio": 0.5}
    return e


def test_two_conjuncts_stretches_never_pool():
    """Bite A5: the conjunct is part of the pooling key (`union_key`), so the stretches of `P x` and of
    `Q x` under one binding, at seeds 1 and 2, are two unions of one stretch each; and a statistical
    stretch of `Q x` does not continue the test of `P x`. With no caller filtering the entries first."""
    p1, q2 = _stretch("P x", 1), _stretch("Q x", 2)
    entries = [q2, p1]
    assert certify.union_key(p1) != certify.union_key(q2)
    assert certify.pooled(entries, "T", "hT", certify.union_key(p1)) == 100
    assert list(certify.stretches(entries, "T", "hT", certify.union_key(q2))) == [2]
    assert certify.pools(entries, "T", "hT") == []
    p2 = _stretch("P x", 2)
    assert certify.pools([p2] + entries, "T", "hT") == ["P x: pooled over seeds 1, 2: 200 cases in all"]
    ps = _stretch("P x", 1, 30, statistical=True)
    qs = _stretch("Q x", 2, 30, statistical=True)
    cutoffs = {"alpha": 0.01, "beta": 0.01, "delta": 0.5, "initial": 50, "budget": 400}
    assert certify.continuation([ps], qs, cutoffs, "c") is None
    assert certify.continuation([ps], dict(ps, seed=2), cutoffs, "c") == {"ratio": 0.5, "spent": 30, "seeds": [1]}


# ---------------------------------------------------------------------- wave A, bite A6 (audit 1.8)

def _formed(grade="Cases", coverage="Listed", evaluated=2, **fields):
    e = {"law": "L", "cone": "h", "binding": [{"parameter": "x", "generator": "xs (Listed)", "fingerprint": ""}],
         "seed": 7, "cases": 2, "outcome": "Passed" if grade else {"Failed": "x = 1"}, "grade": grade,
         "reach": [{"parameter": "x", "reach": {"Members": [{"Printed": "a"}, {"Printed": "b"}]}}],
         "budgets": dict.fromkeys(certify.SAMPLED_REQUIRES, 1),
         "evidence": {"Points": {"evaluated": evaluated, "raised": 0, "coverage": coverage, "verdict": "Confirmed"}},
         "date": "2026-10-23T00:00:00+00:00"}
    e.update(fields)
    return e


# each a fixture, whether the reader admits it, the field its refusal names, and whether the theory's
# `heldAsRun` reads it (the theory's types give the seed and the budgets, and its entries have no kind)
FORMED = [
    (_formed(), True, None, True),
    (_formed("Proved", evidence={"Cited": "Theorem 3 of the library"}), True, None, True),
    (_formed("Proved", evidence={"Cited": ""}), False, "evidence.Cited", True),
    (_formed("ExhaustiveGrade", "Exhaustive"), True, None, True),
    (_formed("ExhaustiveGrade", "Exhaustive", reach=[{"parameter": "x", "reach": {"Interval": [0.0, 1.0]}}]),
     False, "binding.generator, reach", False),  # the theory reads `enumeratedWhole` here, a hole
    (_formed("ExhaustiveGrade", "(Bounded 3)", reach=[{"parameter": "x", "reach": {"Interval": [0.0, 1.0]}}]), True, None, True),
    (_formed("ExhaustiveGrade", "(Bounded 0)"), False, "binding.generator, reach", True),
    (_formed("Sampled", "(Drawn 7)"), True, None, True),
    (_formed("Sampled", "(Drawn 7)", binding=[{"parameter": "x", "generator": "", "fingerprint": ""}]),
     False, "binding.generator", True),
    (_formed("Sampled", "(Drawn 7)", seed=None), False, "seed", False),
    (_formed("Sampled", "(Drawn 7)", budgets={"fuel": 10}), False, "budgets", False),
    (_formed(None, kind="Control", outcome={"ControlRefuted": "x = a"}), True, None, False),
    (_formed(None, kind="Control", outcome={"ControlRefuted": "x = a"},
             binding=[{"parameter": "x", "generator": "", "fingerprint": ""}]), False, "binding.generator", False),
]


def test_each_evidence_form_is_refused_without_its_fields():
    """Bite A6: a fixture per form, refused with a message naming the field; the well formed ones read."""
    for e, ok, field, _ in FORMED:
        errors = certify.store_errors([e])
        assert (errors == []) == ok, (e, errors)
        if field is not None:
            assert any(f"({field})" in m for m in errors), errors


def _lut_value(v):
    return f'Number {float(v["Number"])!r}' if "Number" in v else f'Printed {json.dumps(v["Printed"])}'


def _lut_reach(r):
    if r == "Support":
        return "Support"
    (k, w), = r.items()
    if k == "Interval":
        return f"Interval {float(w[0])!r} {float(w[1])!r}"
    return "Members [" + ", ".join(_lut_value(v) for v in w) + "]"


def _lut_entry(e):
    ev = e["evidence"]
    if "Cited" in ev:
        evidence = f'Cited {json.dumps(ev["Cited"])}'
    else:
        c = ev["Points"]["coverage"].strip("()")
        cov = c if " " not in c else f"({c})"
        point = '(true, Cited "p")'
        evidence = f'Points Bool [{", ".join([point] * ev["Points"]["evaluated"])}] {cov}'
    binding = ", ".join(f'{{ parameter := {json.dumps(d["parameter"])}, generator := {json.dumps(d["generator"])}, '
                        f'fingerprint := "" }}' for d in e["binding"])
    reach = ", ".join(f'{{ parameter := {json.dumps(r["parameter"])}, reach := {_lut_reach(r["reach"])} }}' for r in e["reach"])
    grade = f'just {e["grade"]}' if e["grade"] else "nothing"
    outcome = "Passed" if e["outcome"] == "Passed" else f'Failed {json.dumps(e["outcome"]["Failed"])}'
    return (f'{{ law := "L", cone := "h", binding := [{binding}], seed := 7, cases := {e["cases"]}, conjunct := nothing, '
            f'conjuncts := nil, budgets := defaultBudgets, reach := [{reach}], evidence := {evidence}, grade := {grade}, '
            f'outcome := {outcome}, date := "2026-10-23", interpreter := "listed", hosts := nil }}')


def test_the_theory_s_held_as_run_and_the_reader_agree(tmp_path):
    """Bite A6: certification.lth's `heldAsRun` (with `formedAsItsEvidence`) and certify.py's
    `store_errors` agree on every fixture the theory can state (the others are the reader's alone)."""
    stated = [(e, ok) for e, ok, _, theory in FORMED if theory]
    laws = "".join(f"Agrees{k} : Bool := heldAsRun [{_lut_entry(e)}] == {'true' if ok else 'false'}\n"
                   f'test "Agrees{k}" ExhaustiveMode\n' for k, (e, ok) in enumerate(stated))
    (tmp_path / "formed.test.lut").write_text('''import "test.lth" test ExhaustiveMode Grade Proved ExhaustiveGrade Cases Sampled defaultBudgets
import "laws.lth" Listed Exhaustive Bounded Drawn Points Cited
import "certification.lth" Entry heldAsRun Members Printed Number Support Interval Passed Failed

''' + laws, encoding="utf-8")
    outs = tester.run_tests(tmp_path / "formed.test.lut", store=False)
    assert len(outs) == len(stated)
    assert all(o.verdict in ("Confirmed", "Supported") for o in outs), [tester.line(o) for o in outs]


def test_the_latest_in_front_is_the_order_written():
    """The coordinator's answer of 2026-10-23: the store's order is the order written, and a date is
    when a run started. An entry dated before the one behind it is no error, and `record` puts a new
    entry in front of the store as it was."""
    late, early = entry(seed=1), dict(entry(seed=2), date="2026-10-13T00:00:00+00:00")
    assert certify.store_errors([early, late]) == []
    assert certify.record([late], early) == [early, late]


# ---------------------------------------------------------------------- bite B1: ε̂ at serve time

TAPE = ROOT / "docs" / "concepts" / "tape.test.lut"


def _drawn(n, seed=1, conjunct=None, law="L", regions=None):
    e = {"law": law, "cone": "h", "binding": [{"parameter": "x", "generator": "SampledMode", "fingerprint": "d"}],
         "seed": seed, "cases": n, "reach": [], "outcome": "Passed", "grade": "Sampled",
         "evidence": {"Points": {"evaluated": n, "raised": 0, "coverage": f"(Drawn {seed})", "verdict": "Supported"}}}
    if conjunct is not None:
        e.update(conjunct=conjunct, conjuncts=["P", "Q"])
    if regions is not None:
        e["regions"] = [{"region": {"source": "FromLaw", "name": r}, "n": k} for r, k in regions.items()]
    return e


def test_epsilon_hat_is_the_rule_of_three_and_sound():
    """L10.3, 7.S11: min(1, −log δ / n), 1 with nothing drawn; (1 − ε̂)^n ≤ δ (`SoundAtNoFailure`)."""
    assert f"{certify.epsilon_hat(200, 0.05):.2g}" == "0.015"
    assert certify.epsilon_hat(0, 0.05) == 1.0 and certify.epsilon_hat(2, 0.05) == 1.0
    for n in (1, 3, 10, 200, 10_000):
        for delta in (0.01, 0.05, 0.5, 1.0):
            e = certify.epsilon_hat(n, delta)
            assert e >= 1.0 or (1.0 - e) ** n <= delta


def test_a_sampled_pass_gives_its_pair_at_the_demand_s_delta_and_the_union_s_n():
    """Bite B1: ε̂ from the pooled n (two seeds of 100 are one sample of 200), at the δ asked, stored
    nowhere; an exact pass gives (0, 0); the composition is the capped sum by default."""
    a, b = _drawn(100, seed=1), _drawn(100, seed=2)
    pair = certify.entry_evidence(a, [a, b], 0.05)
    assert pair == (certify.epsilon_hat(200, 0.05), 0.05)
    assert certify.entry_evidence(a, [a, b], 0.01)[0] > pair[0]
    assert "failure" not in a and "risk" not in a  # nothing written in the entry
    exact = dict(_drawn(5), grade="Cases",
                 evidence={"Points": {"evaluated": 5, "raised": 0, "coverage": "Listed", "verdict": "Supported"}})
    assert certify.entry_evidence(exact, [exact]) == certify.UNIT
    assert certify.compose([(0.1, 0.1), (0.1, 0.1)]) == (0.2, 0.2)
    assert certify.compose([(0.1, 0.1), (0.1, 0.1)], "productComposition") == pytest.approx((0.19, 0.19))
    # per region, each from its own cases
    r = _drawn(200, regions={"x boundary": 13})
    assert certify.region_evidence([r], r) == {"x boundary": (13, certify.epsilon_hat(13, 0.05))}


def test_the_tape_example_reports_its_epsilon_per_conjunct():
    """Bite B1's acceptance (docs/concepts.md 6.4): ε̂ = 0.015 at δ = 0.05 for 200 cases per conjunct."""
    shown = dict(certify.standings(TAPE))
    assert "ε̂ 0.015 at δ 0.05 in each of 4 conjuncts (200 cases)" in shown["Tape"], shown
    assert "composed by the capped sum" in shown["Tape"]


def test_the_demand_carries_delta_and_its_composition(tmp_path):
    """Bite B1, L5.19: δ has a declared default; the product composes only with its axiom accepted."""
    from luthier.run import RunError, demand_of
    d = demand_of()
    assert (d.delta, d.composition) == (0.05, "cappedSumComposition")
    rec = demand_of(delta=0.01).record("sha256:c")
    assert (rec["delta"], rec["composition"]) == (0.01, "cappedSumComposition")
    with pytest.raises(RunError):
        demand_of(composition="productComposition")
    assert demand_of(composition="productComposition", assumes=["FailuresIndependent"]).composition == "productComposition"
    with pytest.raises(RunError):
        demand_of(delta=0.0)


def test_a_run_records_the_evidence_of_its_cone(tmp_path, capsys):
    """Bite B1: the run's certification carries the pair of its cone at its δ, by its composition."""
    for name, text in [("ops.lth", CONJ_THEORY), ("ops.lut", CONJ_MODELS), ("ops.test.lut", CONJ_TEST),
                       ("ops.run.lut", CONJ_RUN_OPS)]:
        (tmp_path / name).write_text(text, encoding="utf-8")
    main(["certify", str(tmp_path / "ops.test.lut")])
    capsys.readouterr()
    assert main(["run", str(tmp_path / "ops.run.lut"), "--delta", "0.01"]) == 0, capsys.readouterr()
    record = json.loads((tmp_path / "ops.run.json").read_text(encoding="utf-8"))[-1]
    evidence = record["certification"]["evidence"]
    assert (evidence["delta"], evidence["composition"]) == (0.01, "cappedSumComposition")
    # the conjuncts of `Ops` passed over listed cases: exact, so the cone knows (0, 0)
    assert (evidence["failure"], evidence["risk"]) == (0.0, 0.0) and evidence["links"]
    assert record["demand"]["delta"] == 0.01


# ---------------------------------------------------------------------- bite B3: the grade as a projection

def _live_stores():
    import subprocess
    listed = subprocess.run(["git", "-C", str(ROOT), "ls-files", "*.cert.json"], capture_output=True, text=True,
                            check=True).stdout.split()
    return [ROOT / f for f in listed if not f.startswith("record/")]


def test_every_stored_grade_is_the_derived_one():
    """Bite B3's reader check (L10.2): over every store of the tree, each pass's grade is the
    projection of its evidence's (domain, cost), and every store keeps its predicate."""
    checked = 0
    for where in _live_stores():
        entries = json.loads(where.read_text(encoding="utf-8"))
        assert certify.store_errors(entries) == [], where
        for e in entries:
            if e.get("grade") is not None:
                assert certify.derived_grade(e.get("evidence")) == e["grade"], (where, e["law"], e.get("conjunct"))
                checked += 1
    assert checked > 1000


def test_the_grade_is_the_projection_of_domain_and_cost():
    """certification.lth's `strengthOf` and `gradeOfStrength` (L10.2): one grade per evidence."""
    def points(coverage):
        return {"Points": {"evaluated": 3, "raised": 0, "coverage": coverage, "verdict": "Supported"}}
    assert certify.strength(points("(Drawn 7)")) == ("DistributionDomain", "StatisticalCost")
    assert certify.derived_grade(points("(Drawn 7)")) == "Sampled"
    assert certify.derived_grade(points("Listed")) == "Cases"
    assert certify.derived_grade(points("Exhaustive")) == "ExhaustiveGrade"
    assert certify.derived_grade(points("(Bounded 4)")) == "ExhaustiveGrade"
    assert certify.derived_grade({"Cited": "a theorem"}) == "Proved"
    assert certify.derived_grade("Assumed") == "AssumedGrade"
    assert certify.derived_grade({"Tested": {"verdict": "Holds"}}) == "Sampled"
    assert certify.derived_grade({"NotRun": "why"}) is None
    # a sample no longer admits cases, nor an enumeration cases: the grade is derived, not chosen
    assert not certify.admits(points("(Drawn 7)"), "Cases") and not certify.admits(points("Exhaustive"), "Cases")


def test_a_run_records_its_cone_s_grades_beside_the_weakest(tmp_path, capsys):
    """Bite B3: the vector of the cone's grades and their combination by the demand's `combine`."""
    for name, text in [("ops.lth", CONJ_THEORY), ("ops.lut", CONJ_MODELS), ("ops.test.lut", CONJ_TEST),
                       ("ops.run.lut", CONJ_RUN_OPS)]:
        (tmp_path / name).write_text(text, encoding="utf-8")
    main(["certify", str(tmp_path / "ops.test.lut")])
    capsys.readouterr()
    assert main(["run", str(tmp_path / "ops.run.lut")]) == 0, capsys.readouterr()
    certification = json.loads((tmp_path / "ops.run.json").read_text(encoding="utf-8"))[-1]["certification"]
    assert certification["grades"] and {g["grade"] for g in certification["grades"]} == {"cases"}
    assert certification["grade"] == "cases"
