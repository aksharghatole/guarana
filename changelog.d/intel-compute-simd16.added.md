- `EDEN_NX2_INTEL_COMPUTE_SIMD16` (experimental, off): on Intel GPUs, compute shaders without warp
  operations can be built at 16 lanes, which built Ocarina of Time's large global-memory programs
  about 2.6 times faster on an Arc B580 at the cost of some frame rate. From Fritchii-Intel-Fixes
  (patch 0011).
