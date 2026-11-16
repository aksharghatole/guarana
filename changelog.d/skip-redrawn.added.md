- `EDEN_NX2_SKIP_REDRAWN=1` (experimental, off by default): with asynchronous shaders on, a Switch 2
  draw into a target the game redraws every frame is skipped while its pipeline builds instead of
  stopping the frame (port of [Eglantine #874](https://github.com/Eglantine-Community/Eglantine/pull/874);
  step F4 of [docs/console-boot.md](docs/console-boot.md)).
