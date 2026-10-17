`arrays_model.recertified.cert.json` is src/luthier/lib/arrays_model.cert.json as the `--deep` re-certification of 3j j2a left it (written 2026-10-17, moved here from record/IA/regions-2026-10-17/, where commit ef6ec51 put it). It holds two refutations, kept as evidence (P3: the original evidence and its correction):

- PinvSymmetric, seed 20261014, n 100, cone sha256:55d4ddaf3320, entry of 2026-10-17T12:37:42: refuted at a 10 x 10 symmetric matrix of rank 9 (a zero row and column, the rank-deficient family of 7.S5).
- PinvScales, seed 20261014, n 100, cone sha256:af389dd97fd0, entry of 2026-10-17T12:47:33: refuted at a 5 x 5 matrix of rank 4 and c = 8.361370115381893.

The two matrices are in `pinv-counterexamples.json` (moved from the same folder, commit 6b3d23c), with how they were drawn.

Why they are archived and not the law's standing: numpy was right to within rounding in both. The laws' error model was wrong: each compared with the scale of one entry only, so an exact zero on one side (an entry of a zero row) allowed no difference at all, while its computed twin carries the rounding of a whole product. The coordinator's answer to report-code.md's question (2026-10-17): compare with the scale of both entries plus a normwise term (Higham 2002, section 3.5). The corrected laws are at new cone hashes, so these entries are stale for them; they stay here as what the old error model gave.
