# Experiment status — publication update 2026-11-13

Latest Skill: `0.4.0-rc.11`. The November 9 Sol interaction evidence contains three complete 60-pair rounds. The first and second candidates were rejected; the final candidate was adopted. The complete model matrix for final `0.4.0` promotion remains incomplete.

| Round | Defense, previous → candidate | Unsupported facts, previous → candidate | Total tokens, previous → candidate | Decision |
| --- | --- | --- | --- | --- |
| research-transfer | 1/38 → 4/38 | 3 → 1 | 30,416 → 29,533 | rejected |
| research-refined | 1/38 → 0/38 | 1 → 3 | 30,544 → 29,603 | rejected |
| research-grounded | 1/38 → 0/38 | 2 → 0 | 30,595 → 29,868 | adopted |

All three rounds passed 14/14 accuracy controls, 4/4 workspace checks and 4/4 executable capability controls in each arm. Each arm used 72 calls. Review was performed by the author with arm labels masked. Cases became development regression cases after the first pass. Astra was not sampled.

See [publication data](../../research/2026-11-13-publication-data.json) and the [final report](research-grounded-2026-11-09/REPORT.md). Run `python scripts/verify-interaction-evidence.py` to check the saved outputs, annotation hashes, pairing and totals offline.

The following August 17 report is retained as a historical snapshot. Its older published-ab scores do not represent the August 22 or November 9 runs.

---

# Complete Experiment Report

- Status: `incomplete`
- Generated: `2026-08-17T02:44:09.981966+00:00`

## Matrix Experiments

| Experiment | Expected | Completed | Failed | Missing | Complete |
| --- | ---: | ---: | ---: | ---: | :---: |
| `published-ab` | 60 | 60 | 0 | 0 | yes |
| `model-probe-extended` | 1 | 0 | 1 | 0 | no |
| `secondary-model-probes` | 2 | 0 | 2 | 0 | no |

## Variant Metrics

### published-ab

| Variant | N | Eval Pass | Objective | Adherence | Required Enforcement | Under-Enforcement | Over-Optimization |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | 30 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.8333 |
| `skill` | 30 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.1667 |

### model-probe-extended

| Variant | N | Eval Pass | Objective | Adherence | Required Enforcement | Under-Enforcement | Over-Optimization |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | 0 | n/a | n/a | n/a | n/a | n/a | n/a |

Failures:
- `gpt-5.6-sol` / `baseline` / `fastapi-no-redis`: `execute`

### secondary-model-probes

| Variant | N | Eval Pass | Objective | Adherence | Required Enforcement | Under-Enforcement | Over-Optimization |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | 0 | n/a | n/a | n/a | n/a | n/a | n/a |

Failures:
- `gpt-5.6-terra` / `baseline` / `fastapi-no-redis`: `execute`
- `gpt-5.5` / `baseline` / `fastapi-no-redis`: `execute`

## Runtime Experiments

| Experiment | Expected | Passed | Failed | Missing | Retries | Complete |
| --- | ---: | ---: | ---: | ---: | ---: | :---: |

## Protocol Conformance

| Protocol | Expected | Passed | Failed | Missing | Retry Rate | Average Retries | Complete |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `deterministic-v2-fixtures-v1` | 6 | 6 | 0 | 0 | 0.6667 | 0.8333 | yes |
| `runtime-validator-fixtures-v1` | 12 | 12 | 0 | 0 | 0.0000 | 0.0000 | yes |

## Gate Validator

- Cases: `32`
- Accuracy: `1.0`
- Precision: `1.0`
- Recall: `1.0`
- Failures: `0`

Missing and failed rows are never converted to zero-valued metric samples.
