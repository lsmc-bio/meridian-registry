# Implementation Notes

The bootstrap account below is historical. Current requests follow
[Contributing](../CONTRIBUTING.md) and the [prefix guide](prefix-registries.md),
with approval and merge through PRs to `main`.

## Source Files Inspected

The bootstrap used `/Users/jmajor/projects/lsmc/archived/meridian-euid` as the authoritative Meridian source. The inspected files were:

- `SPEC.md`
- `domain_code_registry.json`
- `prefix_ownership_registry.json`
- `reference-implementations/python/meridian_euid/euid.py`
- `reference-implementations/python/meridian_euid/governance.py`
- `reference-implementations/python/meridian_euid/mod32.py`
- `docs/plans/20260521T214153Z_reserved_m_n_domain_ledger.md`

The older archive `/Users/jmajor/projects/lsmc/archived/blahhh/meridian-euid.tgz` was found but not used as source truth.

## Domain-Code Rules

The current Meridian source defines domain codes as 1-4 characters from:

```text
0123456789ABCDEFGHJKMNPQRSTVWXYZ
```

Forbidden characters are `I`, `L`, `O`, and `U`. Lowercase, whitespace, non-ASCII input, tolerant decoding, trimming, and character substitution are rejected.

## Source Registry Facts

The source domain registry includes these reserved domains:

- `A`: reserved; not assigned for issuance.
- `F`: reserved for Inflection.
- `M`: reserved for LSMC, already in production use, with triple approval required for LSMC non-production use.
- `N`: reserved for LSMC in the archived source.
- `W`, `X`, `Y`, `Z`: testing reserved domains.

The source JSON spells `reserved_for` as `testig` for `W`, `X`, `Y`, and `Z`; this registry normalizes the public note to testing/examples language and records the source spelling here for provenance.

## Prompt Conflicts

The bootstrap prompt requested `M`, `N`, and `D` as assigned domains and mapped `N` to Inflection. The first bootstrap implementation followed the archived Meridian source for `N`; the user then corrected the registry requirement on 2026-06-04: `N` is for Inflection.

- `M` remains reserved for LSMC, not changed to assigned.
- `N` is assigned to Inflection by explicit user correction.
- `F` is included as the current Inflection reservation.
- `D` is added as a new assigned bootstrap record for Daylily Informatics because the current source did not register `D`; the source did include `D2` as a routing example domain.

## Legacy Examples Not Imported As Claims

The source registry also contains example or boundary domains `0`, `A1`, `AB9`, `D2`, `DV1`, and `MAX`. They were not imported as unavailable public claims in this new registry model.

## Prefix Boundary

The source states that prefix ownership is `(DOMAIN, PREFIX)` governance and
resolver routing is governance behavior, not business truth. The original
bootstrap hosted domains only. The registry now optionally hosts prefix records
with domain-holder approval; the holder retains assignment authority.
