- CI: only pushes save the build's dependency and compiler cache; pull requests restore the
  newest one of their base. A day of pull requests had filled the repository's 10 GB of Actions
  cache with caches only their own pull request could read, which evicted `main`'s and made its
  next Windows build start cold (65 minutes instead of about 9).
