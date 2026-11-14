# Governance

This repository records public domain assignments and may host prefix
assignments approved by the relevant domain holder.

## Domain States

- `reserved`: unavailable for general claims.
- `assigned`: controlled by the listed public or private holder.
- `retired`: no longer issued, but lookup-valid forever.
- `disputed`: unavailable while maintainers resolve the claim.

Retired domains and prefixes remain permanently recorded and are never
reassigned to unrelated issuers. Transfers preserve allocation history.

## Claim Review

Requests for domains and prefixes, including reserved ones, must be PRs to
`main`. The first approved and merged assignment wins. A pending PR reserves
nothing. Maintainers review domain claims; domain holders approve hosted prefix
claims. Reserved namespaces need their existing authority's approval.

Git records the accepted change and history. Review competing requests against
the current `main` record; never resolve a conflict by replacing a grant with an
unrelated owner. Existing GitHub access and review controls provide the authority
mechanism. The helper scripts do not authenticate a holder or stop an
administrator deliberately bypassing that process.

Registry records are not legal identity proof, security proof, clinical certification, regulatory certification, or an endorsement of the holder.

## Public And Private Holders

Public holder records may show a public label and stable holder reference.

Private holder records must use `holder.visibility: "private"`, a `holder_<CROCKFORD>` pseudonymous holder reference, and `public_label: null`. Private holder identity mappings must not be committed to this repository.

No registry JSON record may contain raw emails, phone numbers, or postal addresses.

## Prefix Authority

Once a domain is assigned or reserved for a holder, that holder controls its
prefixes. Hosting records here does not transfer that authority.

Prefix registries may be hosted here, public elsewhere, private, or undeclared.
A holder explicitly adopts this registry before using it for new grants,
accounting for existing reservations. Software does not discover historical
installations or automatically import claims.

The owner token identifies one continuing allocator, not merely a software
product. Independent writable databases need distinct domain/prefix assignments.
Processes sharing one native allocator may share its assignment. Supported
recovery preserves allocation history through the existing native controls.

Provision from an explicit accepted revision. Issuance stays local and may
continue offline; a registry edit is not an instant remote revocation.

Software must not infer object type, workflow state, assay meaning, clinical meaning, business logic, or regulatory status from domain or prefix strings.
