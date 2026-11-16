- Benchmark: boot suites. `tools/bench/suites/console-boot.json` measures launch to gameplay and
  first-visit hitches in one command, every boot and shader switch against the baseline with a
  cold, a second and a warm shader cache (and the GPU driver's cache with `--driver-cache-dir`),
  three times; each row has the boot phases, the held draws and builds to the scene and the
  stutter frames, and is invalid when its cache was not in the state it claims
  ([docs/console-boot.md](docs/console-boot.md)).
