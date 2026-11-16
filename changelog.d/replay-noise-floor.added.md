- GPU trace bench: on a driver that does not replay bit for bit (Intel's Windows driver), the
  baseline's own run-to-run difference becomes a noise floor, and a variant within it is reported
  as within noise instead of failing the comparison (`trace_replay.py bench --noise-margin`).
