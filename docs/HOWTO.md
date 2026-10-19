# How to use

Setup: Python >= 3.11, git, `gh` CLI authenticated (`gh auth login`).
```
pip install -e . pytest
tm ingest owner/repo [--no-github]       # clones to data/owner__repo/repo, writes tm.db (slow: GitHub API)
tm replay owner/repo --from YYYY-MM-DD --to YYYY-MM-DD --every-days 60 --window-days 180
python -m pytest tests
```
`tm replay` currently runs only the two baselines.

## Writing the real system
Subclass `Predictor` (`timemachine/predictor.py`), implement what you support, and use ONLY the `view` argument:
```python
class MyPredictor(Predictor):
    name = "claude_kb"
    def risky_commits(self, view, candidates):
        # view.diff(sha), view.files(sha), view.issues(), view.issue_state(n), view.comments(n)
        return [Flag(c["sha"], score) for c in candidates]
```
Then call `evaluate.replay(db, repo, MyPredictor(), times)` and register it in `cli.py`. Scores rank candidates; the evaluator flags the top `top_frac`.

Knowledge-base/agent code must read data through `TimeView`; building the KB per T from the view is the safest way to keep the leakage guarantee.

## Gotchas
- `tm ingest` can take minutes on issue-heavy repos; re-running re-fetches everything.
- The package imports `Oracle` only in `evaluate.py`. Keep it out of predictor code.
- `data/` is large and regenerable; do not commit it.
