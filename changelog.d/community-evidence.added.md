- Device reports: each report gets the engine's GPU family (Arrow Lake-H, Lunar Lake, Radeon 780M,
  Steam Deck LCD and the others) when it names its GPU exactly, and the new
  `site/data/community-evidence.json` counts reports and devices per family, game and build, with
  the effects that paired `tools/bench` rows measured. Nothing reads it to change a default yet
  ([#24](https://github.com/karimalsalah/guarana/issues/24)).
