# Compact entry: first candidate rejected

Independent GalaxyData gpt-6.1-sol, medium reasoning, low verbosity; 46 cases repeated twice, 92 matched pairs, 184 complete answers. Frozen A is tail-v2 (2,817 characters), B the first compact candidate (1,444 characters). Single-author manual review used shuffled arm-hidden packets; frozen annotations and complete raw outputs are included.

| Metric | A | B |
| --- | ---: | ---: |
| Unnecessary defensive additions | 1/64 | 8/64 |
| Accuracy controls | 12/12 | 12/12 |
| Capability controls | 8/8 | 8/8 |
| Actual workspace contracts | 8/8 | 8/8 |
| Calls | 116 | 116 |
| Input tokens | 67,392 | 40,722 |
| Output tokens | 7,022 | 7,464 |
| Total tokens | 74,414 | 48,186 |

Total tokens decreased 35.25%, but semantic defensiveness worsened. There were seven B-only failures and one shared failure (exact McNemar p=0.015625). Examples and rewrites reintroduced scope warnings; style critiques suggested verification-gap advice. Controls and executable code passed. Cost savings alone did not satisfy acceptance: this candidate was rejected and is not the delivered skill.

The next iteration restores the missing scope and whole-addition-removal decisions in one paragraph, retaining a shorter entrypoint. See [the refined experiment](../compact-entry-refined-2026-11-09/REPORT.md). Snapshots here remain unchanged; the current SKILL.md belongs to the later iteration.
