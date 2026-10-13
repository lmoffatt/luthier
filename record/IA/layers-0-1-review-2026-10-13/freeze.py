"""Freeze the three bundles of the layers 0-1 review: copy the files, and extract from
record/decisions.md the entries the bundle's files cite. Run from the repository root:
python3 record/IA/layers-0-1-review-2026-10-13/freeze.py. Records the commit in each bundle."""
import re, shutil, subprocess
from pathlib import Path

HERE = Path(__file__).parent
LIB = Path("src/luthier/lib")
SPEC = Path("docs/spec")
BUNDLES = {
    "A": [LIB / "kernel_laws.lth", LIB / "kernel_models.lut", LIB / "term.lth", LIB / "term_model.lut",
          SPEC / "03-kernel.md"],
    "B": [LIB / "grammar.lth", LIB / "term.lth", LIB / "translation.lth", LIB / "program.lth",
          SPEC / "02-grammar.md", SPEC / "04-static-semantics.md"],
    "C": [LIB / "laws.lth", LIB / "checks.lth", LIB / "checks_model.lut", LIB / "library.lth",
          SPEC / "05-laws.md", SPEC / "12-files-and-tools.md"],
}
DID = re.compile(r"D-\d{4}-\d{2}-\d{2}-[a-z]{1,2}")

def entries(ids):
    text = Path("record/decisions.md").read_text(encoding="utf-8")
    out = []
    for i in sorted(ids):
        m = re.search(rf"^{re.escape(i)}\s.*?(?=^\S|\Z)", text, re.M | re.S)
        if m:
            block = m.group(0)
            more = re.search(r"\A.*?(?=\n\n|\Z)", text[m.start():], re.S)
            out.append(more.group(0) if more else block)
    return "\n\n".join(out)

commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
for name, files in BUNDLES.items():
    b = HERE / name / "bundle"
    if b.exists():
        shutil.rmtree(b)
    b.mkdir(parents=True)
    ids = set()
    for f in files:
        dest = b / (f.name + ".txt" if f.suffix in (".lth", ".lut") else f.name)
        shutil.copy(f, dest)
        if f.suffix in (".lth", ".lut"):
            ids |= set(DID.findall(f.read_text(encoding="utf-8")))
    shutil.copy("docs/principles.md", b / "principles.md")
    (b / "decisions-cited.md").write_text(
        f"# Decisions cited by the files of bundle {name}\n\nFrom record/decisions.md at {commit}.\n\n"
        + entries(ids) + "\n", encoding="utf-8")
    (b / "FROZEN").write_text(f"{commit}\n", encoding="utf-8")
    print(name, len(list(b.iterdir())), "files,", len(ids), "decisions")
