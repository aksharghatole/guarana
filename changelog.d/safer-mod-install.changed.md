- Add-Ons: importing a mod asks before it replaces a mod of the same name, which it did without
  a word. The new mod is copied completely before the installed one goes, so a copy that fails
  leaves the installed mod as it was. Importing from a folder no longer renames that folder, or
  deletes a folder next to it that has the name chosen for the mod.
- Add-Ons: each imported mod gets a `mod.json` with its name, the zip or folder it was imported
  from and the date, shown under the list when the mod is selected. The game never reads the
  file, and a mod that brings a `mod.json` of its own keeps it.
- Add-Ons: an "Open Mods Folder" button opens the game's mod folder, and makes it for a game
  that has no mods yet.
- Add-Ons: a warning under the list names the game files that more than one ticked mod replaces
  and the mod whose file the game gets, which is the first one in name order.
