# Ground truth (oracle) per output

Window W (default 180 days) after T. Implemented in `timemachine/groundtruth.py`.

| Output | Status | Positive when | Weakness |
|---|---|---|---|
| 1 Risky change | done | flagged commit is blamed (SZZ: `git blame -w` on lines a fix deleted/changed, in `fix^`, skipping test/doc files) by a fix commit in (T, T+W] | fix detection by message keywords or closing a `bug`-labeled issue; SZZ is noisy on refactors/whitespace/moves |
| 2 Missing tests | done (heuristic) | flagged commit touched no test files AND later a test commit touches a file with a matching stem, or a later fix touches the same source files | stem matching is crude; no real coverage data |
| 3 Similar past issue | done (partial) | new issue later says "duplicate of #N" (comment/body) and N is in the top-k returned | misses `marked_as_duplicate` targets and cross-references; hit rate only measured on issues that have a duplicate target |
| 4 Similar bug from diff | TODO | diff resembles past bug-introducing change AND flagged change is later confirmed buggy (Output 1 truth) or fix commit references the matched bug | needs diff-similarity predictor |
| 5 Outdated docs | TODO | doc updated in later commit to match flagged change, or a doc issue is opened | |
| 6 Test/build time regression | TODO (stretch) | needs CI data (Input 5) | most public repos lack it |
| 7 Requirement vs impl | TODO | linked issue reopened, follow-up says incomplete, or change reverted | noisy; manually review ~30 cases |

Metrics: precision, recall, F1, lead time (fix ts minus T). Baselines: random, most-changed-files. Spec also requires a memorization check (repos/periods after the model's training cutoff).
