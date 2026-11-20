- Add-Ons: the page says whether each built-in patch is made for the installed version of the
  game before the game has ever been started. It reads the build id of the game's main program
  from the version that would start (the enabled update and mods included) without loading it.
  A built-in made for another version gets the warning sign and "Cannot be applied: it is made
  for another version of the game", ticked or not; one made for this version says so until the
  first start tells whether it was applied. The other reasons (a mod changes the same part of the
  game, the game's code is not what it expects) still come from the last start. The loader call
  is `AppLoader::ReadMainBuildId`, ported from Lichii #1358.
