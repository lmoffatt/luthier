"""Assemble the layer-3 review prompt (world and certification) as one inlined paste.
Run from the repository root: python3 record/IA/layer-3-review-2026-10-15/freeze.py
Inputs: the six files below at the current HEAD, docs/principles.md (Terms, L2.7, L9.6, L10, L11),
record/decisions.md (entries the files cite). No parameters, no randomness. Writes A-prompt.md
and FROZEN. Commit the inputs first; the commit is recorded in FROZEN and in the prompt's header."""
import re, subprocess
from pathlib import Path

HERE = Path(__file__).parent
LIB, SPEC = Path("src/luthier/lib"), Path("docs/spec")
FILES = [LIB/"world.lth", LIB/"world_model.lut", LIB/"certification.lth", LIB/"certification_model.lut",
         SPEC/"10-world.md", SPEC/"06-certification.md"]
DID = re.compile(r"D-\d{4}-\d{2}-\d{2}-[a-z]{1,2}")
commit = subprocess.run(["git","rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()

def entries(ids):
    text = Path("record/decisions.md").read_text(encoding="utf-8"); out=[]
    for i in sorted(ids):
        m = re.search(rf"^{re.escape(i)}\s", text, re.M)
        if m:
            out.append(re.match(r".*?(?=\n\n|\Z)", text[m.start():], re.S).group(0))
    return "\n\n".join(out)

P = Path("docs/principles.md").read_text(encoding="utf-8").split("\n")
def lines(a,b): return "\n".join(P[a-1:b])
def clause(prefix):
    for k,l in enumerate(P):
        if l.startswith(prefix+" "):
            j=k+1
            while j<len(P) and P[j].startswith("  "): j+=1
            return "\n".join(P[k:j])
    return ""
terms = lines(18, 70)
princ = "\n\n".join([terms, clause("- L2.7"), clause("- L9.6"),
    "\n".join(l for l in P if l.startswith("**L10.")), lines(511,560),
    "\n".join(l for l in P if l.startswith("**L11.")), clause("- L11.1"), clause("- L11.2"),
    "- P11 Every criterion is a parameter, never a constant in the code."])
ids=set()
for f in FILES:
    if f.suffix in (".lth",".lut"): ids |= set(DID.findall(f.read_text(encoding="utf-8")))
    else: ids |= set(DID.findall(f.read_text(encoding="utf-8")))
def fence(f):
    return f"### `{f.name}`\n\n````\n{f.read_text(encoding='utf-8').rstrip()}\n````\n"
head = (HERE/"A-head.md").read_text(encoding="utf-8").replace("@COMMIT@", commit[:7])
body = head + "\n\n---\n\n## Material\n\nFrozen at commit " + commit[:7] + ".\n\n" \
  + "### Principles (excerpt of `docs/principles.md`)\n\n" + princ + "\n\n" \
  + "### Decisions the files cite (from `record/decisions.md`)\n\n" + entries(ids) + "\n\n" \
  + "\n".join(fence(f) for f in FILES)
(HERE/"A-prompt.md").write_text(body, encoding="utf-8")
(HERE/"FROZEN").write_text(commit+"\n", encoding="utf-8")
print(len(body.split()), "words")
