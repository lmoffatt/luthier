# record/runs/

Runs of Luthier programs whose outputs are kept, one directory per series, each with its own
README saying the command, the commit and what the run is not.

Each `luthier run` that succeeds appends an entry to `x.run.json` beside `x.lut` (12.S18; the
file is ignored by git, as `*.cert.json` is, so a run's record is copied into the directory of
its series when it is kept). An entry has: `entry` (the name run), `time` (UTC), `parameters` (the
`--set` values), `output` (standard output), `calls` (the calls the host made back into Luthier,
by route and argument position), `fuel` (`given` and `spent`), `files_read` (a list of
`[path, sha256 of its bytes]` for each file `host.observe` or `read_file` read), `lock` (the
`luthier.lock` found beside the program or one directory above: its `path`, the revision it
`pinned`, and `status`: `matches`, `differs` (a warning was printed; the run went on) or `written`
when none was found and the run pinned the current revision), and `certification`: `cone` (hash
of the entry's cone with its hosts and the interpreter), `fingerprint` (the hash of the cone's
canonical code alone, so two entries with the same fingerprint ran the same code), `interpreter`
(the revision, as `certify` reads it), `python` (its version), `hosts` (each host route of the
cone with the version or file hash `certify.host_hash` gives it, numpy and matplotlib among
them), `accept` (the weakest grade accepted), `states` (the counts of states of the cone's
names), `laws` and `not certified` (empty: a run starts only on a certified cone, 12.S17).
