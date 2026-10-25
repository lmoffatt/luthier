# Brief: waves B and C begin, after Luciano's answers (D-2026-10-25-a)

Luciano answered the five questions as recommended (D-2026-10-25-a), adding to question 1:
"Luthier should provide the mechanisms for defining any reasonable choice, as long as we do not get
into an infinite loop." So the capped sum is the default composition of evidence, and the
composition is a parameter a theory or a demand can choose among reasonable ones (P11: every
criterion is a parameter), each such choice a structure claimed and certified, never one that can
loop (it must be a total function, as the language's totality already asks).

Two agents start now, split by files:
- Agent B2 (Fable): bite B2 of `execution.md`, the evidence and error bases in the core, with the
  addition above: the evidence base's tensor is a parameter, the capped sum its default, the nats
  sum under declared independence a second claimed instance. Files: src/luthier/lib/core/structures/
  (algebraic.lth, equality.lth) and new test programs for them. Don't touch properties/functions.lth.
- Agent C1 (Opus): bite C1 of `execution.md`, the `Within` form and the bound transformer. Files:
  laws.lth, tester.py, certify.py, demand.lth, run.py, src/luthier/lib/core/properties/functions.lth,
  arrays.lth and numbers.lth where `dot` and the identity laws live, their test programs and tests.
  Don't touch core/structures/.

Each: read `CLAUDE.md`, `execution.md` (your bite, its sources and criteria), `decisions.md` with
Luciano's answers, D-2026-10-25-a. Tests that fail before and pass after; commits as they pass,
staged by path (subject, blank line, one body line, ending with "Co-Authored-By: Claude <Fable 5.1
or Opus 5.5> <noreply@anthropic.com>"). Run with `/home/lmoffatt/miniconda3/bin/python` and
`/home/lmoffatt/miniconda3/bin/luthier`; certify six programs at a time (`xargs -P6`, each with its
own log) under ~/.cache/luthier-wave-bc/<agent>/, never /tmp; long runs waited for in the
foreground with bounded waits. C1's re-certification of every agreement law is its own; B2
certifies its new claims. Report: `report-<bite>.md` beside this file, committed; if your Write is
refused, give its full text in your final message. Per bite: what you did, commits, checks,
decisions taken on your own, at most one question.
