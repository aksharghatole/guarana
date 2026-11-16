- `EDEN_NX2_LOAD_SAVE=1` (experimental, off by default): on Intel's Windows driver the boot load
  saves the driver pipeline cache once its builds have ended and starts the background prebuild
  after it, so a crash or kill later in the session no longer loses that boot's driver builds
  (port of [Lichii #1838](https://github.com/zortos293/Lichii/pull/1838); step B6 of
  [docs/console-boot.md](docs/console-boot.md)).
