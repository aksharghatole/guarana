- `EDEN_NX2_ASYNC_GUARD` (experimental, off): with asynchronous shaders, draws that write memory,
  use transform feedback, rasterize nothing or render into a small target wait for their pipeline
  instead of being skipped, so effects later draws depend on are not lost until a restart. From
  Eden ([6a767ac43a](https://git.eden-emu.dev/eden-emu/eden/commit/6a767ac43a089fe988526bf7f8477ccc43277fb1)).
