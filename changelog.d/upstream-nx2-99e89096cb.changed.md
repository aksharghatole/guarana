- Upstream: merged zortos293/Lichii `nx2` from `642eace1b7` to `99e89096cb` (67 commits).
  Among them: Loading Shaders waits only for the pipelines the last two sessions used and
  builds older ones in the background (Lichii #1803); generated-frame spacing counts from the
  deadline, which ends Ocarina of Time locking at 11 to 17 game fps at 240 Hz with 4x frame
  generation (Lichii #1779); images newer ones overwrote are collected at the collector's own
  age, which ends the 16 GB growth in Ocarina of Time's Skulltula House (Lichii #1845); global
  memory accesses are routed among their own candidate buffers (Lichii #1807, #1848, #1853);
  large ASTC arrays decode in batches on integrated GPUs (Lichii #1823); a staging buffer
  without memory degrades instead of aborting (Lichii #1870); Ocarina of Time's upscale passes
  are recognised by native program key, so a lowering change no longer turns FSR and DLSS off
  (Lichii #1871); Mario Kart World keeps GPU tick timestamps (Lichii #1817); SDL gyro survives
  a controller reconnect (Lichii #1805); and bounds fixes in the NCZ, KIP, NPDM, IPSwitch and
  cheat parsers.
- `EDEN_NX2_GM`: narrowed and rebased loads (bits 2 and 4) now sit on top of upstream's
  per-access routes: a load takes its narrowed list when it has one and its route otherwise.
  Buffer base hoisting (bit 1) applies to both.
- Frame trace: Guarana's per-pass GPU cost timing (`DKB gpu_pass renderer_frame=...`, the
  debug server's `gpu_costs`) runs next to upstream's new pass trace (`DKB gpu_passes`, one
  `DKB gpu_pass <ms>` line per pass); `tools/bench` reads the summary line only.
- Shader cache: the log line and marker that count the pipelines admitted for the background
  prebuild report the planned count again; it had read 0 since the v20.3 merge, which also
  kept the "Background prebuild done" line from being logged.
