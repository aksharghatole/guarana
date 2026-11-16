- Experimental switches for the game's own tensor networks on matrix units that go through shared
  memory (AMD's 16x16x16, Intel's 8x16x16): `EDEN_NX2_HMMA_ZERO_C` starts an HMMA whose accumulator
  is zero from a zero matrix instead of a stored C tile (bit-exact), and `EDEN_NX2_HMMA_K16_ONCE`
  runs a K=16 HMMA as one 8x16x16 product per row half, rounding once. The diagnostic
  `EDEN_NX2_TENSOR_LOG` logs each tensor program's HMMA counts and the path they take, and
  `tools/bench/suites/game-network-a1.json` measures the two switches on Ocarina of Time. All off by
  default and not measured yet.
