# Waves 2 and 3 of the specification: what waits for your marks

Draft 0, 2026-10-13, at 7410d5e. The twelve chapters of `docs/spec/` now exist. Chapters 5 and 6
were written by the integrating session, and 8, 9 and 10 by three Sonnet agents on the briefs in
`record/spec-briefs/`. This lists every `[proposed]` item of those five chapters and the agents'
questions. Mark as before: "ok" under a line, "no" or a comment; unmarked stays proposed.

## First: the interfaces asked of libraries

By D-2026-10-12-al every open choice went to a library, and each chapter states only what the core
asks of that library. These tables are the one thing a library can never change later, so they
are worth your attention more than anything else here. Each one asks for as little as the chapter
could manage.

- 5.S3, a law's value: one operation, `verdict : V -> C`. It is `lift` for `Bool`, the identity for
  a cost, and `lift` of `holds` for a check.
- 5.S5, a sixth law for 6.S5: `⊤ ≤ 0` is false. Without it the trivial algebra (`0 = ⊤`) satisfies
  the five laws you approved and breaks `exact (lift b) = b`, which L12.2 settles.
- 8.S2, a demand: `entry`, `cutoff` (compared by `≤`), `delta` (the confidence), `assumed` (the
  evidence cost of assumptions, absent means refuse), `key` (what enters a result's identity).
- 9.S14, a ranking: `rank` from a cost, the resources and the demand's weight to a value; a total
  preorder on that value; a path of cost `0` ranks no worse at equal resources. D-2026-10-12-u's
  `cost + w·log resources` is its first candidate model (9.S15).
- 10.S5, a world: a token `W` with no `==` that a program never builds; `act`, which gives a new
  token each time, so the memo never merges two actions; `own`, which marks an action on Luthier's
  own store as idempotent.

## Chapter 5. Laws

- 5.S10, checks and `Failures E` go to a library, `lib/checks.lut`; the core sees them only through
  `verdict`.
- 5.S12, three forms a check can take beyond its failures: a witness, a statistical verdict with its
  level, a tolerance kept in the type.
- 5.S13, translations between presentations as a pair `to`/`from` whose round trip is the identity.
  Version 0 can express them per model; naming and certifying them as a concept is later work.

## Chapter 6. Certification

- 6.S6, the fields of a certificate: law, domain, bound, evidence cost with its derived grade, and
  identity. Today the bound and the evidence cost are not recorded.
- 6.S8, a new check keeps the old certificate beside the new one (L10.4). Today it replaces it, and
  only git keeps the chain.
- 6.S9, proved by delegation: a host library's documented guarantee cited as the theorem.
- 6.S13, no operation on certificates gives evidence for free, as a law of the theory.
- 6.S16, `lib/certification.lut` states the chapter, with `CostAlgebra C` and `grade`, which holds
  the correspondence of the old grade names (the answer proposed for D-2026-10-12-ag).

## Chapter 8. The demand and the plan

- 8.S1, a demand is a value: entry, cutoff, δ, the cost of assumptions, limits on resources;
  nothing else is a parameter of it.
          Justamente la demand es una compuerta por la cual pasar parametros que modifiquen el comportamiento del programa, porque cerrar los parametros sin razon?
          La forma de setear los parametros es simple: al pedir un determinado tipo de entrada a la funcion  f: (t: P T)->W , yo se que necesito que t sea un P T y entonces veo si el cono de t permite construir un P T y lo construyo. 
          Ahora esto implica que todo el cono que trabajaba para hace T ahora tiene que hacer P T y eso deberia ser posible. 
          Una forma es que sea un codigo generico sobre (G T) (donde G puede ser Identity ) y entonces reemplazo G por P. 


- 8.S11, `lib/plan.lut` gains the memo key, a function from a demand and a program to a plan, and
  the law that the key changes when any input changes. 
          No se que es el memo key, elabora
   


- 8.S15, a trace library would offer `record d p r`, append-only.
- Question of the agent: may a result computed under a tighter tolerance serve a looser demand?
  8.S9 asks for equal keys for now. Mine: keep equal keys until a case asks (P8, no more
  bureaucracy than it pays for); certificates already serve looser demands (6.S15).
- Question of the agent: L5.6 lists more in a result's identity than D-2026-10-10-d (the type
  demanded, the tolerance, the seed, the plan, the certificates). Mine: L5.6 extends it, as written.

## Chapter 9. Specimens and the planner

- 9.S3, the host is a specimen of what Luthier states; an extern that cannot be validated is never
  offered to the planner.
- 9.S8 and 9.S11, the two regimes (decidable carrier, carrier with a distance) and the tolerance
  charged at a specimen from the demand's, with no substitution without a known sensitivity.
- 9.S12, a path is memoized by its links; in-place mutation is a choice of the plan.
- 9.S13, resources measured per specimen and input shape, kept apart from certificates.
- 9.S17, `lib/planner.lut`.
- Question of the agent: 9.S8 and 9.S11 restate L6.4 and L6.8, settled in the principles but with
  no decision id, so a chapter can only mark them proposed. Mine: let `check_spec.py` accept a
  settled clause as a status, `[decided L6.4]`; this is the first real case for it.

## Chapter 10. Actions and the world

- 10.S3, an action is told by its type: a function that takes and gives a `W` is an action, one
  that mentions no `W` is a definition. No new checker rule is needed.
- 10.S4, the world is a token threaded through actions, one token or one per part as the library
  chooses.
- 10.S12, a foreign algorithm with no law runs in a named world, a parameter of the demand,
  priced as an assumption (L11.6, a candidate).
- 10.S13 and 10.S14, `lib/world.lut`, and what the chapter leaves to libraries (traces, equality
  of consequence, observations, classes of machines).
- Question of the agent: L11.7 (a file is read when a demand needs it) is proposed in the
  principles while D-2026-10-12-ac, your decision, is current. Mine: mark L11.7 settled.
- Question of the agent: the validation of an extern at the first action that asks has no decision
  of its own and is cited through D-2026-10-11-n, whose text carries it. Mine: leave it so.
OK