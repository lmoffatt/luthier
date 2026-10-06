"""scripts/check_spec_tests.py on a small specification and test folder of its own (step 4.2 of
docs/plan-working-method-execution-2026-10-06.md)."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_spec_tests.py"

SPEC = """\
# Static semantics

## 4. Dependence

**R99. A rule outside section 5 is not a rule.** It has no tests and is not reported.

## 5. Well-formedness rules

**R1. Both kinds.** A rule with an accepted and a rejected program.
Files: `r1_both.accept.lut`, `r1_both.reject.lut`.

### 5.1 A subsection

Text after a heading belongs to no rule, even if it says not implemented.

**R2. Only accept.** A rule with an accepted program and no rejected one.
Files: `r2_only.accept.lut`.

**R3. Marked open** (decided today; not
implemented). The words are split across two lines.
Files: to be written with the implementation.

## 6. Reports that do not reject

**R4. After section 5.** Not a rule of section 5.
"""


def run(spec: Path, tests: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), "--spec", str(spec), "--tests", str(tests)],
                          capture_output=True, text=True, cwd=spec.parent)


def build(tmp_path: Path, spec: str, files: list[str]) -> tuple[Path, Path]:
    spec_path = tmp_path / "05-static-semantics.md"
    spec_path.write_text(spec, encoding="utf-8")
    tests = tmp_path / "spec"
    tests.mkdir()
    for name in files:
        (tests / name).write_text("-- a program\n", encoding="utf-8")
    return spec_path, tests


def line_of(spec: str, prefix: str) -> int:
    return next(i for i, l in enumerate(spec.splitlines(), 1) if l.startswith(prefix))


def test_findings(tmp_path):
    spec, tests = build(tmp_path, SPEC, ["r1_both.accept.lut", "r1_both.reject.lut",
                                         "r1_more.accept.lut", "r2_only.accept.lut",
                                         "r2_helper.lut"])
    result = run(spec, tests)
    lines = result.stdout.splitlines()

    assert result.returncode == 1, result.stderr
    assert lines == [
        f"05-static-semantics.md:{line_of(SPEC, '**R2.')}: spec-tests: R2 (Only accept) has no "
        f"reject test: no r2_*.reject.lut in spec",
        f"05-static-semantics.md:{line_of(SPEC, '**R3.')}: spec-tests: R3 (Marked open) is "
        f"marked not implemented",
    ]


def test_a_rule_with_both_kinds_passes(tmp_path):
    spec_text = SPEC.split("**R2.")[0] + "## 6. End\n"
    spec, tests = build(tmp_path, spec_text, ["r1_both.accept.lut", "r1_both.reject.lut"])
    result = run(spec, tests)

    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout == ""


def test_a_rule_with_no_tests(tmp_path):
    spec, tests = build(tmp_path, SPEC, [])
    result = run(spec, tests)

    assert result.returncode == 1
    assert "R1 (Both kinds) has no tests: no r1_*.accept.lut and no r1_*.reject.lut" in result.stdout
    assert "R3 (Marked open) is marked not implemented" in result.stdout
    assert "R3 (Marked open) has no" not in result.stdout


def test_no_section_5_is_an_error(tmp_path):
    spec, tests = build(tmp_path, "# Nothing\n\n**R1. Outside.** Text.\n", [])
    result = run(spec, tests)

    assert result.returncode == 2
    assert "no rules" in result.stderr
