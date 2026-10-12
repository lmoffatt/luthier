#!/usr/bin/env python3
"""Step 4 of the draft 11 plan: his decisions applied to record/principles-language.md, one edit per
run with `--upto N` (N from 1 to 10), each edit a commit. Every clause the model wrote is marked
proposed; a clause moved unchanged keeps its status. The entries merged (L3 into L2, L11 into L9,
L12 into L10) keep their Quote, Source and History inside the absorbing entry's History and become
(History:) paragraphs. The new entry, L16 Certificates, goes under G1. The clause texts were written
by the model from the decisions D-2026-10-12-h to -s and the critiques of draft 10; the assembly is
mechanical."""
import argparse
import importlib.util
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("pp", ROOT / "scripts/project_principles.py")
pp = importlib.util.module_from_spec(spec); spec.loader.exec_module(pp)
RECORD = ROOT / "record/principles-language.md"

ap = argparse.ArgumentParser()
ap.add_argument("--upto", type=int, default=10)
UPTO = ap.parse_args().upto

text = RECORD.read_text(encoding="utf-8")
items = pp.parse_record(text)
E = {e["tag"]: e for k, e in items if k == "entry"}
for e in E.values():
    e["clauses"] = [(c["text"], c["status"]) for c in e["clauses"]]
    e.setdefault("hist_add", [])
merged_into: dict[str, str] = {}      # old tag -> absorbing tag
order = {"G0": ["L4", "L5", "L9", "L10", "L13", "L15"], "G1": ["L2", "L7", "L14"], "G2": ["L6", "L8"]}
STEP = "draft 11, step 4 (2026-10-12)"

def keep(tag, n):
    return E[tag]["clauses"][n - 1]

def absorb(absorber, absorbed, note):
    a, b = E[absorber], E[absorbed]
    a["hist_add"].append(f"{STEP}: {note} (absorbed {absorbed}) " + " ".join(
        f"{f}: {b[f]}" for f in ("From", "Quote", "Source", "Status", "History") if f in b))
    merged_into[absorbed] = absorber
    for ls in order.values():
        if absorbed in ls:
            ls.remove(absorbed)

# ---- edit 1: L16 Certificates ---------------------------------------------------------------------
def edit1():
    E["L16"] = {
        "tag": "L16",
        "statement": "A certificate records what is known of a law, its domain, its bound and its "
                     "evidence; it is frozen, it serves every demand it meets, and it transports along "
                     "identity.",
        "From": "G1 (a model is known by the law it satisfies, with the evidence it has) with G2 (evidence "
                "is a cost) and G0, the demand (what the demand requires of the evidence is its own)",
        "clauses": [
            ("A certificate (Terms) names the law it records as checked, the domain "
             "the check covered (a subtype, the cases listed, or the distribution sampled), the bound "
             "observed (for a law into `Cost`, the worst cost seen), and the evidence: its grade and, "
             "for a sampled check, the sample's statistics converted to an evidence cost "
             "(D-2026-10-12-r).", "proposed"),
            ("The grade is derived from the domain and the evidence cost: proved and exhaustive have "
             "evidence cost 0 on their domain; cases, 0 on the cases listed and ∞ outside; sampled, "
             "the finite cost of its statistics on the distribution sampled; assumed, the evidence cost "
             "the demand assigns to assumptions, a parameter with no default, so that a demand that "
             "names none refuses assumed values (D-2026-10-11-n, D-2026-10-12-r). The five names stay "
             "in the certificate for the reader; the planner reads the costs.", "proposed"),
            ("The conversion from statistics to an evidence cost is a function with a declared shape, "
             "the sample's statistics and the demand's level in, a cost out, filled per theory "
             "(D-2026-10-12-r); the first instance is −log(1 − ε̂(n, δ)) in nats, with ε̂ the bound on "
             "the fraction of the distribution where the law's bound fails, from n samples at "
             "confidence 1 − δ, and δ the demand's parameter.", "proposed"),
            ("A certificate is identified by a hash over its dependency cone (code, cases, seed, the "
             "distribution and level sampled); it is a frozen snapshot, and a later check does not "
             "change it but issues a new one that supersedes it, both kept, the latest in front (P3), "
             "so progress is the chain of certificates.", "settled"),
            ("A certificate serves every demand whose cutoff it meets, on the bound and on the evidence "
             "cost alike (D-2026-10-12-h); the demand states what it requires (P11), and a memo hit "
             "serves a demand only if the cached cone meets it, checked at the hit and not only when "
             "the certificate was issued.", "settled"),
            ("Certification is the default: demanding a value demands every certificate in its "
             "dependency cone, paid once through the memo, unless the demand opts out by a mechanism "
             "to be named (O3), which leaves a certificate of grade `assumed` (D-2026-10-11-n); what "
             "never reaches an output needs no certificate, and what reaches one carries its cone's; "
             "`test` is the action that demands certificates without values (L10).", "settled"),
            ("Certification transports along identity: if B is certified on inputs X with bound b and "
             "evidence cost e, and the identity A ≡ B is certified on inputs Y with distance d and "
             "evidence cost e′, then A is certified on X ∩ Y with bound b + d and evidence cost e + e′, "
             "and by nothing else; a path of identities composes the same way, link by link, the "
             "distances summed and the evidence summed (D-2026-10-12-q). (His correction, in grades) A "
             "is certified at the weaker of the two grades on X ∩ Y.", "proposed"),
            ("Links sampled over different distributions do not compose without a law relating the "
             "distributions; links sampled over the same distribution compose by the union bound, the "
             "failure fractions summed, which is the probabilistic bound the planner waited for "
             "(D-2026-10-12-q). The composition algebra belongs to the theory's cost type, the sum its "
             "first instance; whether a demand accepts a sampled path is its evidence cutoff, a "
             "parameter (P11).", "proposed"),
            ("No operation on certificates raises a grade, lowers an evidence cost or widens a domain "
             "without new evidence.", "proposed")],
        "Example": "with B's laws only `assumed`, A inherits the cost of an assumption and nothing "
                   "more; a lookup table equal to the native on a grid is certified on the grid and "
                   "nowhere else (clause 7)",
        "Rests on": "O1 (the conversion and the algebra), O3 (the opt-out's syntax)",
        "Quote": "\"a is model of A with cost C, we pass the statistics to cost, we need a convertion. "
                 "might be we work with logCost in nat.\" \"The same, the conversion is expressed by a "
                 "dedicated function and we might choose different functions on different theories. "
                 "Luthier would ask for some input output shape, that the particular function is filled "
                 "on each case.\" (his marks, e8d7db1, 57a0023)",
        "Source": "the critiques of draft 10 (`record/IA/principles 2026 10 12/`, 1429f35: Claude, the "
                  "certificate as the object every L leans on, scattered over L2, L5, L7, L10, L13, L14; "
                  "GPT en, the calculus of evidence scope and the rule that no operation increases grade "
                  "or domain without new evidence); his decisions D-2026-10-12-j, -q, -r; clauses 4 to 6 "
                  "moved from L10.7, L10.10, L10.13, L10.5 and L14.5 of draft 11 step 3",
        "Status": "proposed in draft 11; clauses 4 to 6 settled, moved from L10 and L14; clause 7 "
                  "carries his correction of draft 7 in grades",
        "History": f"{STEP}: new entry, under G1, after L7.",
        "hist_add": [],
    }
    order["G1"].insert(2, "L16")

# ---- edit 2: L5 equality, its clauses to L9, L13, L16 ---------------------------------------------
def edit2():
    e = E["L5"]
    E["_L5.2"] = keep("L5", 2)
    E["_L5.4"] = keep("L5", 4)
    e["statement"] = "Equality has levels and belongs to the object."
    e["clauses"] = [
        keep("L5", 1),
        keep("L5", 3),
        ("Equality is a law of the object: Boolean where the carrier is decidable, a distance where it "
         "carries one, and the type of the identity law's result, `Bool` or `Cost`, says which (L7); "
         "how a certified identity composes along a path is L16.7.", "proposed")]
    e["Rests on"] = "O2 (the equality a type comes with)"
    e["Status"] = "settled; clause 3 proposed"
    e["hist_add"].append(f"{STEP}: the binding-acts clause (2) moved to L9, the identity-law clause (4) "
                         "to L13, the composition clause (5) to L16.7 with its intersection rule "
                         "deleted (D-2026-10-12-q); clause 3 written in their place.")

# ---- edit 3: L9 + L11 -----------------------------------------------------------------------------
def edit3():
    e = E["L9"]
    e["statement"] = ("A program is a DAG of definitions without effects, and statements commute; "
                      "actions have effects, and are verified by observing the world before and after.")
    e["clauses"] = [keep("L9", 1), keep("L9", 2), E.pop("_L5.2"), keep("L9", 3), keep("L9", 4),
                    keep("L9", 5), keep("L9", 6), keep("L9", 7), keep("L11", 1), keep("L11", 2),
                    ("An action on Luthier's own state, writing a certificate or running a test, is "
                     "idempotent and memoizable; an action on the world never is: the world is an "
                     "opaque, unique value, so an action on it is never served from the memo "
                     "(D-2026-10-12-m, O3).", "proposed")]
    e["Rests on"] = "O3 (the world as a value)"
    e["Status"] = "settled; clause 11 proposed"
    E["L9"]["clauses"][4] = (E["L9"]["clauses"][4][0].replace("where L13 and L11 live", "where L13 and the verification of actions (clause 9) live"), "settled")
    E["L14"]["clauses"][3] = (E["L14"]["clauses"][3][0].replace("(L11, L9)", "(L9)"), "settled")
    absorb("L9", "L11", "L11 (an action is verified by observing the world before and after it) merged "
                         "in as clauses 9 and 10, the binding acts of L5.2 as clause 3, clause 11 on "
                         "actions on Luthier's own state written (D-2026-10-12-m)")

# ---- edit 4: L10 + L12, the cutoff, the three objects as statement ---------------------------------
def edit4():
    e = E["L10"]
    e["statement"] = ("The demand determines the computation and the types produced; the meaning of a "
                      "program, its realization under a plan and its evidence are three objects, never "
                      "one.")
    c = {n: keep("L10", n) for n in range(1, 20)}
    e["clauses"] = [
        c[1], c[2], c[3], c[4],
        ("The tests are actions, so verifying is demanding; what a demand requires of the certificates "
         "in its cone, and when a certificate serves it, is L16.5 and L16.6.", "settled"),
        c[6], c[8], c[9],
        ("A test is an action whose result is a certificate (L16.4), rerun when asked or when the "
         "certificate's identity changed; \"each node once\" is once per plan: a stricter demand on "
         "the same definition is another node of another plan, and the looser certificate still "
         "serves what it met.", "settled"),
        ("The meaning of a program is the class its laws fix; a realization is the result under a "
         "plan; the evidence is its certificates (L16): three objects, never one.", "settled"),
        c[14], c[15], c[16], c[17], c[18], c[19],
        ("The demand carries the cutoff: the minimal cutoff for a specimen to be considered, applied to "
         "the composed bound and the composed evidence cost of a path (D-2026-10-12-h, L16.5); a cutoff "
         "does not compose (two links within ε are within 2ε), so it lives in the demand and is "
         "passed down from it, and no law carries one.", "proposed"),
        ("No unrecorded policy constants: thresholds, budgets, limits, statistical levels and the "
         "planner's default policies are never constants in code; they are declared, passed and "
         "recorded. The kernel's primitives (0, ∞, `lift`, `exact`) and mathematical constants are not "
         "policies (D-2026-10-12-n).", "proposed"),
        keep("L12", 2)]
    e["Example"] = ("doubling positives is positive only when positivity is demanded and derivable, sin "
                    "of positives is only Real because no law composes (clause 15)")
    e["Rests on"] = "O1 (the error decoration), O3 (the world as a value), O5, O8, O12"
    e["Status"] = "settled; clause 4 proposed on his note on Terms; clauses 17 and 18 proposed"
    E["L10"]["clauses"][1] = (E["L10"]["clauses"][1][0].replace("(L12)", "(clause 18)"), "settled")
    E["L10"]["clauses"][16] = (E["L10"]["clauses"][16][0].replace("a cutoff does not compose (two links within ε are within 2ε), so it lives in the demand", "a cutoff does not compose (L6.3), so it lives in the demand"), "proposed")
    absorb("L10", "L12", "L12 (no hardcoded constants) merged in as clauses 18 and 19, clause 18 reworded "
                          "to \"no unrecorded policy constants\" (D-2026-10-12-n); the cutoff clause 17 "
                          "written (D-2026-10-12-h); the three objects raised to the statement; the memo "
                          "gate (7), the certificate's identity (10) and the frozen snapshot (13) moved "
                          "to L16.4 and L16.5, clauses 5 and 9 citing them")

# ---- edit 5: L13 specimens, classes and graphs, the sampled edge ----------------------------------
def edit5():
    e = E["L13"]
    c = {n: keep("L13", n) for n in range(1, 12)}
    e["statement"] = ("One function, many specimens, chosen by maximizing the performance the demander "
                      "chooses, along certified identities.")
    e["clauses"] = [
        ("A function has many equivalent implementations, its specimens, each with its precision, "
         "speed, memory and place of execution; equivalence is established first, and the choice among "
         "paths follows expected loss and resources, estimated from a database of measured runs.",
         "settled"),
        ("The cost of a law and the resources of a run, time and memory, are not one scalar, and the "
         "trade-off among them is a parameter of the demand (L10), never the planner's own.",
         "settled"),
        ("(His formula) What the planner ranks is an efficiency, exp(−w·cost) over the resources used, "
         "so that a specimen of cost zero has efficiency 1/resources and not zero, with w, the weight "
         "between cost and resources, the demand's parameter.", "proposed"),
        c[4],
        ("Semantic equivalence forms classes; certified substitutability forms a graph. In the theory "
         "the specimens of a function are the quotient by \"compute the same function up to the law's "
         "equality\", one class per mathematical function, the class chosen by law; in a model that "
         "carries a distance closeness is not transitive, there is no class, only the ball of the "
         "demanded radius (`11` §3), and the planner substitutes one specimen for another only along a "
         "certified identity between the two, the identity law of L5 with its result `Bool` or `Cost` "
         "(D-2026-10-11-m).", "proposed"),
        ("The law gives the candidates; the identity certificates say which the planner may exchange, "
         "and they form a weighted graph: a substitution is a path whose summed distance (`11` §2) and "
         "summed evidence cost (L16.7) are within the demand's cutoff, so two specimens joined through "
         "a third may each replace it and not each other; a lone specimen is never replaced.",
         "proposed"),
        ("A sampled edge is admissible on the distribution it sampled; it composes with edges sampled "
         "over the same distribution, the failure fractions summed, and not with others; the demand's "
         "evidence cutoff says whether it accepts the path (L16.8, D-2026-10-12-q).", "proposed"),
        c[9], c[10], c[11],
        E.pop("_L5.4")]
    e["clauses"][-1] = (e["clauses"][-1][0].replace("into the class the planner moves in", "into the "
                                                   "planner's graph"), "candidate")
    e["Example"] = ("γ_n needs n·u < 1, false for float32 over an hour at 48 kHz, so the cited bound is "
                    "void there (clause 9)")
    e["Rests on"] = "O1 (the sensitivity), O2"
    e["Status"] = ("settled; statement in his words, 2026-10-12, with \"specimens\" and \"along certified "
                   "identities\" added; clauses 3, 5, 6, 7 proposed; clause 11 candidate, from L5")
    e["hist_add"].append(f"{STEP}: \"never summed into a path\" deleted (D-2026-10-12-q); the quotient "
                         "and the ball joined into clause 5 with GPT sp's wording; the sum now a bound "
                         "with its evidence cost (clause 6); cost reserved for the law and resources "
                         "for time and memory (D-2026-10-12-l); the weight named in his formula; the "
                         "identity-law clause of L5.4 joined as clause 11.")

# ---- edit 6: L6 the cutoff, the retraction, the algebras ------------------------------------------
def edit6():
    e = E["L6"]
    e["clauses"] = [
        keep("L6", 1),
        ("The lift is explicit and named: `lift : Bool -> Cost` sends true to 0 and false to ∞, "
         "`exact : Cost -> Bool` is c == 0, with `exact ∘ lift = id`, so `Bool` is a retract of "
         "`Cost`, not a subtype, and the planner inserts the lift as a bridge of cost zero; whether "
         "the two are homomorphisms waits for the algebra (O1), since Boolean or has no counterpart "
         "among the operations of `Cost` yet.", "proposed"),
        ("The cutoff is the demand's (L10.17), passed down from it; it does not compose (two links "
         "within ε are within 2ε), so no law carries one.", "proposed"),
        keep("L6", 4),
        ("The law of a theory is one law, so its certificate is one certificate; how the grades of its "
         "parts combine is the demand's parameter, the vector of grades or the weakest "
         "(D-2026-10-12-i); how the costs of its parts combine is the theory's algebra, with two "
         "candidate models, min and max, or 1/n log-sum-exp and 1/n sum (D-2026-10-12-p); the "
         "composition along a path is the sum (L16.7, D-2026-10-12-q).", "proposed")]
    e["Status"] = ("proposed on his note of 2026-10-12; the names lift, exact and within his to rename; "
                   "clauses 2, 3, 5 reworded on D-2026-10-12-h, -i, -p, -q")
    e["hist_add"].append(f"{STEP}: \"homomorphisms\" withdrawn until the algebra exists (GPT en, GPT sp); "
                         "\"only in the demand\" became \"the demand's, passed down\" (D-2026-10-12-h); "
                         "the grade of a sum parameterizable (D-2026-10-12-i); the two candidate "
                         "algebras named (D-2026-10-12-p).")

# ---- edit 7: L7 law and certifier, delegation --------------------------------------------------------
def edit7():
    e = E["L7"]
    c = {n: keep("L7", n) for n in range(1, 8)}
    e["statement"] = ("A law characterizes; a certifier produces its evidence, exact or statistical; "
                      "and the certificate of identity is not the certificate of the law.")
    e["clauses"] = [
        ("A law is the proposition; a certifier is a method that produces evidence for it, and one law "
         "may have several: a theorem cited, an exhaustive run, chosen cases, a sample, an assumption "
         "(D-2026-10-12-k). The law is not the procedure that checks it, and a universal law over an "
         "infinite carrier has no certifier that runs it.", "proposed"),
        c[1], c[2], c[3],
        ("The certifier is chosen by what the law admits: what is known by a theorem is cited, what "
         "can be enumerated is checked exhaustively, what has chosen cases is checked on them, what "
         "can only be sampled is checked statistically; the evidence travels with the value in a "
         "certificate (L16). The line is the method, since associativity over `Int` is computable and "
         "cannot be checked by running.", "settled"),
        c[5],
        ("Verification by a theorem is `proved` by citation (D-2026-10-11-f); verification by "
         "delegation is the same certifier with the host library's guarantee as the theorem cited "
         "(LAPACK's backward-error bounds, the condition number their hypothesis) and the library's "
         "version and platform as hypotheses the certificate carries; no new grade. A function known "
         "correct by a theorem outside Luthier is certified this way, and the chain law, citation, "
         "native, identity, extern is carried by hash.", "proposed"),
        c[6],
        ("(His annotation) The certificate of the law travels by the certificate of identity (L16.7): "
         "exactly where the identity is boolean (`==` structural, `05` R8: integers, decidable types, "
         "the same implementation rerun), and with the observed distance added where it is a cost "
         "(G2), since two implementations over floats are almost never bit-identical; the type of the "
         "identity law's result says which (`Bool` or `Cost`).", "settled")]
    e["Status"] = "settled; clause 1 proposed (D-2026-10-12-k); clause 7 proposed on his mark"
    e["hist_add"].append(f"{STEP}: clause 1 written on D-2026-10-12-k (GPT en's distinction); delegation "
                         "as citation moved here from L14.8 as clause 7; clause 5 reworded with the "
                         "certifier and the grade list cited from Terms; clause 9 cites L16.7.")

# ---- edit 8: L2 + L3, what `a : A` asserts ---------------------------------------------------------
def edit8():
    e = E["L2"]
    e["statement"] = ("A type is a proposition, membership is a guarantee, and the certified subtype "
                      "from a law is the fundamental construction pattern.")
    e["clauses"] = [
        keep("L2", 1),
        ("`a : A` is one judgment, structural and decidable for the kernel's structures; it asserts the "
         "structural proposition outright and the laws through the certificate, with the evidence the "
         "certificate has.", "settled"),
        ("A value with a sampled or assumed certificate is a model of its theory with the cost its "
         "certificate records (D-2026-10-12-j); \"guarantee\" means what the evidence says, and the "
         "word model promises the evidence, not exactness.", "proposed"),
        ("What a law adds is evidence, recorded in a certificate (L16); what leaves the program carries "
         "one (L16.6, D-2026-10-11-n).", "settled"),
        keep("L3", 1), keep("L3", 2),
        ("Where the law is into `Cost`, the certificate records the bound it observed, and the "
         "demand's cutoff decides whether it serves (L16.5, D-2026-10-12-h); the constructor takes no "
         "tolerance.", "proposed"),
        keep("L3", 4)]
    e["Rests on"] = "O1 (the bound in a certificate)"
    e["Status"] = ("settled; clauses 3 and 7 proposed (D-2026-10-12-j, -h); \"from a law\" is his "
                   "correction of 2026-10-12")
    E["L13"]["clauses"][8] = (E["L13"]["clauses"][8][0].replace("inputs certified (L3) in that subtype", "inputs certified (L2) in that subtype"), E["L13"]["clauses"][8][1])
    absorb("L2", "L3", "L3 (the certified subtype from a law) merged in as clauses 5 to 8; clause 3 "
                        "written on D-2026-10-12-j; the grade meanings of draft 10's clause 3 are now "
                        "L16.2; the tolerance left the constructor (D-2026-10-12-h)")

# ---- edit 9: L14 halved -------------------------------------------------------------------------------
def edit9():
    e = E["L14"]
    c = {n: keep("L14", n) for n in range(1, 10)}
    e["statement"] = ("Luthier orchestrates other languages: an extern is a specimen certified by its "
                      "laws, and what does not follow Luthier's way lives in a world.")
    e["clauses"] = [
        c[1], c[2], c[3], c[4], c[6],
        ("A definition or an implementation that does not follow Luthier's way, an extern with no law "
         "yet, a foreign algorithm taken as is, may execute inside a named world (L9): its "
         "certificates carry the cost of an assumption (L16.2), the plan shows the world it ran in, "
         "and nothing from it enters the planner's graph (L13) nor a certified theory until a law is "
         "certified.", "candidate")]
    e.pop("Example", None)
    e["Rests on"] = "O3 (the opt-out's syntax; the world as a value)"
    e["Status"] = "settled by his correction of draft 7; clause 6 candidate, reworded"
    e["hist_add"].append(f"{STEP}: certification by default (5) moved to L16.6, delegation (8) to L7.7, "
                         "the graded transport (9, his correction) to L16.7 with its example; clause 6 "
                         "reworded so that an extern without a law executes in a world and enters "
                         "neither the planner's graph nor a certified theory (DeepSeek, GPT en, GPT "
                         "sp).")

# ---- edit 10: vocabulary ---------------------------------------------------------------------------
def edit10():
    subs = [(r"\bthe kernel's types\b", "the kernel's structures")]
    for tag in ("L4", "L5", "L9", "L10", "L15", "L6", "L8"):
        e = E[tag]
        new = []
        changed = False
        for t, s in e["clauses"]:
            t2 = t
            for a, b in subs:
                t2 = re.sub(a, b, t2)
            changed |= t2 != t
            new.append((t2, s))
        e["clauses"] = new
        if changed:
            e["hist_add"].append(f"{STEP}: vocabulary (D-2026-10-12-l).")
    E["L15"]["clauses"][2] = (E["L15"]["clauses"][2][0], "settled")
    t = E["L10"]["clauses"][5][0]
    E["L10"]["clauses"][5] = (t.replace("the model its type names", "the model its type names (Terms)"), "settled")
    E["L10"]["hist_add"].append(f"{STEP}: vocabulary pass (D-2026-10-12-l): structure for a kernel type, "
                               "theory for a Luthier type, cost for the law and resources for time and "
                               "memory, model for what a type names and specimen for the planner's "
                               "candidates; applied where the old word stood.")

EDITS = [edit1, edit2, edit3, edit4, edit5, edit6, edit7, edit8, edit9, edit10]
for f in EDITS[:UPTO]:
    f()

# ---- rendering (as the step 3 script) ------------------------------------------------------------
def field(name, text):
    first = f"{name}:" + " " * max(1, 12 - len(name) - 1)
    return textwrap.fill(text, width=100, initial_indent=first, subsequent_indent=" " * 12,
                         break_long_words=False, break_on_hyphens=False)

def head_line(tag, stmt):
    return textwrap.fill(stmt, width=100, initial_indent=f"{tag}" + " " * max(1, 4 - len(tag)),
                         subsequent_indent="    ", break_long_words=False, break_on_hyphens=False)

def clause_line(tag, n, t, status):
    first = f"{tag}.{n}" + " " * max(1, 7 - len(f"{tag}.{n}"))
    return textwrap.fill(f"{t} [{status}]", width=100, initial_indent=first, subsequent_indent=" " * 7,
                         break_long_words=False, break_on_hyphens=False)

def references(e):
    t = " ".join(x for x, _ in e["clauses"]) + " " + e.get("Example", "")
    ds = sorted(set(re.findall(r"\bD-\d{4}-\d{2}-\d{2}-[a-z]+\b", t)))
    docs = sorted(set(re.findall(r"`\d\d(?: §\d+)?`(?: R\d+)?", t)))
    ws = sorted(set(re.findall(r"\bW\d+\b", t)), key=lambda w: int(w[1:]))
    ps = sorted(set(re.findall(r"\bP\d+\b", t)), key=lambda w: int(w[1:]))
    return "; ".join(x for x in [", ".join(docs), ", ".join(ds), ", ".join(ws), ", ".join(ps)] if x)

def render(e):
    out = [head_line(e["tag"], e["statement"])]
    for name in ("Tier", "From", "Formulation"):
        if name in e:
            out.append(field(name, e[name]))
    for n, (t, s) in enumerate(e["clauses"], 1):
        out.append(clause_line(e["tag"], n, t, s))
    if e.get("Example"):
        out.append(field("Example", e["Example"]))
    refs = references(e)
    if refs:
        out.append(field("References", refs))
    if e.get("Rests on"):
        out.append(field("Rests on", e["Rests on"]))
    if e.get("Quote"):
        out.append(field("Quote", e["Quote"]))
    out.append(field("Source", e["Source"]))
    if e.get("Status"):
        out.append(field("Status", e["Status"]))
    out.append(field("History", " ".join([e.get("History", "")] + e["hist_add"]).strip()))
    return "\n".join(out)

def hist_para(t):
    return textwrap.fill(t, width=100, break_long_words=False, break_on_hyphens=False)

# ---- assemble: the record's prose as it is, the entries re-rendered in the new order --------------
lines = text.splitlines()
start = next(i for i, l in enumerate(lines) if l.strip() == "## Purpose")
head = "\n".join(lines[:start]).rstrip("\n")
if UPTO >= 1:
    head = head.replace("| absorbed | L3 | into G1 (draft 10) |",
                        "| absorbed | L3 | into G1 (draft 10) |\n| L16 | new | certificates, draft 11 (step 4) |")
if UPTO >= 3:
    head = head.replace("| L11 | L12 | renumbered and shortened |",
                        "| L11 | L12 | renumbered and shortened; merged into L9 in draft 11 |")
if UPTO >= 4:
    head = head.replace("| L12 | L17 | renumbered; statement in his words |",
                        "| L12 | L17 | renumbered; statement in his words; merged into L10 in draft 11 |")
if UPTO >= 8:
    head = head.replace("| L3 | L4 | renumbered; \"from a law\" his correction |",
                        "| L3 | L4 | renumbered; \"from a law\" his correction; merged into L2 in draft 11 |")
if UPTO >= 1:
    head = head.replace("| Draft 10 and 11 | Before | What happened |", "| Draft 11 | Before | What happened |")

out = [head, ""]
PROSE_SUBS = []
if UPTO >= 3:
    PROSE_SUBS.append(("verified by reading the store back (L11)", "verified by reading the store back (L9)"))
if UPTO >= 4:
    PROSE_SUBS.append(("with tol a parameter (L12)", "with tol a parameter (L10)"))
def fix_prose(block):
    for a, b in PROSE_SUBS:
        block = block.replace(a, b)
    return block
prose_blocks = [(k, fix_prose(it) if k == "prose" else it) for k, it in items]
# walk the record's items; prose kept; entries re-rendered by section
section = None
seen_sections = set()
for k, it in prose_blocks:
    if k == "prose":
        if "### Under G0" in it:
            section = "G0"
        elif "### Under G1" in it:
            section = "G1"
        elif "### Under G2" in it:
            section = "G2"
        elif it.lstrip().startswith("## What is open"):
            section = None
        out += [it, ""]
        if section and section not in seen_sections:
            seen_sections.add(section)
            out += ["```", "\n\n".join(render(E[t]) for t in order[section]), "```", ""]
    else:
        tag = it["tag"]
        if tag in ("L1", "G0", "G1", "G2"):
            out += ["```", render(E[tag]), "```", ""]
        # L entries are rendered by section above
# the merged entries as (History:) paragraphs, before What is open
merged_paras = []
for old_tag, new_tag in merged_into.items():
    b = E[old_tag]
    merged_paras.append(hist_para(f"(History: {old_tag} at draft 11 step 3, merged into {new_tag} in step 4: "
                                  f"{old_tag} {b['statement']} " +
                                  " ".join(f"{n}. {t} [{s}]" for n, (t, s) in enumerate(b['clauses'], 1)) + ")"))
if merged_paras:
    i = next(i for i, l in enumerate(out) if l.startswith("## What is open"))
    out[i:i] = merged_paras + [""]
res = "\n".join(out).rstrip("\n") + "\n"
# What is open: the clause numbers it blocks follow the new numbering
if UPTO >= 4:
    res = res.replace("Blocks L2.4,\n  L3.3, L5.5, L6, L8.3, L8.4, L10.4, L13.7, L13.9.",
                      "Blocks L2.7,\n  L5.3, L6, L8.3, L8.4, L10.4, L13.6, L13.8, L16.3, L16.8.")
    res = res.replace("Blocks L10.6, L11, L14.5, L14.7.", "Blocks L9.11, L10.6, L14.6, L16.6.")
    res = res.replace("Blocks L10.18.", "Blocks L10.15.")
    res = res.replace("Blocks\n  L10.15.", "Blocks\n  L10.12.")
    res = res.replace("Blocks L14.8.", "Blocks L7.7.")
    res = res.replace("- L5.5, the composition of identities as paths (his note of 2026-10-12 put in words).",
                      "- L16.7 and L16.8, the composition of identities as paths (his note of 2026-10-12 put in\n  words, with D-2026-10-12-q).")
    res = res.replace("- L14.7, the world as a candidate; L14.8, delegation as citation; L14.9, the wording of the graded\n  transport (his correction).",
                      "- L14.6, the world as a candidate; L7.7, delegation as citation; L16.7, the wording of the graded\n  transport (his correction).\n- L16, the certificate entry; L2.3, what `a : A` asserts; L9.11, actions on Luthier's own state;\n  L10.17 and L10.18, the cutoff and the policy constants; L13.3, 5, 6, 7; L6.2, 3, 5; L7.1.")
    res = res.replace("- L10.4, the decorated output as another model.\n", "- L10.4, the decorated output as another model.\n")
RECORD.write_text(res, encoding="utf-8")
print(f"edits 1..{UPTO} applied; record {len(res.splitlines())} lines")
