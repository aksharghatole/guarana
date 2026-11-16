- Merge gate: `tools/ci/pr_gate.py` now requires the "Check the changelog entry" job, so a pull
  request whose changelog check failed or has not reported is no longer called ready. `main` is
  still judged by the three jobs every push runs, and a `resolve/pr-N` commit takes the changelog
  verdict of its pull request's head ([#147](https://github.com/karimalsalah/guarana/issues/147)).
