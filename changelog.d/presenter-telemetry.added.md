- Presenter telemetry for pacing A/Bs ([#8](https://github.com/karimalsalah/guarana/issues/8)):
  a `Present setup` line at each swapchain creation names the window's display and its refresh
  rate, the present mode and image count, `EDEN_NX2_FLUID` and Windows' hardware-accelerated GPU
  scheduling; `EDEN_NX2_SHOWN_STATS` also counts the intervals between presents in refreshes
  (under one, one, two, three or more) and the refreshes missed against the median; the
  diagnostic `EDEN_NX2_PRESENT_MODE=immediate|fifo|fifo_relaxed|mailbox` asks for one present
  mode, falling back with a warning when the surface lacks it; and
  `tools/bench/suites/presenter-ab.json` runs FIFO against IMMEDIATE with frame generation off
  and on.
