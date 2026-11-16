- Linux and macOS: Guarana installs and announces itself as `io.github.karimalsalah.guarana`
  instead of upstream Lichii's `io.github.zortos293.lichii`: the desktop entry, AppStream metadata,
  MIME package and icon, the Wayland app id, the About dialog's theme icon and the macOS bundle id.
  A Guarana package and a Lichii package no longer install the same files or share one app id
  ([#107](https://github.com/karimalsalah/guarana/issues/107)).
- Built-in console news shows Guarana's own GitHub releases, credited to Guarana with an "Open
  GitHub" link, instead of Lichii's releases labelled as Eden news. The update checker keeps its
  source ([#107](https://github.com/karimalsalah/guarana/issues/107)).
