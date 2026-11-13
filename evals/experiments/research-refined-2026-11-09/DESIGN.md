# Experiment design

Model: gpt-6.1-sol. Independent user-authorized GalaxyData endpoint; no Codex configuration read.
A: frozen compact-v3. B: this experiment's instructions-upgraded.md.
60 cases, one new sample per case per arm, medium reasoning, low verbosity, store=false, three workers.
38 unnecessary-defense cases; 14 accuracy controls; 4 executable capability controls; 4 disposable workspace cases.
Read complete answers with masked arm labels and frozen criteria. Author review is not independent. Count semantic additions and substitute caveats; record unsupported facts separately.
Adoption gate: no more unnecessary defenses or factual errors than the newly sampled baseline; all accuracy, artifact and capability checks pass; total reported tokens do not increase.
These cases are development/regression cases; after the first pass they are not held-out cases. Record failures and rejected candidates. No per-use reviewer calls or text postprocessing.
