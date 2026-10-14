"""Assemble the layer-3 review prompts as inlined pastes, one per bundle.
Run from the repository root: python3 record/IA/layer-3-review-2026-10-15/freeze.py [A] [B] [C] [D]
(default: B C D; A was frozen at 055589c and is regenerated only if named, which would re-freeze it at HEAD).
Bundle A: world and certification. B: demand and plan. C: generators, test, laws. D: probability,
belief, optimization, arrays, with the context chapters and the program that uses them.
Inputs: the files of the bundle at the current HEAD, docs/principles.md (Terms, L2.7, L9.6, L10, L11, P11),
record/decisions.md (entries the files cite). Head text of each bundle in X-head.md. No parameters, no
randomness. Writes X-prompt.md and FROZEN (A) or FROZEN-BCD. Commit the inputs first; the commit is
recorded in the frozen file and in the prompt's header."""
import re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
LIB, SPEC = Path("src/luthier/lib"), Path("docs/spec")
BUNDLES = {
 "A": dict(files=[LIB/"world.lth", LIB/"world_model.lut", LIB/"certification.lth", LIB/"certification_model.lut",
                  SPEC/"10-world.md", SPEC/"06-certification.md"], context=[]),
 "B": dict(files=[LIB/"demand.lth", LIB/"demand_model.lut", LIB/"plan.lth", LIB/"plan_model.lut", SPEC/"08-demand.md"],
           context=[]),
 "C": dict(files=[LIB/"generators.lth", LIB/"generators_model.lut", LIB/"test.lth", LIB/"test_model.lut",
                  LIB/"laws.lth", SPEC/"07-tests.md", SPEC/"05-laws.md"], context=[]),
 "D": dict(files=[LIB/"probability.lth", LIB/"probability_model.lut", LIB/"belief.lth", LIB/"belief_model.lut",
                  LIB/"optimization.lth", LIB/"optimization_model.lut", LIB/"arrays.lth",
                  Path("examples/sonolocalizacion/experiment_zero.lut")],
           # context: (title, file, first line, last line), copied verbatim, not under review
           context=[("`docs/spec/11-numbers.md`, section 2 (context)", SPEC/"11-numbers.md", 13, 24),
                    ("`docs/spec/06-certification.md`, item 6.S16 (context)", SPEC/"06-certification.md", 66, 66)]),
}
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
def fence(f):
    return f"### `{f.name}`\n\n````\n{f.read_text(encoding='utf-8').rstrip()}\n````\n"
def build(name):
    FILES, ctx = BUNDLES[name]["files"], BUNDLES[name]["context"]
    ids=set()
    for f in FILES: ids |= set(DID.findall(f.read_text(encoding="utf-8")))
    ctxt = ["### " + t + "\n\n````\n" + "\n".join(f.read_text(encoding="utf-8").split("\n")[a-1:b]) + "\n````\n"
            for t,f,a,b in ctx]
    for t,f,a,b in ctx: ids |= set(DID.findall("\n".join(f.read_text(encoding="utf-8").split("\n")[a-1:b])))
    head = (HERE/f"{name}-head.md").read_text(encoding="utf-8").replace("@COMMIT@", commit[:7])
    body = head + "\n\n---\n\n## Material\n\nFrozen at commit " + commit[:7] + ".\n\n" \
      + "### Principles (excerpt of `docs/principles.md`)\n\n" + princ + "\n\n" \
      + "### Decisions the files cite (from `record/decisions.md`)\n\n" + entries(ids) + "\n\n" \
      + "\n".join(fence(f) for f in FILES) + ("\n" + "\n".join(ctxt) if ctxt else "")
    (HERE/f"{name}-prompt.md").write_text(body, encoding="utf-8")
    print(name, len(body.split()), "words")
names = sys.argv[1:] or ["B","C","D"]
for n in names: build(n)
(HERE/("FROZEN" if names==["A"] else "FROZEN-BCD")).write_text(commit+"\n", encoding="utf-8")
