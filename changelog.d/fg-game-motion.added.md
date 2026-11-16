- Experimental `EDEN_NX2_FG_GAME_MOTION`: with `EDEN_NX2_FLUID_INTERP`, in-between frames are
  warped from the game's motion (Ocarina of Time's motion guide: the camera from the scene depth,
  and Link) instead of optical flow, and what one real frame no longer shows is filled from the
  other by depth. Off by default and not measured yet; `tools/bench/suites/game-motion-fg.json`
  measures it against the optical-flow interpolation the game ships with at 120 Hz.
