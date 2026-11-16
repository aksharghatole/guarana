- Four frame pacing experiments that measured no gain, or worse, are removed with their code:
  `EDEN_NX2_QUEUE_LIMIT`, `EDEN_NX2_FLUID_OFFSET_US`, `EDEN_NX2_FLUID_SPLIT_SUBMIT` and
  `EDEN_NX2_FLUID_HOST_WAIT_US`. Setting one now changes nothing; the presenter keeps the defaults
  they replaced. Their measurements are in
  [docs/switches.md](docs/switches.md#removed-experiments).
