- Windows ARM64 release builds link again: the Switch 2 BLE WinRT code now compiles against the
  exact C++/WinRT version the Qt arm64 package was built with (2.0.250303.1, fetched from NuGet),
  instead of the Windows SDK's newer 2.0.250303.5 that lld-link's `/failifmismatch` rejects.
- macOS release builds no longer fail when the runner's freetype bottle still links
  `libhvf.dylib` (which macOS 15.0-15.3 lack): freetype is rebuilt from source on the runner.
