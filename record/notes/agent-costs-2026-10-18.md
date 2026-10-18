# What a task costs on each agent we can run, measured 2026-10-18

Why: on 2026-10-18 the Anthropic weekly quota stood at 82% used with 3 days left (Luciano's screen:
90% of the usage at more than 150k tokens of context, 80% from general-purpose subagents). Antigravity
and Codex run on other quotas; this note measures what one task costs on each, so work can be routed
while a quota is low. Measured by the coordinating session, one run per model, one at a time, with
Luciano reading each quota before and after.

## The task

One small task with a known reference: insert clause L9.17 into `record/principles-language.md` and
regenerate `docs/principles.md` (brief `record/plan/core-2026-10-17/prompt-budget-law.md`). The
reference is the Claude Code subagent (Sonnet) that did it for real in commit 50aba5b. Each run worked
in a detached git worktree at 24ebd40 (the commit before the clause), told not to commit; the worktree
was reset between runs, and each result was compared with 50aba5b's clause.

## Results

| Runner and model | Time | Fresh tokens | Cached tokens | Output | Quota used | Result |
|---|---|---|---|---|---|---|
| Claude Code subagent, Sonnet | 21 s | 40,624 (total) | not reported | not reported | not measured | exact (reference) |
| Antigravity, Gemini 4 Argon high | 354 s | 101,195 | 639,465 | 10,794 (+4,607 thinking) | 2% of Argon's own weekly bucket | exact |
| Antigravity, Claude Sonnet 5.5 medium | 98 s | 26,155 | 118,959 | 3,253 | 2% weekly, 4% of 5 h (Claude and GPT bucket) | text exact, continuation lines indented one space too many |
| Antigravity, Claude Opus 5.5 medium | 99 s | 34,314 | 178,265 | 3,825 | 5% weekly, 10% of 5 h (Claude and GPT bucket) | exact |
| Antigravity, Gemini 3.8 Flash medium | 183 s, failed | 40,569 | 0 | 798 | 2% weekly, 2% of 5 h (Gemini bucket) | failed: "User location is not supported" (a VPN) |
| Codex, gpt-6.1-sol, reasoning low | 87 s | 12,524 (147,308 input, 134,784 cached) | 134,784 | 848 | about 1% weekly, 4% of 5 h | exact |

A larger read-only task (re-running the spec debt inventory of record/IA/code-follows-2026-10-16/
prompt-debt.md, which a Sonnet subagent finished with 205k tokens in 7.5 min) was stopped on Argon high
after 632 s: 114,638 fresh tokens and 1,121,202 cached, 4% of Argon's weekly bucket, no report.

Read as weekly capacity, at these rates: Codex about 100 small tasks; Sonnet in Antigravity about 50;
Opus in Antigravity about 20; Argon about 50 small or 25 large, from its own bucket. A core bite is
roughly ten times the small task (bite 4's Opus subagent used about 570k tokens).

## How to run each (headless)

- Antigravity: `agy -p "<prompt>" --model <id> --output-format json --print-timeout 880s`, run in the
  target directory; the JSON carries `usage`. Tools need `--dangerously-skip-permissions` (authorized
  by Luciano on 2026-10-18, one bite at a time, never beside a Claude agent writing) or allow-rules in
  `~/.gemini/antigravity-cli/settings.json`. Model ids: `agy models` (gemini-4-argon-{low,medium,high},
  gemini-3.8-flash-*, claude-opus-5-5-*, claude-sonnet-5-5-*, gpt-oss-120b-medium). Quota: the model
  menu's "View Usage" in the Antigravity app.
- Codex: the binary bundled with the VS Code extension,
  `~/.vscode/extensions/openai.chatgpt-<version>/bin/linux-x86_64/codex exec --json -s workspace-write
  -C <dir> "<prompt>" < /dev/null`; the last event `turn.completed` carries `usage`. The global CLI
  (`codex`, 0.57) is too old: with a ChatGPT account it refuses every model. The model is the one in
  `~/.codex/config.toml` (`gpt-6.1-sol`, effort low). Quota: `/status` in the Codex panel.

## Caveats

- Gemini models fail behind a VPN ("User location is not supported for the API use"), and the failed
  call is still charged; Claude and GPT models through Antigravity work behind it.
- One run per model: the quotas are read as whole percentages, so a small task's cost is known to about
  one percentage point.
- Argon reads much more context than the others for the same task and takes four times as long; its
  place is theory and design, where its level (Fable's) matters, not mechanical edits.

## Routing while the Anthropic quota is low (coordinator's proposal, 2026-10-18)

Code bites of the core to Codex, one at a time, in the repository, the coordinator reviewing the diff
and running the suite on the machine (no quota). Theory bites (the core's bite 6, the structures) to
Argon when off the VPN. Claude only coordinates, in short turns.
