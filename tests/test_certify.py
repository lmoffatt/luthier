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
LAWS = ROOT / "tests" / "tester" / "laws.lut"
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
    return {"law": law, "cone": cone, "binding": list(binding), "seed": seed, "cases": 100, "budgets": {},
            "reach": [], "evidence": {"Points": {"evaluated": 100}}, "grade": grade, "outcome": outcome,
            "date": "2026-10-14T00:00:00+00:00", "interpreter": "abc", "hosts": []}


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
    assert certify.record(es, entry(outcome={"Failed": "x = 1"}, grade=None)) is es  # a known identity
    assert len(certify.record(es, entry(seed=5))) == 2                                # a new seed


def test_the_store_predicate_is_checked(tmp_path):
    path = tmp_path / "x.lut"
    with pytest.raises(certify.StoreError, match="one identity, two outcomes"):
        certify.write_store(path, [entry(), entry(outcome={"NotRunFor": "fuel"}, grade=None)])
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
    path = tmp_path / "laws.lut"
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
    assert after[len(after) - len(before):] == before  # the stale entries are kept
    assert dict(certify.standings(laws))["Small"] == "sampled"


def test_the_entry_holds_what_certification_lth_names(laws):
    tester.run_tests(laws, store=True)
    e = next(e for e in certify.read_store(laws) if e["law"] == "PlusCommutes" and e["seed"] == 7)
    assert set(e) == {"law", "cone", "binding", "seed", "cases", "budgets", "reach", "evidence", "grade",
                      "outcome", "date", "interpreter", "hosts"}
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
    assert "certificate NotInvolutive: exhaustive" in out and "certificate Small: refuted at x = 729" in out


# ---------------------------------------------------------------------- luthier certify (12.S16)

def test_certify_several_files(tmp_path, capsys):
    paths = []
    for name in ("laws.lut", "weakest.lut"):
        shutil.copy(ROOT / "tests" / "tester" / name, tmp_path / name)
        paths.append(str(tmp_path / name))
    assert main(["certify", "--jobs", "2", *paths]) == 1  # laws.lut has refuted laws
    out = capsys.readouterr().out.splitlines()
    assert out[0] == f"{paths[0]}: 4 laws, 6 lines ran, 0 known"
    assert "  NotInvolutive: exhaustive" in out and "  PlusCommutes: sampled" in out
    assert "  Small: refuted at x = 729" in out and "  AndIsOr: refuted at a = true, b = false" in out
    # weakest.lut: one law under two bindings, the weakest
    assert out[out.index(f"{paths[1]}: 1 laws, 2 lines ran, 0 known") + 1] == "  NotInvolutive: cases"
    assert main(["certify", paths[1]]) == 0
    assert capsys.readouterr().out.splitlines()[0] == f"{paths[1]}: 1 laws, 0 lines ran, 2 known"


@pytest.mark.skipif(not os.environ.get("LUTHIER_SLOW"), reason="a few minutes; set LUTHIER_SLOW=1")
def test_certify_the_laws_of_numbers(tmp_path, capsys):
    path = tmp_path / "numbers_laws.lut"
    shutil.copy(ROOT / "tests" / "tester" / "numbers_laws.lut", path)
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
    path = tmp_path / "census.lut"
    path.write_text(CENSUS, encoding="utf-8")
    [outcome] = tester.run_tests(path, store=True)
    e = outcome.entry
    assert e["outcome"] == "Passed"
    assert e["reach"] == [
        {"parameter": "t", "reach": {"Members": [{"Number": 1.0e-3}]}},
        {"parameter": "s", "reach": {"Members": [{"Printed": '"a"'}, {"Printed": '"b"'}]}},
        {"parameter": "x", "reach": {"Interval": [-10.0, 10.0]}}]
    assert [d["generator"] for d in e["binding"][:2]] == ["tol (Listed)", "names (Listed)"]
    assert e["binding"][0]["fingerprint"].startswith("sha256:") and e["binding"][2]["fingerprint"] == ""
