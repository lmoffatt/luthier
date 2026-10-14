| Item | Line in the artifact | Class | One sentence | Decision it would change |
|---|---|---|---|---|
| A1 | world.lth 15-18 | 2, L4.11 | The reading of L4.11 (W is opaque and unique, a primitive with no introduction) makes the table of 10.S5 the whole interface, and the item notices the `act` row is missing from the header. | No decision; a header comment. |
| A2 | world.lth 59 | 1 (with B1) | Both say `Action A = W -> W * A` is the wrong shape for actions that take arguments after the token. | Token-last would change the order of 2.S17 (`w1 <- print w0 "x"`) and D8 behind 10.S3; the alternative (drop the alias) changes nothing. |
| A3 | world.lth 59, 66 | 3 | `World`, `W` and `t.World` share one word; no clause speaks of names. | No decision; a rename. |
| A4 | world.lth 66, 91-93, 201, 226; world_model.lut 15, 20-22 | 5 (otherwise 1 with B11) | Asks the world to carry an equality of "read at every place" (a law of the representation) in place of structural `==` on states. | D-2026-10-13-a (the comparison before and after by the representation's `==`, cited in the header). |
| A5 | world.lth 61-65, 87-93, 222-226 | 5 (otherwise 1 with B3) | Asks that the host, not only `describe`, be checked to change nothing at undeclared places, which is `ChangesOnlyDeclared` for the host and is not stated. | 10.S7 (certified for the host) and the §5 protocol of D-2026-10-13-a. |
| A6 | world.lth 71, 223 | 3 | Splits `places` into `reads` and `writes`; no clause produces it. | No decision recorded on `places` as one list; it changes the `Described` structure. |
| A7 | world.lth 81-83 | 5 (otherwise 1 with B4) | Asks that idempotence of an own action cover the result `A` too, a law of the memo that is not stated. | 10.S6 (an own action may be served from the memo). |
| A8 | world.lth 70-73 | 2, L4.11 | L4.11 says an action on the world is never memoized, which is the "safer reading" the comment gives, and the item finds `own : Bool` has no home for "declares nothing". | 10.S6 (the default for an undeclared action). |
| A9 | world.lth 85-95 | 5 (otherwise 2, L10.4) | Asks for a law that the store only grows (earlier certificates stay), which 10.S7 states in prose and the file leaves out; L10.4 (frozen snapshots, supersession) is the clause behind it. | 10.S7 (its second half), or a comment saying it waits. |
| A10 | world.lth 97-109; world_model.cert.json | 3 | Compares the comment "never a sample" with the store's `Cases` entries and notes `Persistence` carries its own `World`; read off the files, not from a clause. | 10.S13 (what is assumed) for the grade; the shared parameter is no decision. |
| A11 | world.lth 92-93, 105-108; host.py 71-84; world_model.lut 21 | 1 (with B10) | Both find that `"stdout"` and file paths share one namespace; A adds aliasing of paths. | No decision; the header comment "places are any string" would change. |
| A12 | world.lth 118, 186; world_model.lut 12, 28 | 2, L2.1 | L2.1 (a declaration without a body is a hole and cannot be run) is the reading that makes `appendStr` and `hash` without body a finding; B8 shares the unused `hash` only. | No decision (declared "until core names it"). |
| A13 | world.lth 119, 128-132 | 2, L11.4 | L11.4 (the certificate binds the host library's version and the platform) produces the finding that `Route` and `verdictOf` carry no declared type, version or platform. | Implements 10.S8 (an extern has a declared type); no decision changed. |
| A14 | world.lth 133-139; run.py ACCEPT | 1 (with B6) | Both find that `settled` fixes which grades count and ignores the demand's cutoff; A also names L5.17 and L5.18. | `settled` of §3 and 10.S10 / 6.S10 (the demand prices the evidence). |
| A15 | world.lth 135-139; run.py 1582-1593 | 1 (with B7) | Both find that `AppliedWhenSettled` (provisional applied) contradicts `refuse_provisional`. | 10.S10 against 4.R5, 6.S14 and 12.S17: one of them has to give. |
| A16 | world.lth 128-144, 217; run.py 1514-1579 | 5 (otherwise 1 with B2 and B25) | Asks that `Host S` be a theory whose law is `agreement` (the law "the host agrees with its description"), which the file states only as a protocol and a comment. | L11.2 as applied to `hello.lut`; D-2026-10-13-a; the `done` of §5. |
| A17 | world.lth 30-50 | 1 (with B30) | Both find the continuation note to "a session or Codex" in a theory file; A adds that `done` means stated. | No decision; a comment and the status words. |
| A18 | world.lth 140-143 | 5 (otherwise 1 with B8) | Asks that identity be stated to carry the hash and a second identity be stated, laws the theory could state and `IdentityCarriesHash` does not. | 10.S9 (two identities, the result's and the certificate's). |
| A19 | world.lth 121-127 | 5 (otherwise 2, L11.2) | Asks a temporal law (validated the first time an action asks), which L11.2 and 10.S10 say in prose and no law states. | 10.S10, last sentence (the moment is not what runs today). |
| A20 | world.lth 146-177 | 5 (otherwise 1 with B9) | Asks that `Crossing` cover records of fields of different types, an absent label, and counts apart per callback. | D-2026-10-14-a (record crossing by field) and 12.S18 (the count). |
| A21 | world.lth 146-160; run.py 828-847; host.py 53-57 | 1 (with B23) | Both find that counts of distinct crossings merge under one key. | D-2026-10-14-a, which names the count and not its key. |
| A22 | world.lth 161-177; run.py 829-833 | 5 (otherwise 1 with B22) | Asks that `Crossing` say what a failing callback gives the host. | No decision recorded on failure; the case is unstated. |
| A23 | world.lth 148-160; run.py 795-826 | 1 (with B24) | Both find that a function over `Fin n` is always evaluated at all `n` points before the host sees it. | 3.S23 (the cost is `n` evaluations). |
| A24 | run.py 706, 927-928, 965-966; host.py 87-90 | 1 (with B18) | Both find that `from_host` accepts anything for the token. | No decision; enforces 10.S4 and 10.S5. |
| A25 | run.py 706-708 | 5 (otherwise 2, L4.7) | Asks for a law that an extern with no `W` in its type leaves the world unchanged (`DefinitionsAreInert`); L4.7 (a definition depends only on its inputs, a law a dataflow is certified against) is the clause. | 10.S3 ("the check is then the type's, spec 4 needs no new rule"). |
| A26 | run.py 746-752, 971-977 | 1 (with B17) | Both find `Nat` and scalar `Int` unchecked at the bridge while arrays check 64 bits. | No decision; 11.S8 if scalars are meant unbounded. |
| A27 | run.py 786-793 | 1 (with B16) | Both find the `2 ** 1024` guard lets `float(x)` raise `OverflowError`. | No decision; a fix. |
| A28 | run.py 753-784, 963-1010 | 1 (with B19) | Both find typed branches that fall through to the untyped reader; B adds the bare value for `Maybe`. | 4.R5 (each refinement an obligation); no decision otherwise. |
| A29 | run.py 887-897 | 3 | Surplus arguments cross untyped; a reading of the code with no clause behind it. | No decision; a fix. |
| A30 | run.py 899-924, 1040-1065 | 5 (otherwise 1 with B20) | Asks for a `Crossing`-like theory with laws for the array and table conventions, so the bridge is keyed on declared types and not on labels. | 3.S24 and 11.S6, which the code cites for the label-based recognition. |
| A31 | run.py 434-440 | 1 (with B21) | Both find `HostRecord` fields shadowed by `dict` methods. | No decision; a fix. |
| A32 | run.py 857-861, 873-876 | 3 | A function crossed bare skips the declared codomain check; no clause behind it. | No decision; a fix or a docstring. |
| A33 | run.py 1529, 1410 | 2, L5.19 | L5.19 (the default is a declared argument recorded with the call) and L5.18 (no policy constants in code) produce the finding that the default `"Sampled"` is a module constant. | No decision; where the default is declared. |
| A34 | run.py 1541-1546, 1559, 1566 | 3 | `surface` is keyed by plain name and the cone by `name@file`; found by reading the code. | No decision; a fix. |
| A35 | run.py 1548-1549 | 2, L10.4 | L10.4 (a certificate is identified by a hash over its dependency cone) makes a hash that moves with the name of an unrelated law a defect. | No decision; a fix and a test. |
| A36 | run.py 1574-1579 | 3 | The four state counts are always zero; found by reading the code. | 12.S18 (the counts of states) and 10.S10 (`--require-certified`). |
| A37 | host.py 33-45 | 1 (with B12) | Both find `text_of_bytes` is not injective and rewrites newlines. | No decision recorded; L8.9 and 10.S9 (hash of what was read) are the nearest. |
| A38 | host.py 14-16, 47-50, 66-68, 87-90 | 1 (with B14) | Both find the module-global buffer and counts, and the loss of output on failure. | No decision; a design change in `host.py`. |
| A39 | host.py 71-84, 93-99 | 1 (with B13) | Both find that `PermissionError` and other `OSError`s escape as Python exceptions. | No decision; a fix. |
| A40 | tests/run/callbacks.lut 3-7 | 1 (with B27) | Both find `maximize` returns a minimiser. | No decision; a rename. |
| A41 | callbacks.lut 6, record_of_functions.lut 7, host_function.lut 6, hello.lut | 1 (with B29) | Both find `showFloat` repeated in the fixtures over `repr`; both also ask for a round-trip law in a library theory outside world.lth. | No decision; a library addition. |
| A42 | tests/run/observe.lut 9-13 | 1 (with B15) | Both find the program depends on the process's working directory; A adds the message and names. | No decision; a fixture fix. |
| B1 | world.lth 59 | 1 (with A2) | The alias covers only the shape without arguments; same as A2. | As A2. |
| B2 | world.lth 73-77, 95; world_model.lut 26-31 | 1 (with A16) | `Described` is never built for `print` or `readFile`, so §5 cannot run; this is the second half of A16 (models, not a law). | No decision; adds models. |
| B3 | world.lth 61-65, 222-226 | 5 (otherwise 1 with A5) | Same as A5: observe undeclared places, or state the host side as assumed. | As A5. |
| B4 | world.lth 81-83 | 5 (otherwise 1 with A7) | Same as A7; adds that `own` concerns the store while `S` holds only stdout and files. | As A7. |
| B5 | world.lth 101-109, index §2 | 4 | `Persistence` has no model, no `Assumes` and no `writeFile` action, so the persistence hypothesis of 10.S13 is not in any certificate; touches the same laws as A10 from another side. | 10.S13 (and 10.S2 for `writeFile`). |
| B6 | world.lth 133-136 | 1 (with A14) | Same as A14: `settled` ignores the demand's cutoff. | As A14. |
| B7 | world.lth 134-139; run.py 1582-1593 | 1 (with A15) | Same as A15; B adds that the law should say for which command it holds. | As A15. |
| B8 | world.lth 118, 142-143 | 5 (otherwise 1 with A18) | Same as A18 (route in the identity, determinism); also the unused `hash`, shared with A12. | As A18. |
| B9 | world.lth 161-177 | 5 (otherwise 1 with A20) | Asks a law over two fields (calling `a` leaves `b`'s count unchanged) and one for a curried callback. | D-2026-10-14-a, 12.S18. |
| B10 | world_model.lut 21, 29; host.py 43-45, 93-99 | 1 (with A11) | `"stdout"` is one name for two places; same finding as A11. | As A11. |
| B11 | world_model.lut 15-17; host.py 77-83 | 1 (with A4) | Structural `==` on a list of pairs tells apart states that read the same; A4 asks the equality law, B proposes sorting or a map. | As A4. |
| B12 | host.py 33-40 | 1 (with A37) | Same as A37; B adds the hash over raw bytes before decoding. | As A37. |
| B13 | host.py 80-84, 95-98 | 1 (with A39) | Same as A39; B adds a result type that can say "unreadable". | As A39 (the result type would change `readFile`'s declared type, no recorded decision). |
| B14 | host.py 14-15, 47-50, 87-90 | 1 (with A38) | Same as A38; B adds that a long fit shows no progress. | As A38. |
| B15 | host.py 43-45, 80-81; run.py 1575-1579 | 1 (with A42) | Same cwd dependence as A42; B adds that the path and hash of bytes read are not in the run's record. | The record of a run (12.S18) for the second part; none for the first. |
| B16 | run.py 788-789 | 1 (with A27) | Same as A27. | As A27. |
| B17 | run.py 746-752, 971-977, 1036 | 1 (with A26) | Same as A26; B adds `uint64` arrays. | As A26. |
| B18 | run.py 964-965, 1010 | 1 (with A24) | Same as A24. | As A24. |
| B19 | run.py 983-1010 | 1 (with A28) | Same as A28; B adds the bare value for `Maybe` and the uneven checks. | As A28. |
| B20 | run.py 913-923 | 1 (with A30) | Same finding as A30 (recognition by field names), asking to cross by declared type without a law. | As A30. |
| B21 | run.py 433-439 | 1 (with A31) | Same as A31. | As A31. |
| B22 | run.py 828-847 | 5 (otherwise 1 with A22) | Same as A22; B adds counting after the arguments cross and recording the failure. | As A22. |
| B23 | run.py 878-885 | 1 (with A21) | Counts of two closures of one factory merge under one name; same family as A21. | As A21. |
| B24 | run.py 780-783, 795-826 | 1 (with A23) | Same as A23; B proposes a threshold parameter. | As A23. |
| B25 | run.py 1544-1546, 1574-1579; world.lth 125-126, 217 | 5 (otherwise 1 with A16) | `Host` has no law, so `hello.lut` demands no certificate; asks `agreement` as the law of `Host`. | As A16. |
| B26 | run.py 1563 | 4 | `--set` values reach laws by parameter name, so equal names collide; no counterpart in A. | No decision; a fix in the demand's mapping. |
| B27 | tests/run/callbacks.lut 1-7 | 1 (with A40) | Same as A40. | As A40. |
| B28 | world_model.lut 26-40; world.lth 187, 217 | 4 | `Console`, `HostConsole` and `readFile` name two things each; no counterpart in A. | No decision; a rename. |
| B29 | tests/run/host_function.lut, callbacks.lut, record_of_functions.lut | 1 (with A41) | Same as A41; B adds that the cone hash omits `builtins`. | As A41. |
| B30 | world.lth 30-32 | 1 (with A17) | Same as the second half of A17. | As A17. |

Counts by class (both reports, items): class 1: 39, class 2: 6, class 3: 7, class 4: 3, class 5: 17.
Counts in A (42 items): class 1: 18, class 2: 6, class 3: 7, class 4: 0, class 5: 11.
Counts in B (30 items): class 1: 21, class 2: 0, class 3: 0, class 4: 3, class 5: 6.
