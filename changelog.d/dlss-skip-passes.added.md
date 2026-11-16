- Experimental `EDEN_NX2_DLSS_SKIP_PASSES` (ports of zortos293/Lichii#864 and #1985): a game's own
  DLSS network passes are skipped while a replacement upscale draws over their output (`drew`) or
  while the network cannot be shown (`blocked`). Off by default; upstream measured The Duskbloods
  on a Steam Deck at 56.6 to 40.4 ms of GPU time a frame.
