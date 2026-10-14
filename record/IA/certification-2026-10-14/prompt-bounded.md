# The store bounded: an entry per filling, up to four; stale entries pruned, brief for a Sonnet agent

Written 2026-10-15 by the coordinating session (luthier-3e). The stores (`src/luthier/lib/
*_model.cert.json`, `tests/tester/*.cert.json`) hold 2.7 MB and grow by about 9000 lines at each
re-certification, because `record` never removes an entry. 6.S8: "An entry is kept per filling
of the holes its cone depends on, up to four"; 12.S11: a stale entry is kept and marked.

## The prompt

Read `CLAUDE.md` first, then `docs/spec/06-certification.md` 6.S8 and `12-files-and-tools.md`
12.S11, 12.S16, `src/luthier/lib/certification.lth` §1 (`Store`, `record`, `known`: what the laws
say and do not say about removal), `src/luthier/certify.py` (`record`, `add_entry`, `write_store`,
`stale`, `read_store`). Another agent writes new theory files `plot.lth`, `plot_model.lut`: touch
nothing under `src/luthier/lib/` but reading; change `src/luthier/certify.py`,
`src/luthier/lib/certification.lth` only if a law must say what you implement (then one commit
by its path, [proposed], message ending "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"),
`tests/test_certify.py`.

1. On every write, a store keeps per (law, binding) at most four entries at the current cone
   hash, the four most recent by date (6.S8's "per filling, up to four", read as: per identity
   without the seed and `n`, [proposed]); older ones go.
2. Stale entries (another cone hash or another interpreter revision) are kept only as the most
   recent one per (law, binding) and dropped once a current entry exists for that pair
   ([proposed], 12.S11 says kept and marked, not forever).
3. `Store`'s predicate still holds; `known` still finds a current identity; `--deep` unchanged.
4. Rewrite the existing stores by the same rule (`luthier certify --prune FILES` or a step at
   write time: say which), paste the sizes before and after, and check `luthier run
   tests/run/vector_norm.lut`, `maximize_quadratic.lut`, `table_cell.lut`'s neighbours still run
   certified, and the suite passes.

Check: `PYTHONPATH=src python3 -m pytest tests/test_certify.py tests/test_run.py -q`, then the
suite. Do not commit the Python or the stores (the coordinator does; list the stores' new
sizes). Report in your final message.
