# Handover

The living handover for any agent or person who takes over Guarana or works alongside it. It says
where things stand, how to pick up each lane, and how a change is measured. The rules are in
[AGENTS.md](AGENTS.md), and how an agent finds and claims work is in
[docs/agents/README.md](docs/agents/README.md).

**Last checked: 2026-11-16, 00:40 UTC**, from branch `chore/release-v20.4.0`. "Observed" below means
what `git` and `gh` showed at that time. Anything this file could not confirm is marked
**(unsure)**. If you change the state of a lane, update its row in the same pull request.

## Where things stand

- **`main` is v20.4.0.** It holds v20.3.0 plus:
  - the merge of zortos293/Lichii `nx2` up to `99e89096cb` (67 commits, pull request #197; the
    resolutions are listed there);
  - six fixes ported from open upstream pull requests and Eglantine, the replay bench
    (`tools/nx2/trace_replay.py bench`) and the driver verdict at boot (pull request #198).

  The details are in [CHANGELOG.md](CHANGELOG.md).
- **The `upstream` mirror is at `99e89096cb`.** It was pushed by hand, because an upstream commit
  changes a workflow file ([docs/LANES.md](docs/LANES.md), "When the sync stops"). The scheduled
  sync continues from there and will need the same push the next time upstream touches a workflow,
  unless `UPSTREAM_SYNC_TOKEN` is set.
- **What the merge changed for our own code**, for whoever merges upstream next:
  - Upstream routes each global memory access among its own candidate buffers. `EDEN_NX2_GM` bits
    2 and 4 sit on top: a load takes its narrowed list when it has one, its route otherwise.
  - Upstream's pass trace took the names of our per-pass GPU cost timing, which is now
    `cost_pass_*`, `CostPass` and `ReportCostPassTimes` in `vk_scheduler`.
  - A lookup drops a prebuilt pipeline that is still queued and the draw builds it; the async
    boot counts such a build as ended.
- **Open pull requests:** #195 (the Hall of fame, from the `legacy` workflow).
- **Known problems found on 16 November:**
  - #199: a host microphone open that never returns leaves the game without a first frame (one
    boot in six on the measurement machine; the code path is older than the merge).
  - The replay bench has no real rows yet: `guarana-cli --replay` now starts on Intel's Windows
    driver, but the Hyrule Field trace recorded for it replays no frames. Whether the recording or
    the replay drops the presents is not known.
  - The warm shown-frame pacing of v20.4.0 against v20.3.0 was not measured: another process was
    compiling on the measurement machine. The first-run numbers are in #197.
- **The work queue:** the open `agent-ready` issues
  ([the list](https://github.com/karimalsalah/guarana/issues?q=is%3Aissue%20is%3Aopen%20label%3Aagent-ready%20-label%3Aneeds-triage%20no%3Aassignee)).

## Candidates from the 16 November survey

Read from the open pull requests of zortos293/Lichii, Eglantine's branches and about 480 forks with
commits of their own. None of these is measured on an integrated GPU; each needs a paired run before
it becomes a default.

| Candidate | What it is | State |
|---|---|---|
| `EDEN_NX2_OOT_BYPASS_SKIP=d9ee412f00ce399a` | Also skip the network's heavy dispatch while the output pass is bypassed (raphaeltorquat0/Lichii `c91d646a52`) | The switch exists: an A/B needs no code |
| zortos293/Lichii#1903 | Host-visible buffer cache on integrated GPUs (15 to 25 fps on Adreno 830) | Read only; touches the buffer cache |
| zortos293/Lichii#1897, #1810, #1797, #1816 | Collector waits once per pass; semaphore acquires without a drain; ASTC decode image reuse | Behind a switch, then A/B |
| zortos293/Lichii#1832 | Marks routed stores' buffers written | Wait: it runs after `EDEN_NX2_GM` has built its narrowed lists from the read-only buffers |
| zortos293/Lichii#1874 | Formatless image loads on Vulkan 1.3 | No effect on Intel 32.0.101.9175, which reports the feature; no evidence yet where it changes something |
| Eglantine `662af0bfaf` (part) | `Scheduler::WaitSubmitted` woken by a counter instead of 50 us sleeps | Behind a switch, then A/B |
| Eglantine `d1195b7d49` | Translated stages reused across pipelines that differ only in fixed state | Second wave: it sits in the shader cache |
| Deathnetworks/Lichii `059e931f66` | Retry a failed graphics pipeline build on a later draw | Needs a thread-safe counter |

## Lanes in progress

No lane is open on the public repository. To start one:

1. `git fetch origin`, then `git worktree add ../wt-<lane> -b <branch> origin/main`. Use one
   worktree per lane.
2. Keep the pull request in draft until it is compiled and, for a performance change, measured.
3. Update this file's rows in the same pull request.

## How a change is measured

The full rules are in [docs/BENCHMARKING.md](docs/BENCHMARKING.md) and
[tools/bench/README.md](tools/bench/README.md).

- **Use a verified scene.** A `tools/bench` row counts only with `"valid": true` and
  `"scene_ok": true`: the benchmark checked the scene against a reference screenshot. The scene of
  record is Ocarina of Time, Hyrule Field (`tools/bench/scenes/oot-hyrule-field.json`).
- **Measure in pairs.** Run the baseline and the change back to back, in one session, on the same
  machine, plugged in:
  `python -I tools/bench/bench.py run ... --variant tools/bench/variants/baseline.json --variant <yours>.json`.
  Then run `bench.py compare` on the two result files.
- **Report every number.** Put the device, driver, power mode, the before and after numbers and
  the number of paired runs in the pull request's table and in the switch's row in
  [docs/switches.md](docs/switches.md). Report losses too.
- **The measurement machine** for the published numbers is one laptop: Core Ultra 9 285H, Arc 140T,
  Intel driver 32.0.101.9175. Builds, benchmarks or the emulator never start on it unless the owner
  asks, because a compile spoils a run.
- **Live readings are not results.** Use the debug server (`frame_times`, `gpu_costs`) to find a
  cause; only bench rows prove a gain.

## Where things are

| What | Where |
|---|---|
| Rules, repository map, build and test commands | [AGENTS.md](AGENTS.md) |
| Finding work, `/claim`, CI gates, optional agents, MCP registry steps | [docs/agents/README.md](docs/agents/README.md) |
| Which agents to court and what each needs from the owner | [docs/agents/RESEARCH-2026-11.md](docs/agents/RESEARCH-2026-11.md) |
| Lanes, releases, hotfixes, repository settings | [docs/LANES.md](docs/LANES.md) |
| Every `EDEN_NX2_*` switch, its status and measured effect | [docs/switches.md](docs/switches.md) |
| Benchmark harness and evidence rules | [tools/bench/README.md](tools/bench/README.md), [docs/BENCHMARKING.md](docs/BENCHMARKING.md) |
| Debug MCP server: methods and etiquette | [docs/nx2/debug-mcp.md](docs/nx2/debug-mcp.md), `tools/nx2/debug_mcp.py`, [.mcp.json](.mcp.json) |
| Frame generation and pacing | [docs/frame-generation.md](docs/frame-generation.md) |
| Reports, issues, test builds and how they connect | [docs/FEEDBACK.md](docs/FEEDBACK.md) |
| Plans | [ROADMAP.md](ROADMAP.md) |
| AI rules: disclosure, ownership, spam | [docs/AI_POLICY.md](docs/AI_POLICY.md) |
| Claude Code skills (bench, debug-server, perf-change, release, upstream-port) | `.claude/skills/` |

## If you are an agent starting now: do these five things first

1. **Read [AGENTS.md](AGENTS.md)**, then this file and [docs/agents/README.md](docs/agents/README.md).
2. **See what moved since this file was written:** `git fetch origin`,
   `gh pr list -R karimalsalah/guarana` and `gh run list -R karimalsalah/guarana --limit 10`. If
   this file is stale, fixing it is your first commit.
3. **Take exactly one thing:** a lane above, or an `agent-ready` issue that you `/claim`. Work in
   your own worktree, on a branch that carries the issue number.
4. **Run the Python tests** before and after your change (section 4 of
   [docs/agents/README.md](docs/agents/README.md)). Never start a build, a benchmark or the
   emulator on the owner's machine unless asked.
5. **Open a draft pull request** with the template filled in, an `Assisted-by:` trailer on each
   commit, a changelog fragment (`changelog.d/`), and your lane's row here updated.

## Not confirmed when this was written

- Whether the v20.4.0 release run published every platform's files: check with
  `gh run list -R karimalsalah/guarana --workflow release-binaries.yml`.
- The three known problems above.
