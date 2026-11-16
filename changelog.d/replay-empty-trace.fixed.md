- GPU traces: `guarana-cli --replay` refuses a trace that holds no presents (`the trace has no
  frame to replay`, exit status 1) instead of writing an empty `frames.json` and exiting 0. The
  recorder logs an error and sets `last_error` when a recording ends before its first present,
  which closing the game during the snapshot does, and logs a warning when it ends short of the
  presents asked for. `trace_status` gains `last_presents`. `trace_replay.py check` runs corpus
  entries the replay must refuse (`expect_failure`), and CI replays the sample trace written
  without its presents (`--gpu-trace-sample <trace> --no-presents`).
