- The game network suites now log each tensor program's path (`EDEN_NX2_TENSOR_LOG` in
  `game-network.json` too) and say which GPUs their matrix arms apply to: the Arc 140T's driver lists
  only 8x8x16 shapes with fp32 accumulators and 8x8x32 8-bit shapes, so `EDEN_NX2_INTEL_COOP_MATRIX`
  and the A1 switches do nothing there (they apply to Xe2 and RDNA 3). The design gains step A1b, an
  8x8x16 path for the 140T, and says to read only each suite's second pass (every arm compiles cold).
