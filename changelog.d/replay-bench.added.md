- Tools: `tools/nx2/trace_replay.py bench` runs a paired A/B on a recorded GPU trace: each
  variant (switches, a build, or both) replays the same frames in turn, and the report says
  whether its frames are the baseline's bit for bit and what a frame cost to replay. No game,
  save or reference screenshot is needed, so the scene cannot be the wrong one
  (`docs/nx2/gpu-trace.md`). `guarana-cli --replay` gains `--no-images` and writes `replay_ms`
  per frame, the frame's own cost without the PNG encoding of the one before it.
