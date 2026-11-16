- Android: only release builds (tags, the nightly and runs on `main`) are signed with the release key.
  Pull requests and runs dispatched by hand build preview APKs with the debug key, and the decoded
  keystore is deleted even when the build fails.
