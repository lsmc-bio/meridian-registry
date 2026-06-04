# Meridian Registry Bootstrap Execution Ledger

Date: 2026-06-04

## Summary

Create a new public, GitHub-native Meridian domain-code registry at `/Users/jmajor/projects/lsmc/archived/meridian-registry`. The registry governs domain codes only, not prefix assignments below a domain. Current Meridian source wins over prompt examples when they conflict.

## Gate 0: Inventory Freeze

- Controlling plan: user-provided "Multi-Agent Ledger Plan: Meridian Registry Bootstrap".
- Ledger path: `/Users/jmajor/projects/lsmc/archived/meridian-registry/docs/plans/20260604T083126Z_meridian_registry_bootstrap_ledger.md`.
- Target repo path: `/Users/jmajor/projects/lsmc/archived/meridian-registry`.
- Source repo path: `/Users/jmajor/projects/lsmc/archived/meridian-euid`.
- Source repo status: `git status --short --branch` -> `## codex/inf6-deploy-formalization-20260528...origin/codex/inf6-deploy-formalization-20260528`.
- Target repo pre-create sweep: `test -e /Users/jmajor/projects/lsmc/archived/meridian-registry && find ... || true` -> no pre-existing files.
- Instruction files read: `/Users/jmajor/.agents/AGENTS.md`, `/Users/jmajor/.agents/AGENTS-HOW-TO-RUN-DAYOA.md`, `/Users/jmajor/.codex/AGENTS.md`, `/Users/jmajor/.codex/AGENTS-HOW-TO-RUN-DAYOA.md`, `/Users/jmajor/.codex/docs/plan-ledger-workflow.md`.
- Source files inspected: `SPEC.md`, `domain_code_registry.json`, `prefix_ownership_registry.json`, `reference-implementations/python/meridian_euid/euid.py`, `reference-implementations/python/meridian_euid/governance.py`, `reference-implementations/python/meridian_euid/mod32.py`, `docs/plans/20260521T214153Z_reserved_m_n_domain_ledger.md`.
- Source rules discovered: domain codes are 1-4 characters from `0123456789ABCDEFGHJKMNPQRSTVWXYZ`; forbidden characters are `I`, `L`, `O`, `U`; lowercase, whitespace, non-ASCII input, trimming, tolerant decoding, and character substitution are rejected.
- Source conflict recorded: current source reserves `M` and `N` for LSMC, reserves `F` for Inflection, and does not register `D`; the prompt example saying `N = Inflection` and `M/N assigned` is superseded by current source.
- Prefix boundary: source says prefix ownership is `(DOMAIN, PREFIX)` governance and software must not infer object type, workflow state, clinical meaning, assay meaning, or business truth from domain or prefix strings.
- Live-system limits: no GitHub remote creation, GitHub Pages, cloud resources, databases, servers, or live external mutations are part of this plan.

## Rows

| ID | Area | Requirement | Status | Category | Approval Gate | Owner | Evidence | Root Cause | Terminal Note |
|---|---|---|---|---|---|---|---|---|---|
| LEDGER-001 | Ledger | Initialize repo, `docs/plans/`, control ledger, branch/status baseline, source-inspection evidence | SUCCESS | plan_amendment | Gate 0 | Orchestrator | `git init -b main`; this ledger; Gate 0 inventory above |  | Repo initialized and ledger created before implementation rows were terminalized. |
| SRC-001 | Source Truth | Record inspected Meridian source files, alphabet, length, forbidden chars, current reserved domains, prefix-governance boundary | SUCCESS | feature_implementation | Gate 0 | Agent 1 | `docs/implementation-notes.md`; inspected source files listed in Gate 0 |  | Source rules and prompt conflicts are documented, including `F` for Inflection and `M/N` for LSMC. |
| REG-001 | Registry Data | Create schema and domain JSON source records for `A,D,F,M,N,W,X,Y,Z` | SUCCESS | feature_implementation | Gate 1 | Agent 2 | `schemas/domain.schema.json`; `registry/domains/{A,D,F,M,N,W,X,Y,Z}.json`; `python tools/validate_registry.py` -> passed |  | Domain records validate and filenames match domain fields. |
| REG-002 | Generated Index | Implement deterministic index builder | SUCCESS | feature_implementation | Gate 1 | Agent 2 | `tools/build_index.py`; `registry/generated/domains.json`; `python tools/build_index.py --stable` -> wrote 9 domains |  | Stable index uses `generated_at: "1970-01-01T00:00:00Z"` and sorted domain records. |
| TOOL-001 | Validation | Implement validator with schema validation, uniqueness, filename/domain match, stale-index detection, no PII scan, URL mode rules | SUCCESS | feature_implementation | Gate 2 | Agent 3 | `tools/validate_registry.py`; `tools/registry_common.py`; `python tools/validate_registry.py` -> passed; `python -m pytest` -> 14 passed |  | Validator fails hard for malformed records and stale generated output. |
| TOOL-002 | CLI | Implement `check_domain.py` exit codes and public/private display rules | SUCCESS | feature_implementation | Gate 2 | Agent 3 | `tools/check_domain.py`; `python tools/check_domain.py D` -> exit 1 assigned to Daylily Informatics; `M/N/F/Z` -> exit 1 reserved; `Q` -> exit 0 available |  | CLI behavior matches the requested availability contract. |
| DOC-001 | Docs | Write README, GOVERNANCE, CONTRIBUTING, private-claims, prefix-registries | SUCCESS | feature_implementation | Gate 3 | Agent 4 | `README.md`; `GOVERNANCE.md`; `CONTRIBUTING.md`; `docs/private-claims.md`; `docs/prefix-registries.md` |  | Docs state domain-only governance, optional holder prefix registries, and no prefix/business inference. |
| DOC-002 | Repo Metadata | Add LICENSE, minimal CODEOWNERS, issue templates | SUCCESS | feature_implementation | Gate 3 | Agent 4 | `LICENSE`; `CODEOWNERS`; `.github/ISSUE_TEMPLATE/public-domain-claim.yml`; `.github/ISSUE_TEMPLATE/private-domain-claim.md`; `.github/workflows/validate.yml` |  | CC-BY-4.0 license added; CODEOWNERS avoids invented owners; templates avoid personal data. |
| TEST-001 | Tests | Add pytest coverage for initial records, conflicts, sorting, duplicates, mismatch, invalid chars, private holder privacy, public URL requirement, no PII | SUCCESS | contract_test | Gate 4 | Agent 5 | `tests/test_registry.py`; first `python -m pytest` -> 13 passed, 1 failed due overly specific jsonschema wording assertion; patched assertion; rerun `python -m pytest` -> 14 passed |  | Tests cover requested scenarios and pass after the assertion wording fix. |
| CI-001 | CI | Add GitHub Actions validation workflow | SUCCESS | contract_test | Gate 4 | Agent 5 | `.github/workflows/validate.yml` runs Python 3.11, install deps, build stable index, validate, pytest, `git diff --exit-code` |  | CI validates schema, generated index, and tests. |
| ACCEPT-001 | Acceptance | Final ledger terminalization and summary | SUCCESS | contract_test | Gate 5 | Orchestrator | `python tools/build_index.py --stable` -> passed; `python tools/validate_registry.py` -> passed; domain CLI commands checked; `python -m pytest` -> 14 passed; initial commit created; `git diff --exit-code` -> passed |  | All rows are terminal and no blockers remain. |

## Terminal-State Report

- `SUCCESS`: 11
- `DUPLICATE`: 0
- `NO_LONGER_NEEDED`: 0
- `FAIL`: 0
- `BLOCKED`: 0
- Working rows remaining: 0

Objective complete: yes. The registry repo, source records, generated index, tooling, docs, tests, CI, and ledger are complete with current-source conflicts documented.
