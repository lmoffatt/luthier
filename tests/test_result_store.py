"""The store of results across runs at its smallest (v0.4's criterion c; 8.S3, 8.S8, 8.S10;
D-2026-10-15-d, D-2026-10-15-h; L5.20): `run` writes the value of a pure entry under its key in
`x.results.json`, a later run with that key is served without evaluating, an acting run always
executes, `--fresh` executes whatever the store holds. Written 2026-10-16 by Claude Opus 5.5, an
agent of the coordinating session, on record/IA/code-follows-2026-10-16/prompt-store.md."""
import json
from pathlib import Path

from luthier.cli import main
from luthier.run import key_hash, read_results, record_path, result_key, results_path, served_by

ROOT = Path(__file__).resolve().parents[1]

PURE = "a : Int := 1 + 2\nn : Int\nmain : Int := a * n\n"


def _pure(tmp_path):
    path = tmp_path / "pure.lut"
    path.write_text(PURE, encoding="utf-8")
    return path


def _runs(path):
    return json.loads(record_path(path).read_text(encoding="utf-8"))


def test_a_pure_entry_run_twice_is_served_the_second_time(tmp_path, capsys):
    path = _pure(tmp_path)
    assert main(["run", str(path), "--set", "n=4"]) == 0
    assert main(["run", str(path), "--set", "n=4"]) == 0
    first, second = _runs(path)
    assert first["result_store"] == {"pure": True, "fresh": False, "written": 0}
    assert first["fuel"]["spent"] > 0
    # the second names the entry the first wrote, by its index, key hash and the first's time
    served = second["result_store"]["served"]
    assert (served["entry"], served["key hash"], served["time"]) == (0, first["key_hash"], first["time"])
    assert second["fuel"]["spent"] == 0 and second["key_hash"] == first["key_hash"]
    assert [(r["value"], r["time"]) for r in read_results(path)] == [("12", first["time"])]
    assert "served from pure.results.json, entry 0" in capsys.readouterr().err


def test_an_acting_entry_always_executes(tmp_path, capsys):
    # hello.run.lut's cone prints (W): executed twice, nothing stored (D-2026-10-15-d)
    path = tmp_path / "hello.run.lut"
    path.write_text((ROOT / "examples/hello.run.lut").read_text(encoding="utf-8"), encoding="utf-8")
    assert main(["run", str(path)]) == 0
    assert main(["run", str(path)]) == 0
    assert capsys.readouterr().out == "hello, world\nhello, world\n"
    runs = _runs(path)
    assert [r["result_store"] for r in runs] == [{"pure": False, "fresh": False}] * 2
    assert all(r["fuel"]["spent"] > 0 for r in runs)
    assert not results_path(path).exists()
    # each run records the hash of the bytes of every certificate store it read, beside files_read
    stores = runs[0]["stores_read"]
    assert any(Path(p).name == "world_model.cert.json" for p, _ in stores)
    assert all(h.startswith("sha256:") for _, h in stores)
    assert all(h.startswith("sha256:") for h in runs[0]["certificates"])


def test_fresh_executes_and_writes_nothing_when_it_agrees(tmp_path, capsys):
    path = _pure(tmp_path)
    assert main(["run", str(path), "--set", "n=4"]) == 0
    assert main(["run", str(path), "--set", "n=4", "--fresh"]) == 0
    first, fresh = _runs(path)
    assert fresh["result_store"] == {"pure": True, "fresh": True, "agrees": 0}
    assert fresh["fuel"]["spent"] > 0
    assert len(read_results(path)) == 1
    assert "--fresh: the value agrees with entry 0" in capsys.readouterr().err


def test_fresh_keeps_both_when_it_disagrees_and_the_key_is_then_not_served(tmp_path, capsys):
    # as an exact replay of a certificate that disagrees (D-2026-10-15-f): both kept, said, and the
    # key served no more until the discrepancy is resolved (ResultsDetermined broken)
    path = _pure(tmp_path)
    assert main(["run", str(path), "--set", "n=4"]) == 0
    results = read_results(path)
    results[0]["value"] = "13"
    results_path(path).write_text(json.dumps(results), encoding="utf-8")
    assert main(["run", str(path), "--set", "n=4", "--fresh"]) == 0
    assert _runs(path)[-1]["result_store"] == {"pure": True, "fresh": True, "written": 1, "disagrees": [0]}
    assert [r["value"] for r in read_results(path)] == ["13", "12"]
    assert "differs from entries [0] under the same key; both kept" in capsys.readouterr().err
    assert main(["run", str(path), "--set", "n=4"]) == 0
    last = _runs(path)[-1]
    assert "served" not in last["result_store"] and last["result_store"]["agrees"] == 1
    assert len(read_results(path)) == 2


def test_a_run_whose_fuel_differs_is_still_served(tmp_path, capsys):
    # D-2026-10-15-g: fuel is in the record and out of the key
    path = _pure(tmp_path)
    assert main(["run", str(path), "--set", "n=4", "--fuel", "5000"]) == 0
    assert main(["run", str(path), "--set", "n=4", "--fuel", "7000"]) == 0
    first, second = _runs(path)
    assert (first["demand"]["fuel"], second["demand"]["fuel"]) == (5000, 7000)
    assert second["result_store"]["served"]["entry"] == 0


def test_a_hole_the_cone_reads_changes_the_key(tmp_path, capsys):
    path = _pure(tmp_path)
    assert main(["run", str(path), "--set", "n=4"]) == 0
    assert main(["run", str(path), "--set", "n=5"]) == 0
    first, second = _runs(path)
    assert second["key_hash"] != first["key_hash"] and "served" not in second["result_store"]
    assert [r["value"] for r in read_results(path)] == ["12", "15"]


def test_the_key_is_a_function_of_the_record(tmp_path, capsys):
    # plan.lth's KeyIsOfTheRecord: the key's hash recorded is that of `keyOf` of the record, its
    # seed, its plan and its certificates; the fuel, the time and the lock are not in it
    path = _pure(tmp_path)
    assert main(["run", str(path), "--set", "n=4"]) == 0
    r = _runs(path)[0]
    assert key_hash(result_key(r, r["seed"], r["plan"], r["certificates"])) == r["key_hash"]
    other = dict(r, demand=dict(r["demand"], fuel=1, lock="v0.0"), time="1970-01-01T00:00:00+00:00")
    assert key_hash(result_key(other, r["seed"], r["plan"], r["certificates"])) == r["key_hash"]
    # and it sees the seed, the cone and the certificates
    assert key_hash(result_key(r, 7, r["plan"], r["certificates"])) != r["key_hash"]
    assert key_hash(result_key(dict(r, demand=dict(r["demand"], cone="sha256:0")), r["seed"], r["plan"],
                               r["certificates"])) != r["key_hash"]
    assert key_hash(result_key(r, r["seed"], r["plan"], ["sha256:1"])) != r["key_hash"]


def test_controls_an_entry_whose_key_differs_in_one_field_does_not_serve(tmp_path, capsys):
    # L9.14: a store that would serve an entry whose key differs from the run's in the seed or the
    # cone is refused; both as an honest entry (stored under its own key's hash) and as a forged one
    # (stored under the run's key hash)
    path = _pure(tmp_path)
    assert main(["run", str(path), "--set", "n=4"]) == 0
    entry = read_results(path)[0]
    key = entry["key"]
    assert served_by([entry], key) == 0
    for field_name, other in (("seed", 7), ("cone", "sha256:0")):
        changed = dict(key, **{field_name: other})
        honest = dict(entry, key=changed, **{"key hash": key_hash(changed)})
        forged = dict(entry, key=changed)
        assert served_by([honest], key) is None and served_by([forged], key) is None
        results_path(path).write_text(json.dumps([honest, forged]), encoding="utf-8")
        assert main(["run", str(path), "--set", "n=4"]) == 0
        assert "served" not in _runs(path)[-1]["result_store"]
