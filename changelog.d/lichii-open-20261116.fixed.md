- Ocarina of Time: the 3D view no longer comes out white or in false colours after a load.
  A stream buffer wrap that was refused kept the start position, so the next uploads were
  written over bytes the GPU had not read yet (Lichii #1835).
- Resolution scaling: images are not scaled past the device's 2D image and framebuffer limits.
  Ocarina of Time's sun shadow map at 1.5x and 2x went over 16384 and lost the device on AMD
  (Lichii #1890).
- Texture cache: the retention limit follows the lowest driver budget read lately, so a budget
  that Windows moves down and up no longer takes the process over it every few seconds
  (Lichii #1860).
- Memory: native compute launches clear the pending upload list, which grew for the whole
  session in Ocarina of Time, 768 MiB after 90 minutes (Lichii #1908).
- Moving the window during play no longer aborts with VK_INCOMPLETE: the swapchain image,
  surface format and present mode queries are repeated (Eglantine c40fca7da4).
- Status bar: "Building: N shader(s)" returns to zero when a compute pipeline is dropped before
  its build ran (Lichii #1799).
