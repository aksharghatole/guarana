- Upstream: merged zortos293/Lichii `nx2` from `99e89096cb` to `7c7f723b68` (50 commits).
  Among them: Nextendo online play no longer needs a special build and follows Configure >
  Network, still off by default (Lichii #1979); with it on, a game's signed NPLN patch is checked
  before boot ("Checking online patches") and applied after mods (Lichii #1358), with Nextendo's
  network rules and signed game catalogue (Lichii #1984) and Splatoon 3's network requests
  (Lichii #1988). Ocarina of Time's No sharpening copies the image the output pass samples, which
  ends a frozen 3D under a live HUD (Lichii #1875), and skips the unused heavy dispatch while the
  output is replaced (Lichii #1941). A lost Vulkan device ends the process with a log line instead
  of an unhandled exception (Lichii #1938); a buffer without memory frees staging memory and
  retries (Lichii #1963, #1931); padded depth targets are drawn as the square they are (Lichii
  #1868); terminated threads and a stopped game's kernel objects close safely (Lichii #1957,
  #1932); and bounds fixes in the NSO, KIP, NPDM, NCZ, ticket and XTS readers. Help > Check for
  Updates stays hidden in our releases, which are built without the update checker. With
  `EDEN_NX2_OOT_BYPASS_ANY` the
  bypass still copies the tonemap the rasterizer tracks ([docs/switches.md](docs/switches.md)).
