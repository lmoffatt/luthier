# world.lth after round 1: Host against the Console, the laws as predicates over observed cases

Written 2026-10-15 by the coordinating session (luthier-3e). Items 1 and 3 of `summary.md`'s top
screen in this folder, and W1 to W8, M1 of its world.lth and world_model.lut sections: read them
there (the replies under `A/` only where the summary quotes a counterexample: Kimi's no-op host,
GPT's pure predicate).

## The prompt

Read `CLAUDE.md`, then `summary.md` (the top screen, the world sections, the not-sure list),
`src/luthier/lib/world.lth` whole, `world_model.lut`, `docs/spec/10-world.md` 10.S5 to 10.S10,
D-2026-10-13-a and D-2026-10-14-c in `record/decisions.md`, and how run.py validates today
(`record/IA/certification-2026-10-14/report-first-action.md`, read only; no Python changes in
this bite). Change world.lth and world_model.lut only, one commit each by path
("Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"); the report through the shell to
`report-fix-host.md` in this folder, committed alone.

1. W1 (item 1): `Host S` takes the `Console S` model and its descriptions are the console's, not
   fields the host fills; a host-side law that the places not declared do not change across an
   action (10.S7), stated over an observation of a list of places the certifier supplies (a
   parameter); the observer's fidelity stated as what it is, a root of trust cited or assumed
   (the grade for what is not checked), in one law marked so and in the comment.
2. W2 (item 3): the agreement laws as pure predicates over an observed case (before, the
   arguments, after, the result), and `agreement` the action that gathers the case and returns
   the token and the action's result to the program (GPT's form; D4 kept: the token used once);
   say in the comment where a law over `W` sits in certification (the first-action check gives
   one case; whether one case serves the whole run is Luciano's question, left as such).
3. W3 (the declared type in `Route`), W4 (quantify over own descriptions and provisional routes),
   W5 (`RecordCrossesByField` over records of two or more fields, each counted apart), W6
   (`OwnIsIdempotent` includes the result), W8 (`settled` takes the cutoff as a parameter, the
   demand's), M1 (`"stdout"` not a file place for `Host`'s readFile as `Console` already
   excludes it).
Accepted when: both files parse and `luthier check` clean; the report lists per item the law as
it reads now, quotes it, and says what run.py's first-action validation must change (one line
per law) for the coordinator's next bite; nothing of W7 (the provisional extern, Luciano's).
