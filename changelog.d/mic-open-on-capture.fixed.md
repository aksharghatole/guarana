- Audio: a Switch 2 game opens the host microphone only when it starts capturing, and no
  game thread waits for that open. On Windows the first start from a new folder (so after every
  launcher update) asks for microphone access, and Ocarina of Time waited on that prompt before
  its first frame, though it never captures
  ([#199](https://github.com/karimalsalah/guarana/issues/199)).
