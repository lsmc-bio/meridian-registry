# meridian-registry

Public Meridian domain-code registry.

Meridian EUIDs have the form `DOMAIN-PREFIX-BODYCHECKSUM`. This repository governs only the `DOMAIN` part. Once a domain is assigned or reserved for a holder, that holder controls prefix assignments below that domain.

Registry data is governance metadata. Software must not infer object type, workflow behavior, clinical meaning, business logic, or regulatory status from domain or prefix strings.

## Domain Codes

Domain codes follow the Meridian source specification:

- Length: 1-4 characters
- Alphabet: `0123456789ABCDEFGHJKMNPQRSTVWXYZ`
- Forbidden characters: `I`, `L`, `O`, `U`
- Lowercase, whitespace, non-ASCII input, trimming, and character substitution are rejected

## Files

Source records live in `registry/domains/<DOMAIN>.json`.

The generated index lives in `registry/generated/domains.json` and is built from the source records:

```bash
python tools/build_index.py --stable
```

## Check Availability

Install development dependencies, then run:

```bash
python -m pip install -r requirements-dev.txt
python tools/check_domain.py Q
python tools/check_domain.py D
```

Exit codes:

- `0`: valid and available
- `1`: valid but unavailable
- `2`: invalid input or registry error

## Current Bootstrap Records

| Domain | Status | Holder or purpose |
|---|---|---|
| `A` | reserved | Registry-reserved; not assigned for issuance in the Meridian source |
| `D` | assigned | Daylily Informatics |
| `F` | reserved | Inflection |
| `M` | reserved | LSMC |
| `N` | assigned | Inflection |
| `W` | reserved | Testing/examples |
| `X` | reserved | Testing/examples |
| `Y` | reserved | Testing/examples |
| `Z` | reserved | Testing/examples/development/documentation fixtures |

The inspected Meridian source reserves `F` for Inflection and listed `N` for LSMC. The registry record for `N` follows the explicit 2026-06-04 user correction that `N` is for Inflection.

## Claim A Public Domain

Open a public domain-claim issue or pull request that adds one JSON record under `registry/domains/`. The record must validate, must not include personal data, and must explain the public holder label.

First valid approved claim wins, subject to maintainer review for abuse, confusing claims, squatting, or bad-faith submissions.

## Private Claims

A private claim may publish only an assigned status and pseudonymous holder reference. Do not commit private identity mappings, raw emails, phone numbers, or postal addresses to this repository.

See `docs/private-claims.md`.

## Prefix Registries

Prefix registries are optional and controlled by the domain holder. This repository may list a public prefix-registry URL, but it does not approve or validate prefix assignments below a domain.

See `docs/prefix-registries.md`.

## Validate Locally

```bash
python -m pip install -r requirements-dev.txt
python tools/build_index.py --stable
python tools/validate_registry.py
python -m pytest
git diff --exit-code
```
