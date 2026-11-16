- Experimental `EDEN_NX2_INTEL_COOP_MATRIX_8X8`: the game's tensor networks on the Arc 140T's own
  cooperative matrices (8x8x16 with fp32 accumulators, the only fp16 shape its driver lists), two
  products per guest HMMA through shared memory, rounded to fp16 once. Off by default, not measured
  and not yet run on the hardware; `tools/bench/suites/game-network-a1b.json` measures it.
