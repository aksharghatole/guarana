- Design for the game's own reconstruction network and motion on integrated GPUs
  (`docs/design/game-reconstruction-and-motion.md`), and the bench suite of its first step:
  `tools/bench/suites/game-network.json` measures Ocarina of Time's anti-aliasing network with
  each existing way of running its tensor instructions (software, the shared-memory gather,
  Intel's 8x16x16 cooperative matrices), with the game presets off so the network actually runs.
