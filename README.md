# Constraint Exec

An Agent Skill that keeps the user's primary objective ahead of negative constraints and soft preferences. It reduces the tendency to replace useful work with extra guards, scanners, policy layers, rejection paths, or repeated compliance commentary.

Current repository version: `0.4.0-rc.11` (updated November 13, 2026). This prerelease publishes the November 9 direct-interaction upgrade, cross-source research, and complete paired regression evidence. Final `0.4.0` promotion remains gated by the complete model matrix and independent semantic review.

## Latest measured upgrade — November 9, 2026

The final candidate removes whole unsolicited defensive additions, including substitute verification advice, and keeps examples grounded in supplied facts. It retains useful uncertainty, substantive negative findings, and authorized coding through relevant checks. Ordinary Skill use adds no model calls.

The latest experiment contains 60 fresh paired cases on `gpt-6.1-sol`, with medium reasoning and low verbosity. The comparison is against the preceding frozen `compact-v3` entry, not against the August release or an unskilled baseline.

| Metric | Previous compact-v3 | Final upgrade |
| --- | ---: | ---: |
| Unnecessary defensive additions | 1/38 | 0/38 |
| Unsupported factual or completion additions | 2 | 0 |
| Accuracy controls | 14/14 | 14/14 |
| Executable capability controls | 4/4 | 4/4 |
| Real workspace checks | 4/4 | 4/4 |
| Model calls | 72 | 72 |
| Input tokens | 26,424 | 25,910 |
| Output tokens | 4,171 | 3,958 |
| Total tokens | 30,595 | 29,868 |

Total reported tokens fell **2.38%**. The entrypoint is 1,593 characters; file size is not the basis for the cost claim. These are development regression cases with one sample per case and arm. Complete-answer review masked the arms, but the reviewer was the author, not an independent reviewer. Astra was not sampled in this experiment.

Two preceding candidates were rejected: the first increased defensive additions from 1/38 to 4/38; the second removed those additions but increased unsupported facts from 1 to 3. All three rounds retain separate reports, frozen annotations, outputs and tool records. Across the three rounds: 180 paired cases, 432 model calls, 180,559 tokens.

See the [final report](evals/experiments/research-grounded-2026-11-09/REPORT.md), [machine-readable summary](evals/experiments/research-grounded-2026-11-09/summary.json), [all-round publication data](research/2026-11-13-publication-data.json), and [seven-project/six-paper synthesis](research/2026-11-09-cross-source-synthesis.md). Recheck saved evidence offline with `python scripts/verify-interaction-evidence.py`; this does not call a model.

## Direct interaction and coding upgrade

The instructions target GPT-6 Astra and GPT-6.1 Sol; the new measured evidence is for Sol. The upgrade deletes unnecessary defensive additions instead of paraphrasing them, retains resolved context across follow-ups, acts on authorized coding requests, and completes relevant checks. Necessary corrections and accurate verification status remain part of the answer.

See [the collected community feedback and official guidance](research/2026-11-09-direct-interaction.md), [the earlier compact-entry A/B](evals/experiments/compact-entry-refined-2026-11-09/REPORT.md), and [the cross-source research](research/2026-11-09-cross-source-synthesis.md). The preceding 1,601-character entry is frozen as `compact-v3`. The current 1,593-character entry preserves meaningful uncertainty and negative findings without adding a disclaimer-check call. The older 2,817-character version is frozen as `tail-v2`. A 1,444-character first compression failed semantic retention and was rejected; its report remains under `evals/experiments/compact-entry-2026-11-09/`. Earlier removal and example-tail experiments also remain under `evals/experiments/`.

Run the compact comparison with an independent credential environment:

```bash
python evals/run_interaction_eval.py --base-url HTTPS_ENDPOINT --api-key-env INDEPENDENT_SOL_KEY --cases evals/compact_entry_cases.json --variant tail-v2 --variant upgraded --repeats 2 --output evals/experiments/compact-entry-new
python evals/run_interaction_eval.py --base-url HTTPS_ENDPOINT --api-key-env INDEPENDENT_SOL_KEY --cases evals/research_combined_cases.json --variant compact-v3 --variant upgraded --repeats 1 --output evals/experiments/research-transfer-new
# Set the named credential variable outside the repository; no Codex configuration is read.
```

The original compact suite retains 42 conversation/accuracy/workspace cases and four capability controls for hard dependency exclusions, soft preferences, explicit enforcement and exact output. The cross-source comparison adds 14 transfer cases. Read complete answers against the case criteria, counting whole unnecessary additions including paraphrases. Real workspace cases save source files and independent contract-test results. This iteration additionally requires total reported token cost not to increase. Only `gpt-6.1-sol` is sampled; Astra is covered by shared instructions and has no measured result here. Focused evidence remains separate from the repository's full release matrix. See [the final comparison](evals/experiments/research-grounded-2026-11-09/REPORT.md) for current results.

## Historical measured result — August 22, 2026

The published prerelease A/B run was executed on August 22, 2026 with `gpt-5.6-sol`, medium reasoning effort, low verbosity, and direct Responses API requests to the OpenAI-compatible endpoint. It covers 30 matched prompts: 15 English and 15 Chinese. The suite contains 12 hard-constraint cases, 6 soft-preference cases, 6 safety or explicit-enforcement cases, and 6 output or architecture-constraint cases. The API key was supplied only through a temporary local authentication file and is not part of the repository or evidence.

| Metric | Baseline | Skill | Change |
| --- | ---: | ---: | ---: |
| Evaluation pass rate | 100.00% | 100.00% | unchanged |
| Objective coverage | 1.0000 | 1.0000 | unchanged |
| Constraint adherence | 1.0000 | 1.0000 | unchanged |
| Over-optimization score | 0.9333 | 0.6333 | **32.1% lower** |
| Unnecessary constraint echo | 0.5333 | 0.3333 | **37.5% lower** |
| Constraint-only components | 0.1333 | 0.1000 | **25.0% lower** |
| Total token cost | 229,666 | 89,367 | **61.1% lower** |

All 30 pairs pass objective and constraint gates. Per case, 5 improved, 5 worsened, and 20 tied on the deterministic over-optimization score. Required safety enforcement is measured for compliance but is not counted as unnecessary constraint repetition. Quality and non-constraint requirement retention are both `1.0000`, the machine-detected capability regression rate is `0.0000`, aggregate token cost ratio is `0.3891`, latency ratio is `0.6858`, and the published A/B capability gate passes.

See [`evals/results/REPORT.md`](evals/results/REPORT.md), [`evals/results/summary.json`](evals/results/summary.json), [`evals/results/scores.json`](evals/results/scores.json), [`evals/results/metadata.json`](evals/results/metadata.json), and the 60 committed raw responses for the full evidence. Earlier rc.9 evidence remains in [`evals/results/archive/0.4.0-rc.9/`](evals/results/archive/0.4.0-rc.9/) and [`evals/results/archive/0.4.0-rc.9-codex-cli-2026-08-22/`](evals/results/archive/0.4.0-rc.9-codex-cli-2026-08-22/). This is a deterministic, single-model regression experiment, not a universal performance claim or a statistical significance test.

## V1.5/V2 execution protocol

The repository now includes deterministic execution primitives in [`evals/protocol.py`](evals/protocol.py):

- versioned structured-plan parsing and validation;
- separate constraint, implementation strategy, and failure-gate fields;
- relation-based gate detection with negation and quoted-example handling;
- plugin validators for JSON, Markdown, file scope, and Python AST/compile checks;
- explicit `pass`, `fail`, and `unsupported` artifact states;
- bounded Level 1 artifact repair, Level 2 artifact regeneration, and Level 3 replanning decisions.

`evals/run_ab.py` preserves the released `baseline`/`skill` comparison. `evals/run_matrix.py` runs eight orthogonal
variants: baseline, full V1, two V1 rule removals, positive framing, structured planning, plan validation, and full V2.
Structured variants use separate plan and execution calls; full V2 adds deterministic artifact validation and bounded
repair. `evals/run_runtime.py` validates actual workspace artifacts with allowlisted validators and tests.

`evals/run_protocol_fixtures.py`, `evals/run_runtime_fixtures.py`, and `evals/evaluate_validators.py` provide deterministic
conformance evidence. `evals/build_experiment_report.py` reports failed and missing rows explicitly instead of converting
them into zero-valued metric samples. See [`evals/experiments/EXPERIMENT_STATUS.md`](evals/experiments/EXPERIMENT_STATUS.md)
for the current completion state. Validation errors are machine feedback; over-optimization scores are evaluation-only
and are never included in model repair prompts.

The artifact validators prove observable contracts only. Unsupported semantic checks remain explicitly `unsupported`.

## Capability retention

Constraint compliance is not accepted when it makes the model less useful. The evaluation layer pairs each candidate with the same case, model, repeat, and sampling signature, then reports:

- objective, hard-constraint, enforcement, format, path, and artifact retention;
- non-constraint requirement and declared quality retention;
- unnecessary refusal, clarification, and excessive-caution regressions;
- token and latency ratios as separate efficiency metrics.

Missing or failed pairs are coverage gaps, not zero scores. Output length and keyword counts do not prove quality. A final candidate with a functional, required-content, artifact, or declared-quality regression fails the release gate even if its over-optimization score improves.

For semantic quality that deterministic contracts cannot establish, `evals/pairwise_review.py` prepares anonymized baseline/candidate review packets and separate mapping keys. Final release evidence requires two independent reviewers per pair; disputed pairs require adjudication. Reviewers score correctness, completeness, usefulness, and requirement retention on both sides instead of inferring quality from keywords.

## Model-independent runtime

`evals/executors/` provides Codex CLI and local Ollama adapters with common request, result, capability, usage, and failure contracts. `scripts/execute_protocol.py` exposes the plan, execute, validate, and bounded-repair flow through versioned JSON input and output. Workspace writes require an executor that declares workspace access; unsupported capabilities terminate explicitly.

Runtime validators are selected from a fixed registry. File access is contained to the workspace, commands must match an allowlist and run without a shell, and unknown validators return `unsupported`. Trace and result persistence redact credential-shaped values and use isolated temporary runtime state.

The runtime is an operator-controlled local interface, not a remote sandbox for untrusted JSON. Only load request files from trusted automation. Constrain workspace and output roots before invocation, pass the minimum environment needed by the executor, keep credentials outside the workspace, and treat redaction as defense in depth rather than secret storage.

## Install

Use Node.js 22.20 or later. The commands below install a copied Skill globally and do not rely on symlinks.

Install for Codex, Claude Code, and OpenCode in one command:

```bash
npx --yes skills@1.5.22 add Success6666/constraint-exec --skill constraint-exec --agent codex --agent claude-code --agent opencode --global --copy --yes
```

Install for one agent:

```bash
npx --yes skills@1.5.22 add Success6666/constraint-exec --skill constraint-exec --agent codex --global --copy --yes
npx --yes skills@1.5.22 add Success6666/constraint-exec --skill constraint-exec --agent claude-code --global --copy --yes
npx --yes skills@1.5.22 add Success6666/constraint-exec --skill constraint-exec --agent opencode --global --copy --yes
```

For a project-local installation, run the same command from the project root and omit `--global`.

For Claude Desktop in API/third-party mode, custom skills use Desktop's own local skill store; the Claude Code installation is separate. On the inspected Desktop 4.16336.0 build, the store is under the active profile's `local-agent-mode-sessions/skills-plugin/<organization>/<account>/`, with skill files under `skills/<name>/` and a user entry in `manifest.json`. Local entries use `creatorType: "user"`, `syncManaged: false`, and `enabled: true`. Back up the manifest and preserve existing entries when installing locally. The exact profile and identifiers depend on the deployment; do not hardcode this machine's paths. A fresh Desktop session loads the saved skill. The November 9 installation was verified through Desktop's bundled Claude Code 2.1.317 `/skills` menu; the live Desktop UI was not tested.

Verify repository discovery before installation:

```bash
npx --yes skills@1.5.22 add Success6666/constraint-exec --list
```

## Use

Invoke the Skill explicitly:

```text
Use $constraint-exec to complete this task.
```

Its description supports automatic discovery when constraints, defensive caveats, repeated confirmation, or incomplete coding obstruct the requested result.

## What It Changes

- Keeps the requested deliverable as the success criterion.
- Answers the actual claim and deletes whole unnecessary defensive additions.
- Keeps resolved caveats and authorization in context across follow-ups.
- Completes authorized coding work and proportionate checks.
- Treats hard constraints as boundaries and soft preferences as tradeoffs.
- Avoids unrequested detectors, scanners, middleware, CI gates, and rejection paths.
- Preserves enforcement when the user explicitly requests it or safety requires it.
- Demonstrates compliance through the result instead of repeatedly discussing the constraint.
- Avoids mentioning the Skill or its internal instructions in the final answer.

## Evaluation

Run local validation:

```bash
python -m unittest discover -s tests -v
python -m compileall -q evals scripts tests
python scripts/verify-install.py
python scripts/verify-interaction-evidence.py
```

Run or resume the A/B evaluation with an authenticated Responses-compatible endpoint:

```bash
python evals/run_ab.py --transport responses --variant both --model gpt-5.6-sol --base-url BASE_URL --reasoning-effort medium --verbosity low --jobs 1
python evals/run_ab.py --transport responses --variant both --resume --model gpt-5.6-sol --base-url BASE_URL --reasoning-effort medium --verbosity low --jobs 1
python evals/rescore.py
python evals/build_report.py
python evals/evaluate_validators.py --output evals/experiments/validator-v1/results.json
python evals/run_protocol_fixtures.py
python evals/run_runtime_fixtures.py
```

Run an isolated orthogonal matrix or workspace-artifact experiment:

```bash
python evals/run_matrix.py --experiment full-matrix --model MODEL --variant baseline --variant full-v2
python evals/run_matrix.py --experiment local-matrix --executor ollama --model qwen3.5:9b --variant baseline --variant full-v2
python evals/run_runtime.py --experiment runtime-matrix --model MODEL --mode direct --mode full-v2
python evals/pairwise_review.py prepare --results RESULTS.json --experiment-root EXPERIMENT_DIR --variant full-v2 --seed-file reviewer-1.seed --reviewer-id reviewer-1 --cases evals/cases.json --reviews reviewer-1.json --key reviewer-1.key.json
python evals/pairwise_review.py prepare --results RESULTS.json --experiment-root EXPERIMENT_DIR --variant full-v2 --seed-file reviewer-2.seed --reviewer-id reviewer-2 --cases evals/cases.json --reviews reviewer-2.json --key reviewer-2.key.json
python evals/pairwise_review.py apply --results RESULTS.json --reviews reviewer-1.json --key reviewer-1.key.json --reviews reviewer-2.json --key reviewer-2.key.json --minimum-reviewers 2 --output RESULTS.reviewed.json
python evals/release_experiment.py --dry-run --allow-dirty --allow-untagged
```

Run the stable Agent Runtime interface:

```bash
python evals/agent_runtime.py --describe
python evals/agent_runtime.py --request generation-request.json --response generation-response.json
python scripts/execute_protocol.py request.json --workspace-root WORKSPACE_ROOT --artifact-root ARTIFACT_ROOT --output result.json
```

The first interface performs one model generation with normalized capabilities and failures. The second executes the full plan, validate, and bounded-repair protocol.

The full execution request and result contracts are defined in `evals/schemas/runtime-request.schema.json` and `evals/schemas/result.schema.json`. The single-generation interface uses `evals/schemas/generation-request.schema.json` and `evals/schemas/generation-response.schema.json`. Benchmark pairing, frozen datasets, required matrices, semantic review coverage, and release gates are declared in `evals/benchmark-manifest.json`; the benchmark and release configuration have dedicated schemas under `evals/schemas/`.

Each case uses an isolated temporary Git repository and a temporary `CODEX_HOME` containing only a copied authentication file. The authentication copy is deleted after the subprocess exits. Checkpoints are written atomically after each result, and one failed case does not discard completed results.

Release runs first verify frozen dataset hashes, JSON schemas, Skill metadata, and source secret patterns. Resume is valid only when the case, executor, model, sampling configuration, variant, validator profile, and budgets match the saved signature. Human review mapping keys and seeds stay separate from blinded review packets and generated outputs.

The deterministic scorer measures:

- objective coverage and hard constraint compliance;
- required safety or explicit enforcement;
- response-format and file-scope constraints;
- unrequested failure gates and constraint-only components;
- unnecessary constraint repetition and soft-preference hardening.

## Repository Layout

```text
skills/constraint-exec/                  Skill package
evals/cases.json                         30-case bilingual benchmark
evals/run_ab.py                          Isolated concurrent A/B runner
evals/run_matrix.py                      Orthogonal plan/execute/repair matrix runner
evals/run_runtime.py                     Real workspace artifact runner
evals/executors/                         Model execution adapters
evals/validators/                        Allowlisted artifact validator registry
evals/capability_metrics.py              Paired capability-retention metrics
evals/pairwise_review.py                 Blinded semantic capability review workflow
evals/scorer.py                          Deterministic scorer
evals/build_experiment_report.py         Strict completeness and metric report
evals/results/                           Raw responses, scores, and report
scripts/execute_protocol.py              Versioned Agent Runtime JSON CLI
scripts/verify-install.py                Cross-agent installation verifier
tests/                                   Unit and distribution tests
```

## License

MIT
