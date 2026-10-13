# Expected lambda domains

Source: user request 2026-10-13, prompt v1; inputs at HEAD `0a0f6504b0289101b16a8470551f418cf8c84fa7`, original SHA256 elaborate.py `c8a88a14212fa3b4e04d8a12674b538d4f860541b374b453503c376292f35e77`, test_elaborate.py `70897f93869c0102a6e2f1d57da5a4b57c60005d4ccdbfd85a72f93c780ba759`. Method: Codex edits under that prompt, deterministic (no random seed); source laws: `src/luthier/lib/translation.lth`, Lambdas/ActsCurried; separate predicate declaration: check.py 4.R6.

Decisions taken independently: preserve prior declarations, pass expected argument/block-binding types, instantiate dependent binder names, and use a separately declared base as a predicate lambda domain; retain Hole without a known domain. Added regression tests for declarations, binder and arrow argument positions, dependent/implicit arguments, block bindings, and unknown domains. Only elaborate.py and test_elaborate.py edited besides this report; no commit.

Validation: system python3 lacks pytest; ran the requested commands with `PATH=/tmp/luthier-grammar-render-venv/bin:$PATH PYTHONPATH=src`. Focused: **97 passed, 19 xfailed, 1 strict XPASS**; full tests/: **375 passed, 19 xfailed, 1 strict XPASS**. The only newly passing strict xfail is `test_spec_program_syntax[r6_predicate_body.accept.lut]`; every test_elaborate.py law passes. test_spec.py unchanged.

Remaining checks: k_recursor has 4.R6 Recursor, 4.R2 RecZero/RecSucc, and 4.R9 add (succ is inferred as an implication application rather than a function; lambda k/r domains are now N); r12_block has only 4.R2 shift, with its lambda-related 4.R9 removed. Concurrent program.lth edits were observed and left untouched; no failures outside scope were repaired.
