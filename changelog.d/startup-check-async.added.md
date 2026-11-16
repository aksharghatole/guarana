- `EDEN_NX2_STARTUP_CHECK_ASYNC=1` (experimental, off by default): the startup Vulkan check's child
  process runs while the frontend starts, and the frontend waits for its verdict only before it
  first uses Vulkan (step B2 of [docs/console-boot.md](docs/console-boot.md)).
