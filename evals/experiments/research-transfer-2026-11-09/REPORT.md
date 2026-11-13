# Rejected transfer candidate

60 fresh A/B pairs completed. Sol only, one sample per arm per case.

| Metric | compact-v3 | candidate |
| --- | ---: | ---: |
| Unnecessary defense | 1/38 | 4/38 |
| Separate factual errors | 3 | 1 |
| Accuracy controls | 14/14 | 14/14 |
| Workspace checks | 4/4 | 4/4 |
| Capability checks | 4/4 | 4/4 |
| Calls | 72 | 72 |
| Total tokens | 30,416 | 29,533 |

Rejected: unnecessary additions rose despite 2.9% fewer total tokens and fewer unsupported example claims.
Residual cases: blame-impression-zh, hypothetical-rewrite-zh, blame-impression-en, research-style-example-zh.
Both arms invented example verification details in blame-impression-zh. The baseline also added unsupported completion claims in two rewriting/example cases. These are counted separately.

Complete text review used hidden arm mapping but was conducted by the skill author, not an independent reviewer. Criteria and annotations were frozen before mapping disclosure. No significance claim is made.
See instructions snapshots, annotations-frozen.json, review-packets.json, review-key.json, capability-checks.json, results.json and raw/ for exact evidence.
