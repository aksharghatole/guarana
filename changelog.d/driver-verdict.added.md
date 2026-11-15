- Drivers: at boot the engine compares the graphics driver's version with the versions it
  knows something about and logs the result after the `Device profile:` line. Known today:
  NVIDIA's driver before 580.119.02 and Mesa RADV before 26.2.5, which the renderer works
  around (the window names such a driver once per run), and Intel's Windows driver before
  32.0.101.9175 on the Core Ultra and Arc B-series integrated families, the driver the Intel
  numbers were measured on (logged only). Every other driver gets no verdict
  (`Common::AssessDriver`, `docs/DEVICES.md`).
