# Roadmap (suggested order)

1. **Better bug-fix detection** (`Oracle.fix_commits`): "Fixes/Closes #N" in commit or PR text, PR-to-commit mapping, `bug` labels on linked PRs. Rerun on bigger repos; Output 1 has only ~10 positives on click.
2. **Repo selection**: several mid/large repos with active issue trackers and tests, plus repos/periods after the LLM's training cutoff. Decide and record them in `docs/STATE.md`.
3. **First Claude-backed `Predictor`**: build the knowledge base from a `TimeView` (embeddings over issues/diffs, file churn/bug history), use Claude Code/agents as the spec asks, start with Outputs 1-3.
4. **Output 4** (diff similarity to past bug-introducing changes; reuse Output 1 truth).
5. Hardening: tests for `issue_state`, oracle, evaluator; incremental GitHub ingest; multiple random seeds and confidence intervals; handle edited-issue-text leakage.
6. Secondary: Outputs 5 and 7 (with manual review of ~30 cases). Stretch: CI data and Output 6.
