# Brief: a read-only audit of two foundations of certification

Read-only: change no file. Your final message is the report, in English, in Markdown; the
coordinator saves and commits it. Never run `luthier certify`, `test` or `run` (they write stores and
records); probe in memory with PYTHONDONTWRITEBYTECODE=1 and PYTHONPATH pointing at the repository's
src, with /home/lmoffatt/miniconda3/bin/python.

The coordinator named four foundational risks to Luciano on 2026-10-27; the kernel's identity in the
cone is decided (D-2026-10-27-a) and the evaluator's scaling is being worked on. Audit the other two:

1. Is sampled evidence what it claims? `certify.epsilon_hat` (bite B1, report-b1-b3-d1.md) gives ε̂
   by the rule of three, min(1, −log δ / n), which assumes n independent draws from the declared
   distribution. Read the generators (src/luthier/generators.py, src/luthier/lib/generators.lth and
   generators_model.lut, the tester's drawing in tester.py, `scrambled` and the golden-ratio
   multiplier of report-wave-a-3b.md, which found consecutive seeds giving 100 draws within 0.2% of
   [0, 1) with another multiplier). Say what the generator is (an LCG? its modulus and multiplier),
   how a line's n cases get their seeds, whether the draws are independent enough for the rule of
   three to hold, and test it: run standard statistical checks on the draws a real line makes (serial
   correlation, a chi-square on uniformity, the spectral test of the multiplier, runs between
   consecutive seeds), in memory. If it fails, say what replaces it (a counter-based generator such
   as SplitMix64 or Philox) and what moves (every sampled identity).
2. Is the identity of an entry complete? Everything that can change a result must be in its identity
   (the cone hash, the fingerprints, the drawing revision, the host hashes). Bite 13c found sampling
   budgets missing; the kernel was found missing (now decided). Look for what else is missing: the
   platform (CPU, the BLAS numpy links, its threading, the floating-point environment: rounding mode,
   flush-to-zero, fused multiply-add), Python's version, the random state of hosts (numpy's global
   RNG used by an extern), environment variables, time. For each: whether it can change a result
   (probe where you can: numpy's dot with different thread counts, a sum order), whether it is in the
   identity now (cite the code), and the smallest fix.

Order findings by severity, with file and line, a concrete scenario, and the smallest fix. Say
plainly what looked sound. Read CLAUDE.md, spec chapter 6 (6.S8), chapter 7, record/decisions.md
around D-2026-10-16-g and D-2026-10-25-a. Write for the coordinator and Luciano: no em-dashes as
punctuation, numbered references with their statement at first use.
