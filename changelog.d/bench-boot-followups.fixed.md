- Benchmark boot suites: a second run on a driver that keeps its own pipeline cache (NVIDIA, AMD)
  is no longer marked invalid for a driver cache its cold run never saves, and the caches of cold
  runs that no second run copies are deleted at once instead of filling the work folder; the
  README says to record the reference with `bench.py run` and to smoke-test with two runs first.
