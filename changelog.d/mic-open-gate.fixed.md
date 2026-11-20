- Audio: while Windows' microphone prompt is unanswered, capture streams wait for the one open
  already waiting instead of starting one each, and the SDL backend opens the microphone on the
  calling thread again, so a stuck open cannot hold SDL's next playback open
  ([#199](https://github.com/karimalsalah/guarana/issues/199)).
