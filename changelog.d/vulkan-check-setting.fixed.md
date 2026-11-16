- The Debug setting "Perform Vulkan check" turns the startup Vulkan check off again: it was read
  before the settings were loaded, so the check always ran.
