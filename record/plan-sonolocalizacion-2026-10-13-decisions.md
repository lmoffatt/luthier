# Luthier in sonolocalización, then in macroir: the decisions

Draft 0, 2026-10-13, by Claude Opus 5.5, written without reading sonolocalización (to spare the
quota); the inventory is the first step of the execution. Mark under each: "ok", "no", or a comment.

## S1. The target is a vertical slice, not finished layers

The plan from zero completes each layer (checker, certification, execution) before the next, and
the domain libraries come after `v0.4`. Sonolocalización needs a little of every layer: evaluation,
some checking, certification of its laws, externs to numpy, reading its data, and a few domain
libraries. Recommended: after layer 0 and `kernel.py`, reorder the plan to reach the minimum that
runs one analysis of sonolocalización end to end, then fill the layers. Costs: parts of layers 1
to 3 written twice (a minimal version, then the full one); gains: Luthier is used on real work
weeks earlier, and what sonolocalización needs shapes what is written first.

## S2. The core stays in Python for this

The Rust core (Z10) is not on the path: the heavy computation goes to externs. Recommended: Rust
after sonolocalización runs.

## S3. Numerical libraries are externs, models of Luthier theories

numpy and scipy as today; for gradients and compiled numerics JAX (pure functions, `grad`, `jit`,
`vmap`, closest to Luthier's style), or PyTorch. Each enters as an extern certified against a
Luthier theory (a gradient against finite differences, its tolerance a parameter, P11 (every
criterion is a parameter)). Recommended: JAX, when the inventory shows a need for gradients.

## S4. macroir after sonolocalización

Same method, its own inventory, once the slice for sonolocalización runs.

## S5. Working in VS Code

A language server (syntax colours generated from `luthierSyntax`, parse errors now, the checker's
errors and certificate status later), and Jupyter notebooks for exploration once `v0.4` gives a
session. Recommended: the minimal extension (colours and parse errors) as a Codex task at the
start of the next cycle.
