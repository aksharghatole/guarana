- `EDEN_NX2_ASYNC_DISCARD=2` (experimental, off): with asynchronous shaders, a native draw whose
  pipeline is still building is skipped only when it draws into render targets the game clears
  and redraws every frame, and waits otherwise, so title text, chat bubbles and lighting drawn
  once are not lost on an empty shader cache. Ported from Fritchii (`a962f20533`).
