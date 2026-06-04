# Governance

This repository is the public Meridian domain-code registry. It governs domain-code availability and holder metadata only.

## Domain States

- `reserved`: unavailable for general claims.
- `assigned`: controlled by the listed public or private holder.
- `retired`: no longer issued, but lookup-valid forever.
- `disputed`: unavailable while maintainers resolve the claim.

Assigned and retired domains are not casually recycled.

## Claim Review

The default rule is first valid approved claim wins. Maintainers may reject or pause claims for abuse, squatting, confusing similarity, impersonation risk, bad-faith behavior, malformed records, or missing provenance.

Registry records are not legal identity proof, security proof, clinical certification, regulatory certification, or an endorsement of the holder.

## Public And Private Holders

Public holder records may show a public label and stable holder reference.

Private holder records must use `holder.visibility: "private"`, a `holder_<CROCKFORD>` pseudonymous holder reference, and `public_label: null`. Private holder identity mappings must not be committed to this repository.

No registry JSON record may contain raw emails, phone numbers, or postal addresses.

## Prefix Authority

This repository governs domain codes only. Once a domain is assigned or reserved for a holder, that holder controls all prefixes below that domain.

Prefix registries may be public, private, or undeclared. This repository does not centrally govern prefix assignments.

Software must not infer object type, workflow state, assay meaning, clinical meaning, business logic, or regulatory status from domain or prefix strings.
