- Tests: the built-in patch tests fail when two built-in patches that can be applied together
  write, check or keep their state in the same bytes of a game's module: code caves, hooks and
  state blocks. A patch and the one it replaces, and the alternatives of one group, may share
  bytes, because only one of them is applied. The table is read through
  `FileSys::BuiltinPatchRanges`.
