- Device reports name the GPU's PCI ID: `tools/bench` rows record it (`hardware.gpus[].pci`, from
  Windows' PNP device ID or `lspci -nn`), and the launcher's "Share my numbers" writes it after the
  GPU's name. The report bot uses it for the engine's GPU family, so Meteor Lake and Panther Lake
  GPUs that their drivers name only "Intel Graphics" count for their family
  ([#24](https://github.com/karimalsalah/guarana/issues/24)).
