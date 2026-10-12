#!/usr/bin/env python3
"""Step 3 of the draft 11 plan (record/plan-principles-draft-11-2026-10-12-execution.md): the shape
of D-2026-10-12-g and -s applied to record/principles-language.md without changing what any clause
says. Each entry's Formulation becomes numbered clauses, each with the status its sentence had in
draft 10; the worked examples go to Example; the provenance phrases go to History; the grades are
defined once, in Terms; the organizers are two sentences each, no status, no mechanics, and head
the sections; G3 (the demand) dissolves into G0 and L10.1 and stays as a (History:) paragraph;
the Purpose section carries L1; a precedence line and a Keys section are added; What is open is
split into open questions with ids (O1...), his pending marks, and the done items, which go to
the drafts table. Quote, Source and History of every entry are kept as they were, with one line
added for this step. The clauses were written by the model from draft 10 (b7a7e23), by hand; the
assembly is mechanical."""
import importlib.util
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("pp", ROOT / "scripts/project_principles.py")
pp = importlib.util.module_from_spec(spec); spec.loader.exec_module(pp)
RECORD = ROOT / "record/principles-language.md"
record_text = RECORD.read_text(encoding="utf-8")
old = {e["tag"]: e for k, e in pp.parse_record(record_text) if k == "entry"}

STEP = ("draft 11, step 3 (2026-10-12): the formulation split into numbered clauses with the status "
        "each sentence had in draft 10, the examples into Example, the provenance phrases into this "
        "History, the wording otherwise as draft 10 had it.")

# ---- the organizers: two sentences each, no mechanics, no status (D-2026-10-12-s) ---------------
G = {
    "G0": ("Type theory is the guide.",
           "A type is a proposition and a value its proof; a law is a proposition over terms, so it "
           "defines a mathematical object and a quotient, and inside the class the representative is "
           "free. Type theory guides what is declared, and what governs execution is the demand, read "
           "in the same theory: a demanded type is a judgment to inhabit, execution is the search for an "
           "inhabitant, and where type theory normalizes a given term, Luthier searches for one."),
    "G1": ("A type is a theory and its values are its models.",
           "If a type is a proposition, then a proposition can say that a structure follows the rules "
           "of a theory, so \"this structure satisfies the laws of the theory\" is said, in the "
           "language of types, as \"it is of the type of the theory\": it is a model of the theory, "
           "and Luthier verifies that it is. Types thereby carry a strong semantic meaning, and coding "
           "and testing are one act: to declare `m : T` is to declare the tests `m` will pass."),
    "G2": ("Laws are valued in cost: one logic, extended to the non-negative reals.",
           "Not every theory is easily described by Booleans; many are represented better by costs. "
           "Since object classifiers exist that extend logic to the non-negative reals, with the "
           "Booleans as a special case, the composition of errors in numerical libraries can be "
           "attacked with this one unified logic."),
}
G_HISTORY = {
    "G0": "draft 11, step 3 (2026-10-12): cut to two sentences, no status, no mechanics (D-2026-10-12-s); "
          "the executive clause of G3 (the demand defines what is computed) read into it, as G3's own "
          "status asked; \"cost or execution time ranks the candidates\" dropped, since the ranking is "
          "L13's; the Ls under it listed in its section.",
    "G1": "draft 11, step 3 (2026-10-12): cut to two sentences, no status, no mechanics (D-2026-10-12-s); "
          "\"what type theory lacks: it knows a value by its term; Luthier knows it by the law it "
          "satisfies\" kept here; the Ls under it listed in its section.",
    "G2": "draft 11, step 3 (2026-10-12): cut to two sentences, no status, no mechanics (D-2026-10-12-s); "
          "\"how laws combine is L6; how a law is verified, L7; what a run teaches is kept\" and the "
          "status of draft 10 (the second eureka on his note of 2026-10-12, candidate by the P13 count, "
          "one decision guided so far; the algebra of costs open, the analysis he announced pending) "
          "kept here; the Ls under it listed in its section.",
}
G_TIER = {"G0": "the guide", "G1": "eureka, the first (the trigger, audio 09.19, 00:00 to 00:14)",
          "G2": "the second eureka on his note of 2026-10-12"}

# ---- the principles: statement, clauses (text, status), example, rests on, status ----------------
# A clause keeps draft 10's words; "(His words)", "(His annotation)", "(His correction)", "(His
# reading)" stay as attribution; dates, rounds, IA names and "the model's" go to History.
L = {}
L["L1"] = dict(
    statement="Luthier expresses the invariances of the disciplines.",
    clauses=[("What moves the language: a species mates within itself, electrons are fermions, a "
              "probability integrates to one. A definition states the invariances that determine a "
              "concept, and the language exists so that stating them is natural.", "settled")],
    status="settled; the purpose, not a design rule, so it heads the document",
    history="draft 11, step 3 (2026-10-12): moved to the Purpose section, the tag kept so that "
            "citations resolve.")
L["L2"] = dict(
    statement="A type is a proposition, and membership is a guarantee.",
    clauses=[
        ("Belonging to a type asserts the propositions, laws included, that the value satisfies; "
         "function types carry their laws the same way.", "settled"),
        ("`a : A` is one judgment, structural and decidable for the kernel's types; it asserts the "
         "structural proposition outright and the laws through the certificate, at the grade the "
         "certificate has.", "settled"),
        ("\"Guarantee\" means what the grade (Terms) says: proved or exhaustive, a guarantee; sampled, "
         "evidence at a level; assumed, a hole that says so.", "settled"),
        ("What a law adds is evidence, and the certificate of the law carries its grade and, for a law "
         "into `Cost`, the worst cost seen (`11` §4).", "settled"),
        ("The guarantee is what the certificate says and no more, and what leaves the program carries "
         "one (L10, D-2026-10-11-n).", "settled")],
    rests="O1 (the worst cost seen, and how the uncertainty of a cost sits in a certificate)",
    status="settled",
    history="the grade list deleted here, defined in Terms.")
L["L3"] = dict(
    statement="The certified subtype from a law is the fundamental construction pattern.",
    clauses=[
        ("From a material type and a law, a predicate or a cost with its tolerance, come the certified "
         "type, its only constructor and the forgetful projection; the same pattern builds values, "
         "functions and programs.", "settled"),
        ("A law gives the three at once: the type, the constructor with Maybe, the membership "
         "function.", "settled"),
        ("Where the law is into `Cost`, the constructor takes the tolerance as a parameter (L12) and "
         "the certificate records the tolerance it was checked at, so a stricter demand asks for a "
         "new check (`11` §4).", "settled"),
        ("Types are verified before they are constructed: Luthier starts from types by verification, "
         "and types by construction may come in later.", "settled")],
    rests="O1",
    status="settled; \"from a law\" is his correction of 2026-10-12",
    history="")
L["L4"] = dict(
    statement="Declare, then define, then inhabit.",
    clauses=[
        ("A declaration without a body is a first-class hole: at once axiom, program input, external "
         "function, pending definition and dead code; nothing executes until it is defined, and no "
         "value inhabits an undefined type.", "settled"),
        ("An axiom is not a value but a law with grade `assumed`, so it does not inhabit; `assumed` "
         "has one meaning, the grade.", "settled"),
        ("To the type checker the five are one, and the elaborated form records which it is, since "
         "the demand treats them differently: an input asks for a value, an external calls the host, "
         "a pending definition is an error, an axiom is a law with grade `assumed`, reasoned with and "
         "never run (O9).", "settled"),
        ("`extern` is the operation that inhabits a hole with a body in another language, naming the "
         "language; a theoretical module (types, functions, laws, no values) is a module of holes.",
         "settled"),
        ("(His words) A declared name is assumed to have its declared type, and its use where that "
         "type is incompatible is an error (`05` R1, the checker).", "settled")],
    rests="O9 (the kind of a hole in the elaborated form, for the spec)",
    status="settled",
    history="")
L["L5"] = dict(
    statement="Equality has levels, belongs to the object, and is a law that composes.",
    clauses=[
        ("Definition (`:=`), the identity proposition (`=`), decidable equality (`==`) and "
         "definitional equality by reduction (`≡`) are different things, and each object carries the "
         "observational equality that fits it.", "settled"),
        ("(His annotation) The binding acts are two, `:=` once and `<-` rebinding, and they share one "
         "law: after the act the name equals the term in the equality its type has, structural `==` "
         "where it exists (`05` R8), observational otherwise, a distance under G2; after `:=` for all "
         "time, after `<-` until the next `<-` (`05` R12).", "settled"),
        ("In the kernel the binding is exact: the name denotes the term, and reduction does not depend "
         "on a tolerance; the distance enters when the planner realizes the term by another "
         "representative, which it does only along a certified equivalence carrying its distance "
         "(L13, D-2026-10-11-m).", "settled"),
        ("The identity law between two specimens, with its distance, is what admits a second "
         "implementation into the class the planner moves in (L13, D-2026-10-11-m); the agreement test "
         "of W5 between native and extern is this law, and the reference formula of a law evaluated "
         "over `Rational` is one more specimen, with grade exact, checked by the same law.",
         "candidate"),
        ("Identity is a law, so it composes as HoTT composes paths: reflexive, symmetric, transitive; "
         "under cost the composed path costs the sum of its links and holds at the weakest of their "
         "grades, and a sampled link holds only on the inputs its samples cover, so the composition "
         "holds on the intersection of the domains certified.", "proposed")],
    rests="O1 (the composition under cost), O2 (the equality a type comes with)",
    status="settled; clause 4 from the identity entry of drafts 1 to 9 (Numbering), candidate; clause 5 proposed",
    history="clause 5 is his note of 2026-10-12 on the reorder plan put in words, and what L13.7 "
            "states for the planner's paths.")
L["L6"] = dict(
    statement="Laws combine, and a predicate lifts to a cost.",
    clauses=[
        ("Predicates combine by and, or, then, and by a quantifier over a carrier, and the result is "
         "a predicate; costs combine by sum, max and weighted sum, and the result is a cost; a "
         "combination that mixes the two is a cost, each predicate lifted.", "proposed"),
        ("The lift is explicit and named: `lift : Bool -> Cost` sends true to 0 and false to ∞, "
         "`exact : Cost -> Bool` is c == 0, both homomorphisms with `exact ∘ lift = id`, so `Bool` is "
         "a retract of `Cost`, not a subtype, and the planner inserts the lift as a bridge of cost "
         "zero.", "settled"),
        ("The cutoff `within ε : Cost -> Bool` lives only in the demand, since it does not compose "
         "(two links within ε are within 2ε).", "settled"),
        ("`&`, the only join the libraries use today, is the Boolean and.", "settled"),
        ("The law of a theory is one law, so its certificate is one certificate, and its grade is "
         "composed from the grades of the parts: with `&`, the weakest; with a sum of costs, the "
         "costs summed, each at its grade.", "proposed")],
    rests="O1 (the algebra of costs; the two candidate models, D-2026-10-12-p)",
    status="proposed on his note of 2026-10-12; clauses 2 and 3 settled on his mark of draft 9, the "
           "names lift, exact and within his to rename",
    history="clause 1 is the paragraph that stood in G2 at draft 10; clause 5 is the composed grade "
            "from the former L11, on his note on Terms; \"a law is a predicate or a cost\" deleted "
            "here, defined in Terms.")
L["L7"] = dict(
    statement="A law characterizes; it is verified by one operation, exact or statistical; and the "
              "certificate of identity is not the certificate of the law.",
    clauses=[
        ("A law states a mathematical property of an operation; a second implementation checked "
         "against the first is consistency, and the native definition is one more model certified "
         "against the law.", "settled"),
        ("A law over several functions is tested on the values actually computed, as a puzzle whose "
         "pieces must fit; the cases to test are chosen by the law, its arity (three elements for "
         "associativity) and the distribution sampled, never every path.", "settled"),
        ("Laws accumulate, and a law need not determine the operation; when the laws do determine it "
         "up to the presentation's equality, that is the limit (D-2026-10-11-d).", "settled"),
        ("What is known by a theorem is cited, what can be enumerated is checked exhaustively, what "
         "has chosen cases is checked on them, what can only be sampled is checked statistically, and "
         "the grade of the evidence (Terms) travels with the value in a certificate hashed over its "
         "dependency cone; the line is the method, since associativity over `Int` is computable and "
         "cannot be checked by running.", "settled"),
        ("The grade of a sampled certificate depends on the distribution sampled, not only on the "
         "number of samples, because errors concentrate at the edges.", "settled"),
        ("Checking that an implementation gives the same bits as before, with the same seed, "
         "certifies that the implementation has not changed; checking it against its laws, by chosen "
         "or sampled cases, certifies the description. Both are kept, apart.", "settled"),
        ("(His annotation) The certificate of the law travels by the certificate of identity: "
         "exactly where the identity is boolean (`==` structural, `05` R8: integers, decidable types, "
         "the same implementation rerun), and with the observed distance added where it is a cost "
         "(G2), since two implementations over floats are almost never bit-identical; the type of the "
         "identity law's result says which (`Bool` or `Cost`).", "settled")],
    rests="O1 (what a sampled level asserts, and its conversion to a cost, D-2026-10-12-r)",
    status="settled",
    history="the generators of clause 2 are the model's addition; clause 5 is the model's correction, "
            "from the practice of property-based testing; the grade list deleted here, defined in "
            "Terms.")
L["L8"] = dict(
    statement="The ideal world is realized with a guarantee.",
    clauses=[
        ("Code is written over ideal objects (Real) and realized by concrete ones (Float64); the "
         "realization's laws hold within a stated tolerance, and the error of each step is itself a "
         "law rather than a false claim of exactness.", "settled"),
        ("(His reading) Rounding `Real -> Float64` is a functor in Lawvere's sense, and each law of "
         "`Real` is projected onto `Float64` with its cost; it is not a homomorphism, and the exact "
         "map is the inclusion the other way.", "settled"),
        ("Rounding does not expand distances by at most a constant: two reals astride a rounding "
         "boundary land one ulp apart at any distance, so no multiplicative constant exists; rounding "
         "is non-expansive up to an additive defect of about ε|x|, and for subtraction and division "
         "the sensitivity is per input, the condition number (`11` §7).", "mark pending"),
        ("The functor reading stands with \"non-expansive plus an additive term\", and the cost "
         "algebra needs both parts: a multiplicative one where a Lipschitz constant exists and an "
         "additive one where rounding enters (`11` §5).", "mark pending")],
    rests="O1 (the two parts of the algebra)",
    status="settled in its statement; clauses 3 and 4 are the correction proposed, his mark pending",
    history="")
L["L9"] = dict(
    statement="A program is a DAG of definitions without effects, and statements commute.",
    clauses=[
        ("The unit is the definition; dependencies give the only order there is, and time is "
         "reconstructed from them rather than from the text.", "settled"),
        ("Inside a block the text fixes which binding a name means, each `<-` a fresh name "
         "(D-2026-10-11-i), and then dependencies give the only order.", "settled"),
        ("Operations are declared before their laws, so a law that binds two operations is a node "
         "with two parents, not a cycle.", "settled"),
        ("A mutable parameter is two variables, before and after, so it is not an effect, the "
         "dependence is an edge, and mutation in place is the planner's optimization when the "
         "earlier one has no other consumer; what is forbidden is what the graph does not show.",
         "settled"),
        ("The DAG says what depends on what; the structure the laws generate over terms (an "
         "equivalence when laws are boolean, a metric space when they carry a distance) is a second "
         "structure, where L13 and L11 live.", "settled"),
        ("A definition's result depends only on its inputs; effects live only in the actions (print, "
         "save). It is the one assumption under which every evaluation strategy gives the same "
         "result; over a carrier with a distance, a result in the same class at a distance the plan "
         "records, and for the Boolean case this is `Confluent` in `lib/plan.lut`, a law a dataflow "
         "is certified against rather than a theorem assumed.", "settled"),
        ("(His words) No effect on the world; its one effect is on the program: it takes its name, "
         "once, and enters the map of definitions, so the same name is not defined twice (`:=` once; "
         "`<-` only in a block, D-2026-10-11-i).", "settled")],
    example="after `x <- 1`, `y := x + 10`, `x <- 2`, y is 11, as the session answers (clause 2)",
    status="settled",
    history="clause 4 joins the two sentences of draft 10 on the mutable parameter, which said the "
            "same thing twice.")
L["L10"] = dict(
    statement="The demand determines the computation and the types produced.",
    clauses=[
        ("The declarative face states what is known, universal and minimally processed; the executive "
         "face is a demand from outside, and the demanded type fixes the path, the types and the "
         "tolerances actually produced.", "settled"),
        ("The evaluation strategy is a parameter separate from the program (L12); by default, a plan "
         "backward from the actions over names, evaluating nothing, then a strict forward run over "
         "the live subgraph, each node once and whole: forward on demand.", "settled"),
        ("What the action asks for flows backward along the plan and is produced forward: the value, "
         "its error, its derivative, its test, the type of its result; at the leaves a value lifts on "
         "its own, takes a mark given with the demand, or is a hole.", "settled"),
        ("A decoration of the output is another model of the theory the code was written over (G1): "
         "run over dual numbers the code gives its derivative, run over intervals or over pairs of "
         "value and cost it gives its error; the demand choosing the output type is the demand "
         "choosing the model, and the planner inserts the bridges (L13). The derivative needs nothing "
         "new; the error waits for the algebra of costs (O1, O5).", "proposed"),
        ("The tests are actions, so verifying is demanding. What never reaches an output needs no "
         "certificate, and what reaches one carries its cone's certificates (D-2026-10-11-n; `test` "
         "demands certificates without values).", "settled"),
        ("A result is identified by code, inputs, mode, the demanded type and tolerance, the model "
         "its type names, the seed, the plan that produced it, the plan being a value "
         "(`lib/plan.lut`), and the hashes of the certificates in its live cone, so a host library or "
         "platform that changed is a new result.", "settled"),
        ("The grade the demand states is in the identity too, and a memo hit serves a demand only if "
         "the cached cone meets that grade, checked at the hit and not only when the certificate was "
         "issued.", "settled"),
        ("The runtime includes the thread count and scheduling of the host, and an extern whose bits "
         "depend on scheduling is not bit-identical to itself, so its identity law is `Cost`, never "
         "`Bool` (L5).", "settled"),
        ("The run database is what the planner reads to choose the plan and is not an input of the "
         "result once the plan is fixed; evidence accumulates by a separate action with its own "
         "record, so \"each node once\" and G2's \"kept across runs\" never meet on one node.",
         "settled"),
        ("A test is an action whose result is a certificate, memoized by the certificate's identity "
         "(code, cases, seed, the distribution and level sampled, L7) and rerun when asked or when "
         "that identity changed; the demand states the grade it requires (P11), and a certificate "
         "serves every demand whose tolerance and grade it meets (`11` §4).", "settled"),
        ("\"Each node once\" is once per plan: a stricter demand on the same definition is another "
         "node of another plan, and the looser certificate still serves what it met.", "settled"),
        ("Three objects, never one: the meaning of a program, the class its laws fix; a realization, "
         "the result under a plan; the evidence, its certificates.", "settled"),
        ("A certificate is a frozen snapshot by hash; a later test does not change it, it issues a new "
         "one that supersedes it, both kept, the latest in front (P3), so progress is the chain of "
         "certificates.", "settled"),
        ("Two sessions that differ only in the order of independent bindings are equivalent by "
         "`Confluent` (L9), the law the session block is certified against.", "settled"),
        ("The program is the synthesis and is kept, the computation is the expansion and is redone. "
         "Script and interpreter are the same under this L, one batch of demands or demands one at a "
         "time with the memo between them (`04` §7, O8); a session is a block and a file is never "
         "one, so a session saved to a file becomes its `main` block (D-2026-10-11-i).", "settled"),
        ("What is produced, and which types, is what the demanded value needs; what it does not need, "
         "the complement of its dependency cone, is not produced, so the choice is canonical, one per "
         "demand, and the types being spoken are what was asked for.", "settled"),
        ("Not producing at run time (a node freed after its last consumer) and not carrying in the "
         "type (how much history a certificate keeps) are one; the program is always kept, only what "
         "leaves scope is lost; not producing is not materializing a derived value, never erasing "
         "what reconstructs or recertifies it (code, inputs, model, seed, plan, tolerance), which the "
         "memo's identity keeps.", "settled"),
        ("A function on a type applied to a subtype does not produce one overload per subtype; the "
         "demanded return type selects which law to derive by composition (G1, O4), and the rest is "
         "not produced.", "settled"),
        ("What is derivable is a property of the expression, independent of the demand; the demand "
         "chooses which of it is derived, certified and carried, so the elaboration (types, derivable "
         "laws) does not depend on the observer; the memo of results does, and they are two caches.",
         "settled")],
    example="doubling positives is positive only when positivity is demanded and derivable, sin of "
            "positives is only Real because no law composes (clause 18)",
    rests="O1 (the error decoration), O3 (the world as a value, so that an action is never served "
          "from the memo), O5, O8, O12",
    status="settled; clause 4 proposed on his note on Terms",
    history="clause 1 is G3 of draft 10, the demand defines what is computed, read here as its own "
            "status asked; the identity of a result (6), the memo gate (7) and the three objects (12) "
            "are the model's, from the rounds of critiques; the three cases at the leaves (3) and the "
            "memo key are the model's, accepted; clause 15's source is audio 08.58, 17:12 to 23:35; "
            "the former L13 restated without the forgetful functor on his note of 2026-10-12 (16 "
            "to 19).")
L["L11"] = dict(
    statement="An action is verified by observing the world before and after it.",
    clauses=[
        ("(His annotation) Executing is the executive face: an action changes the state of the world, "
         "and it is verified too, by observing the world before and after it; the laws over actions "
         "are stated over those two observations, as a mutable parameter is two variables (L9).",
         "settled"),
        ("An observation is itself an action, so this stops where the world can be read back (a file "
         "written and reread), and says nothing beyond; an effect on state Luthier owns is verified "
         "this way, an irreversible or concurrent effect outside it is typed, logged and audited, "
         "never verified.", "settled")],
    rests="O3 (actions and the world as a value, not implemented)",
    status="settled",
    history="shortened at draft 10 on his note of 2026-10-12: evaluation and execution are in Terms, "
            "the reading of computation as the kernel of a function stays in this History.")
L["L12"] = dict(
    statement="No hardcoded constants: every criterion is a parameter.",
    clauses=[
        ("Thresholds, budgets, limits and statistical levels are never constants in code; they are "
         "declared, passed and recorded.", "settled"),
        ("The outermost demand, an action with no caller, carries its tolerance as a declared default "
         "argument (D-2026-10-11-c), recorded with the call, so there is a root and it is a "
         "parameter.", "settled")],
    status="settled; statement in his words, 2026-10-12",
    history="")
L["L13"] = dict(
    statement="One function, many paths, chosen by maximizing the performance the demander chooses.",
    clauses=[
        ("A function has many equivalent implementations, each with its precision, speed, memory and "
         "place of execution; equivalence is established first, and the choice among paths follows "
         "expected loss and cost, estimated from a database of measured runs.", "settled"),
        ("Error, time and memory are not one scalar, and the trade-off among them is a parameter of "
         "the demand (L12), never the planner's own.", "settled"),
        ("(His formula) What the planner ranks is an efficiency, exp(−cost) over the resources used "
         "(time, memory), so that a model of cost zero has efficiency 1/resources and not zero, with "
         "the weight between cost and resources the demand's parameter.", "proposed"),
        ("Two regimes: on a decidable carrier (`Int`, `Fin n`) two implementations compute the same "
         "function or not, the quotient is exact, there is no precision to trade and the Boolean "
         "kernel stands on its own; on a carrier with a distance (`Float64`) they are interchangeable "
         "only up to a distance within the demanded tolerance, and precision can be traded for "
         "resources, which is where cost (G2) and the demand enter G0's quotient.", "settled"),
        ("Stated as a quotient: the implementations of a function are the quotient by \"compute the "
         "same function up to the law's equality\", one class per mathematical function, and inside "
         "the class the fibre of what differs; the class is chosen by law, the representative by "
         "cost.", "settled"),
        ("The class is exact in the theory (`Real`); in a model that carries a distance it is the "
         "ball of the demanded radius (`11` §3), and closeness is not transitive, so the planner "
         "substitutes one implementation for another only along a certified equivalence between the "
         "two, the identity law of L5 with its result `Bool` or `Cost` (D-2026-10-11-m).", "settled"),
        ("The law gives the candidates; the identity certificates say which the planner may exchange, "
         "and they form a weighted graph, not a class: a substitution is a path whose summed distance "
         "(`11` §2) is within the demanded tolerance, so two specimens joined through a third may "
         "each replace it and not each other; the sum is a bound only when every link is one (proved, "
         "exhaustive), otherwise an estimate with the weakest grade and the samples it was seen on; a "
         "lone implementation is never replaced.", "settled"),
        ("A sampled edge is admissible only on inputs the distribution it sampled covers, and only as "
         "a direct edge, never summed into a path, until a probabilistic bound exists as a law.",
         "settled"),
        ("The tolerance charged at a node is the demand's pulled back through the sensitivity of the "
         "cone from the node to the demand (`11` §5), and where no sensitivity is known there is no "
         "substitution.", "settled"),
        ("A link certified on a subtype is a link only at inputs certified (L3) in that subtype, so a "
         "path exists at x only where every link does; a `proved` link by citation carries the "
         "theorem's hypotheses as parameters and is void where they fail.", "settled"),
        ("The author's free choice among the inhabitants of an under-determined function "
         "(D-2026-10-11-d, P5) stays; the planner's choice is only among what has been compared.",
         "settled")],
    example="γ_n needs n·u < 1, false for float32 over an hour at 48 kHz, so the cited bound is void "
            "there (clause 10)",
    rests="O1 (the sum as a bound, the sensitivity), O2",
    status="settled; statement in his words, 2026-10-12; clause 3 is the proposed wording of his "
           "chat note",
    history="clauses 7, 8 and 10 (the weighted graph, the admissibility of sampled edges, the subtype "
            "and cited hypotheses) are the model's, from the rounds of critiques.")
L["L14"] = dict(
    statement="Luthier orchestrates other languages; what does not follow its way lives in a world; "
              "a foreign function is certified by delegation, and certification transports along "
              "equality.",
    clauses=[
        ("Types and laws are native; values may come through `extern` from Python or any host, "
         "declared over what they really receive and return, with description and verification kept "
         "on Luthier's side.", "settled"),
        ("(His words, \"si el tipo no sigue la ley no se aplica el calculo\") An extern is declared "
         "over a type, a type carries its laws (L2), and the extern is validated against them, like "
         "any other function, the first time an action asks for it, before it is applied, and refused "
         "if it fails; its certificate stays by hash; without a type with a law to validate against "
         "it is not applied; the agreement test with the native is in addition (W5), and the "
         "planner's substitution is D-2026-10-11-m.", "settled"),
        ("A function with no laws at all is not a function to run but a hole of a theory being "
         "defined (L4).", "settled"),
        ("The extern's certificate binds the host library's version and the platform (W10), and its "
         "declaration says whether it is a definition or an action (L11, L9).", "settled"),
        ("Certification is the default for every value: demanding a value demands every certificate "
         "in its dependency cone, paid once through the memo, unless the demand asks otherwise by a "
         "mechanism to be named (O3), which leaves a certificate of grade `assumed` (D-2026-10-11-n), "
         "since what could be done Luthier gives a way to do; `test` is the action that demands "
         "certificates without values (L10).", "settled"),
        ("Luthier is in use a coupling language: the joint between two libraries is a theory of which "
         "each is a model, the bridges between representations live at the joint with their cost and "
         "error, and no coupling without a law.", "settled"),
        ("A definition or an implementation that does not follow Luthier's way, an extern with no law "
         "yet, a foreign algorithm taken as is, is allowed inside a named world (L11): its "
         "certificates are `assumed` (D-2026-10-11-n), the plan shows the world it ran in, and "
         "nothing from it enters the planner's graph (L13) until a law is certified.", "candidate"),
        ("Verification by a theorem is `proved` by citation (D-2026-10-11-f); verification by "
         "delegation is the same mechanism with the host library's guarantee as the theorem cited "
         "(LAPACK's backward-error bounds, the condition number their hypothesis) and the library's "
         "version and platform as hypotheses the certificate carries; no new grade. A function known "
         "correct by a theorem outside Luthier is certified this way, and the chain law, citation, "
         "native, identity, extern is carried by hash.", "proposed"),
        ("(His correction) Certification transports along identity: if B is certified at grade g on "
         "inputs X and the identity A ≡ B is certified at grade h on inputs Y, then A is certified at "
         "the weaker of g and h on X ∩ Y, and by nothing else.", "mark pending")],
    example="with B's laws only `assumed` the transport gives A `assumed`, nothing; a lookup table "
            "equal to the native on a grid is certified on the grid and nowhere else (clause 9)",
    rests="O3 (the opt-out's syntax; the world as a value)",
    status="settled by his correction of draft 7; clause 7 candidate, clause 8 proposed on his mark, "
           "clause 9 his correction, his mark on the wording pending",
    history="clause 2 joins the two sentences of draft 10 on validation before application, which said "
            "it twice; clause 8 joins the two on `proved` by citation; the two counterexamples of the "
            "example are Kimi's and Claude's, from the third round; delegation (clause 8) is from the "
            "former L11 and transport (clause 9) from the former L21, placed here on his note of "
            "2026-10-12.")
L["L15"] = dict(
    statement="The core is minimal, executable by hand, and its programs are data.",
    clauses=[
        ("A handful of well-specified primitives, so that a program can be run with pencil and paper; "
         "everything else is a library whose translation to the core is mechanical.", "settled"),
        ("Hand execution is of the kernel given a plan, an order of execution that is a value "
         "(`lib/plan.lut`); the planner's choice among plans is outside the kernel.", "settled"),
        ("Four layers, each trusted differently: the kernel, checked by hand; the libraries and the "
         "interpreter in Luthier, certified against the kernel's laws; the host runtime, a specimen; "
         "the planner, advice that the plan records.", "settled"),
        ("A Luthier program is an element of Luthier; programs build, inspect and run other programs, "
         "and the interpreter is meant to be written in the language it interprets.", "settled")],
    rests="O11 (the kernel's theory stated in Luthier)",
    status="settled",
    history="")

# the From of L13 named G4, retired and no longer an entry
FROM_FIX = {"L13": ("and, before its retirement, G4 (every path expressible; now L13's own clause)",
                    "and, before its retirement in draft 9, the organizer \"expressive over restrictive\" "
                    "(every path expressible; now L13's own clause)"),
            "L5": ("the identity clauses from G1", "clause 4 from G1"),
            "L7": ("", ""), "L14": ("transport from G1 (the former L21)", "transport (clause 9) from G1")}

SECTIONS = [("G0", ["L4", "L5", "L9", "L10", "L11", "L12", "L13", "L15"]),
            ("G1", ["L2", "L3", "L7", "L14"]),
            ("G2", ["L6", "L8"])]

# ---- prose ----------------------------------------------------------------------------------------
PURPOSE = """## Purpose

One sentence, which is L1, heads the document: the language exists so that the invariances of a
discipline can be stated in it. Everything below says how."""

TERMS = """## Terms

Each term has one category and is defined here and nowhere else; the principles cite Terms.

- A *structure* is a type in the kernel's language (`04`), built from four forms: a product, a
  value made of several named fields (a record, a tuple); a sum, a value that is one of several
  cases, each tagged (a variant, an enumeration, `Maybe`); a function type `A -> B`; and a
  recursive type, one defined in terms of itself (a list, a tree). Each form may hold the others.
- A *predicate* is a function into `Bool`. A *cost* is a function into `Cost`, the non-negative
  reals with infinity, 0 true and ∞ false.
- A *law* is a predicate or a cost, or a combination of laws that is again a predicate or a cost;
  how laws combine is L6.
- A *theory* is a structure with its law.
- A *model* is an inhabitant of a theory: a value of its structure whose law is certified.
- A *function* is a value of a function type `A -> B`, in the standard sense. A function type with
  its law is a theory, and a function that satisfies it is a model of that theory.
- The *dependences* of a theory are the theories whose models its structure and law use
  (`Monoid A` depends on `Setoid A`; `VectorSpace K V` on `Field K`). A carrier is assumed to come
  with the models it names, `A` with its setoid, `K` with its field, so a theory reads them from
  the type (O2 for the syntax). Every theory has dependences; a function type has at least the
  setoids of its carriers, since its law uses their equality.
- A *certificate* is the record that a law was checked, with its *grade*: *proved*, by a theorem
  cited or by delegation to a library's guarantee; *exhaustive*, over every case; *cases*, over
  chosen cases; *sampled at a level*, over a sample drawn from a stated distribution; *assumed*,
  not checked. A proof is a certificate of grade proved. To *certify* is to produce one.
- *Evaluation* computes a function, and has no effect (L9). *Execution* is an action on the world
  (print, save). Writing a certificate into the store Luthier owns is an action on Luthier's own
  state, verified by reading the store back (L11); `test` is that action (L10).
- The *demand* is a request for a value from outside the program, an action, carrying the type and
  the tolerance it wants, the type possibly decorated: the value with its error, its derivative,
  its certificate. The *planner* is what chooses, among the models certified equivalent, the one
  that runs, and plans the decorated type the demand asks for.
- The *declarative face* of a program is what it states: its types, laws and definitions. The
  *executive face* is what the demands ask of it.

*Object* (`05 §3`) is not a term (O7)."""

TERMS_HISTORY = ("(History: the status paragraph of the Terms at draft 10: his list (D-2026-10-12-f); "
                 "the names structure, cost and certificate are the model's where he left a question "
                 "mark, marked OK by him on 2026-10-12; *dependences* replaces the model's \"dependent "
                 "theory\" on his note (every theory is one, so the emphasis goes on what it depends on); "
                 "the reading of certification as an action on Luthier's own state is proposed, kept by "
                 "him on 2026-10-12 with the clause \"never an action on the world\" removed as obscuring; "
                 "the carrier coming with its setoid and its field is his note of the same day, and "
                 "\"today the libraries pass them as parameters\" was the implementation's state. Draft 11, "
                 "step 3: the grades defined here, with the meaning each had across L2, L7 and L14; the "
                 "two faces named, since the organizers and the headings use them; nothing marked "
                 "proposed or open stays in Terms.)")

ORGANIZERS = """## The organizers

The guide and the two eurekas, in his order. An organizer is two sentences: what it says and what
it decides; it carries no mechanics and no status, and the principles under it are its section
below. The history of the eurekas and the P13 count are in the record."""

ORG_HISTORY = ("(History: draft 10's introduction: the guide, then the two eurekas, then the demand; "
               "renumbered on his note of 2026-10-12: G1 is theory and model (G2 until draft 9), G2 is "
               "cost (G3 until draft 9), G3 is the demand (G1 until draft 9). Draft 11, step 3: G3 "
               "dissolved into G0's second sentence and L10.1, as its own status asked (D-2026-10-12-s); "
               "its entry is the paragraph below.)")

PRECEDENCE = """## Precedence

When two statements conflict, the organizer they derive from decides; when two organizers
conflict, G0 decides; within an entry, the statement decides over its clauses. A clause marked
proposed, candidate or mark pending yields to one marked settled."""

PRINCIPLES = """## The principles of the language

Fifteen principles, each under the organizer it derives from, in the order of his six topics.
Each is a statement, the fixed part, and numbered clauses, each with its own status: settled,
proposed (the model's, awaiting his mark), candidate, or mark pending (his words, the wording
awaiting his mark). Where a clause has a worked example, the example follows the clauses; what
each entry rests on among the open questions is named. The Numbering table at the end maps the
numbers of drafts 1 to 10."""

PRINCIPLES_HISTORY = ("(History: draft 10's introduction: fifteen L in six topics, from the most general "
                      "to the most particular, renumbered on 2026-10-12 "
                      "(`record/plan-principles-reorder-2026-10-12.md`, his marks 14ea9f0); each heading "
                      "named the former numbers it joined; five merges, one new L on how laws combine, the "
                      "former L21 dissolved into the new L5, L7 and L14, the former L3 and L20 absorbed "
                      "into G1; formulations joined, not reworded, except where his note asked. Draft 11, "
                      "step 3: the six topics give the order inside each organizer's section and are no "
                      "longer headings, since a topic cuts across organizers (types, theories and models "
                      "has L2 and L3 under G1 and L4 and L5 under G0).)")

SECTION_HEAD = {
    "G0": "### Under G0, the guide",
    "G1": "### Under G1, theory and model",
    "G2": "### Under G2, cost",
}

OPEN = """## What is open

Only questions whose answer changes the language or the specification, each with the entries it
blocks; the done and implemented items are in the record's drafts table.

- **O1** (language) The algebra of costs. Its articulation is `docs/rationale/11-cost-valued-laws.md`
  draft 0: Ω replaced by [0,∞), quantitative equality, graded judgments, cost as −log p or as
  distance, how the uncertainty of a cost is represented in a certificate; the composition: a
  Lipschitz constant per function type where known (sensitivity types, Reed and Pierce 2010;
  condition numbers), a sampled cost where not, costs adding as −log p under independence; the
  interface of `Cost` in a certificate (a multiplicative constant where it exists, an additive
  defect where rounding enters, the grade as a lattice, the worst cost seen; `11` §5, §6); worked
  examples the sum of n floats, a matrix inverse with κ(A), a sampled probability integrating to
  one. Two candidate models (D-2026-10-12-p): min and max, or 1/n log-sum-exp with 1/n sum. The
  extension of Boolean logic to Lawvere and Bayes, which he names as another motivator or eureka;
  whether it is the third eureka or a principle of good use is his to mark after that analysis.
  Until it exists the application runs on a Boolean interim: laws of the form d(f x, g x) ≤ tol
  with tol a parameter (L12), every law returning `Bool` or `Cost` with the result type saying
  which (`11` §2, L5), no composition of tolerances along a chain, no run database. Blocks L2.4,
  L3.3, L5.5, L6, L8.3, L8.4, L10.4, L13.7, L13.9.
- **O2** (language) The type with its equality as the base case of every theory (a setoid; a
  metric space where the equality is a cost), the kernel's structural `==` its model for the
  decidable types (`05` R8), the equality of functions extensional and derived from it (L5), the
  equality of models componentwise; and whether a type names its equality as it names its model
  (`05` R13). Proposed by the model on his observation of 2026-10-12 (D-2026-10-12-e); his note of
  the same day on Terms goes the same way ("podríamos suponer que A viene con su Setoid", `K` with
  its `Field`); the syntax, how a type names its setoid and its field, is the open part. Blocks
  Terms (dependences), L5, L7, L13.
- **O3** (language) The opt-out of certification in a demand (D-2026-10-11-n, syntax open); the
  world as an opaque, unique value so that an action is never served from the memo (L9, L10);
  actions and the world as a value, designed and not implemented. Blocks L10.6, L11, L14.5, L14.7.
- **O4** (language) The composition of invariances (G1's derived route): which laws compose and how
  the demand selects them (audio 08.58, 32:01 to 34:07; audio 09.21). Blocks L10.18.
- **O5** (language) The decorated output (L10.4): the derivative by dual numbers as a model of the
  theory, the error by intervals or value-and-cost pairs once O1 exists; what in the planner
  chooses the model and inserts the bridges. Blocks L10.4.
- **O6** (language) Units as a candidate L under G0: a dimension is a proposition, dimensions form
  a group under multiplication, the quantities of one dimension a one-dimensional vector space,
  the whole a graded algebra; addition inside a dimension, multiplication across (second round
  §18). Precedent quimulun (his repository); pressure from sonolocalización (metres, seconds, the
  speed of sound). Blocks nothing.
- **O7** (spec) *Object* in the spec (`05 §3`, a strongly connected component of the dependency
  graph): not among the terms; in them it is a theory written in one cycle of names with its
  models, never a function. Proposed: `05 §3` becomes "theories are cycles" and the word survives
  only in "object classifier"; one commit over `04` and `05`; his decision (D-2026-10-12-f). Blocks
  Terms.
- **O8** (spec) The session as a block over the dataflow of L10: `<-` to explore, `:=` to lock, a
  file may contain a block, `<-` banned at the top level of a file (decided, D-2026-10-11-i); the
  spec's `04 §7` and a section on the session; the memo between the items of a session. Blocks
  L10.15.
- **O9** (spec) The kind of a hole in the elaborated form (L4.3). Blocks L4.3.
- **O10** (spec) `proved` by citation: the citation a `.bib` key with a resolved DOI, ISBN or URL,
  and who checked (human, ai+human, none) recorded; syntax `cite name bibkey checked ai+human`
  proposed, allowed in user code (D-2026-10-11-f as amended; to `05 §7`). Blocks L14.8.
- **O11** (spec) The kernel's theory stated in Luthier: `src/luthier/lib/kernel_laws.lut`, tested
  on `Fin 3`, `Fin 2` (`examples/kernel_finite.lut`, 10 laws, sampled); eta not statable (`05`
  R8), functions over `Fin n` not enumerated by `exhaustive` (to fix). Blocks L15.
- **O12** (spec) The identity of a result in the memo (L10.6) and `plan.lut` as its carrier.
  Blocks L10.6.

## His marks pending

- L5.5, the composition of identities as paths (his note of 2026-10-12 put in words).
- L6, the names lift, exact and within (his to rename), and clauses 1 and 5.
- L8.3 and L8.4, the correction on rounding.
- L10.4, the decorated output as another model.
- L13.3, the wording of his formula for the efficiency.
- L14.7, the world as a candidate; L14.8, delegation as citation; L14.9, the wording of the graded
  transport (his correction).
- The two faces defined in Terms, and the shape of this draft (D-2026-10-12-g, -s)."""

KEYS = """## Keys

- G0, G1, G2: the organizers above; L1 to L15: the principles; L10.4: clause 4 of L10.
- O1 to O12: the open questions above.
- D-2026-10-11-n and the like: decisions, in `record/decisions.md`.
- P1 to P15: the principles of the method, `record/principles.md`.
- W1 to W15: the way of working, `docs/way-of-working.md`.
- `02` to `08`: the specification, `docs/spec/02-grammar.md` to `08-tests.md`; R1 to R13 the rules
  of `05`, the static semantics; `11`: `docs/rationale/11-cost-valued-laws.md`, and `01`, `07`,
  `09`, `10` the other rationale documents.
- His words, his annotation, his correction, his reading, his formula: Luciano's; a clause without
  such a mark is the model's."""

# ---- rendering ------------------------------------------------------------------------------------
def field(name, text):
    first = f"{name}:" + " " * max(1, 12 - len(name) - 1)
    return textwrap.fill(text, width=100, initial_indent=first, subsequent_indent=" " * 12,
                         break_long_words=False, break_on_hyphens=False)

def head_line(tag, stmt):
    return textwrap.fill(stmt, width=100, initial_indent=f"{tag}" + " " * max(1, 4 - len(tag)),
                         subsequent_indent="    ", break_long_words=False, break_on_hyphens=False)

def clause_line(tag, n, text, status):
    first = f"{tag}.{n}" + " " * max(1, 7 - len(f"{tag}.{n}"))
    return textwrap.fill(f"{text} [{status}]", width=100, initial_indent=first,
                         subsequent_indent=" " * 7, break_long_words=False, break_on_hyphens=False)

def references(d):
    text = " ".join(t for t, _ in d["clauses"]) + " " + d.get("example", "")
    ds = sorted(set(re.findall(r"\bD-\d{4}-\d{2}-\d{2}-[a-z]+\b", text)))
    docs = sorted(set(re.findall(r"`\d\d(?: §\d+)?`(?: R\d+)?", text)))
    ws = sorted(set(re.findall(r"\bW\d+\b", text)), key=lambda w: int(w[1:]))
    ps = sorted(set(re.findall(r"\bP\d+\b", text)), key=lambda w: int(w[1:]))
    return "; ".join(x for x in [", ".join(docs), ", ".join(ds), ", ".join(ws), ", ".join(ps)] if x)

def l_entry(tag):
    d, o = L[tag], old[tag]
    out = [head_line(tag, d["statement"])]
    frm = o["From"]
    if tag in FROM_FIX and FROM_FIX[tag][0]:
        assert FROM_FIX[tag][0] in frm, (tag, frm)
        frm = frm.replace(*FROM_FIX[tag])
    frm = re.sub(r"\bG3\b", "G0, the demand", frm)
    frm = re.sub(r"\bL21\b", "the former L21", frm) if "the former L21" not in frm else frm
    out.append(field("From", frm))
    for n, (text, status) in enumerate(d["clauses"], 1):
        out.append(clause_line(tag, n, text, status))
    if d.get("example"):
        out.append(field("Example", d["example"]))
    refs = references(d)
    if refs:
        out.append(field("References", refs))
    if d.get("rests"):
        out.append(field("Rests on", d["rests"]))
    if "Quote" in o:
        out.append(field("Quote", o["Quote"]))
    out.append(field("Source", o["Source"]))
    out.append(field("Status", d["status"]))
    hist = o["History"] + " " + STEP + (" " + d["history"] if d["history"] else "")
    out.append(field("History", hist))
    return "\n".join(out)

def g_entry(tag):
    o = old[tag]
    stmt, form = G[tag]
    out = [head_line(tag, stmt), field("Tier", G_TIER[tag]), field("Formulation", form)]
    if "Quote" in o:
        out.append(field("Quote", o["Quote"]))
    out.append(field("Source", o["Source"]))
    out.append(field("History", o["History"] + " status at draft 10: " + o["Status"] + ". " + G_HISTORY[tag]))
    return "\n".join(out)

def old_entry_as_text(o):
    e = old[o]
    bits = [f"{o} {e['statement']}"]
    for n in ("Tier", "From", "Formulation", "Quote", "Source", "Status", "History"):
        if n in e:
            bits.append(f"{n}: {e[n]}")
    return " ".join(bits)

def hist_para(text):
    return textwrap.fill(text, width=100, break_long_words=False, break_on_hyphens=False)

# ---- the head of the record: drafts table row, numbering table ------------------------------------
lines = record_text.splitlines()
terms_i = next(i for i, l in enumerate(lines) if l.strip() == "## Terms")
head = "\n".join(lines[:terms_i]).rstrip("\n")
num_i = head.index("## Numbering")
head_before, numbering = head[:num_i].rstrip("\n"), head[num_i:]
DONE_ROW = ("| record | 2026-10-12 | this file | Step 3 of the draft 11 plan (D-2026-10-12-g, -s): the shape "
            "applied by `scripts/migrate_record_draft11_shape.py`, nothing reworded. Done items that stood "
            "in What is open until draft 10: in the spec on 2026-10-11, blocks (`02 §9`, `04 §5`, `05` R12, "
            "D-2026-10-11-i); operators by the type naming its model (`05` R13, D-2026-10-11-j; "
            "`examples/z7ring.lut` rewritten, Z7 its own type and `mod 7` a certified homomorphism); "
            "Python-like separators (`02 §1`, D-2026-10-11-k); `cite` and `proved` by citation (`05 §7`, "
            "D-2026-10-11-f); `lib/laws.lut` split from `algebra.lut` (D-2026-10-11-l). Implemented "
            "2026-10-11 in the interpreter: blocks and the session (`luthier session`), defaults and named "
            "arguments, R13's refusal of two models on one type, `cite` with `.bib` modules, exhaustive "
            "tables of `Fin n -> T`; `lib/plan.lut` states an order of execution as a value and confluence "
            "as a law, checked exhaustively in `examples/plan_confluence.lut`. |")
step1_row = next(l for l in head_before.splitlines() if l.startswith("| record | 2026-10-12 | this file | Step 1"))
head_before = head_before.replace(step1_row, step1_row + "\n" + DONE_ROW)
assert DONE_ROW in head_before
numbering = numbering.replace(
    "| G3 | G1 | the demand, printed third |",
    "| G3 | G1 | the demand, printed third in draft 10; dissolved in draft 11 into G0's second sentence and L10.1 |")
numbering = numbering.replace("| L1 | L1 | kept |", "| L1 | L1 | kept; the Purpose section since draft 11 |")
numbering = numbering.replace("| Draft 10 | Before | What happened |", "| Draft 10 and 11 | Before | What happened |")
assert "dissolved in draft 11" in numbering and "Purpose section" in numbering

# ---- assemble --------------------------------------------------------------------------------------
out = [head_before, "", numbering.rstrip("\n"), ""]
out += [PURPOSE, "", "```", l_entry("L1"), "```", ""]
out += [TERMS, "", hist_para(TERMS_HISTORY), ""]
out += [ORGANIZERS, "", hist_para(ORG_HISTORY), ""]
out += ["```", "\n\n".join(g_entry(g) for g in ("G0", "G1", "G2")), "```", ""]
out += [hist_para("(History: G3 at draft 10, dissolved in draft 11: " + old_entry_as_text("G3") + ")"), ""]
# the (History:) paragraphs of step 1 that stood in the organizers' block are kept
for k, item in pp.parse_record(record_text):
    if k == "prose" and item.lstrip().startswith("## The organizers"):
        for para in re.split(r"\n\s*\n", item):
            if para.lstrip().startswith("(History:"):
                out += [para, ""]
out += [PRECEDENCE, ""]
out += [PRINCIPLES, "", hist_para(PRINCIPLES_HISTORY), ""]
for k, item in pp.parse_record(record_text):
    if k == "prose" and "(History: the former L20" in item:
        for para in re.split(r"\n\s*\n", item):
            if para.lstrip().startswith("(History:"):
                out += [para, ""]
for g, ls in SECTIONS:
    out += [SECTION_HEAD[g], "", "```", "\n\n".join(l_entry(t) for t in ls), "```", ""]
out += [OPEN, "", KEYS]
text = "\n".join(out).rstrip("\n") + "\n"
RECORD.write_text(text, encoding="utf-8")
print("wrote record:", len(text.splitlines()), "lines,", len(text.split()), "words")
