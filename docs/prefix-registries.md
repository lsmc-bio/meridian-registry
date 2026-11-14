# Prefix assignments

The domain holder grants prefixes. This repository provides an optional,
Git-backed record of those grants for any Meridian client, including TapDB.
There is no allocation service or runtime discovery protocol.

## Request a prefix

Start a working branch from current `main`. Prepare one record manually or use
the Python-standard-library helper, substituting the requested values:

```bash
python tools/request_prefix.py DOMAIN PREFIX --issuer-app-code OWNER --status reserved
python tools/build_index.py --stable
```

Use `reserved` to hold a prefix without permitting issuance, or `assigned` to
request issuance authority. The helper creates a new file and refuses to
replace any existing record. It does not commit, push, open a PR, or grant
anything. Success means only that the local request file was prepared.

Open a **PR targeting `main`** with the source record, regenerated outputs,
the reason for the request, and the domain holder's approval. Reserved domains
and prefixes require their existing authority's approval. Activate an existing
reservation by editing its record in a PR, not by creating a replacement claim.

An assignment becomes effective when the authorized PR merges into `main`.
The accepted commit is its revision and provenance. A local checkout, branch,
release tag, draft PR, or issue is not itself an assignment. Concurrent requests
are decided against the current `main` record.

## Four-field records

One JSON object lives under `registry/prefixes/<DOMAIN>/<PREFIX>.json`:

| Field | Meaning |
|---|---|
| `domain` | Registered domain controlled by the approving holder |
| `prefix` | One exact 1–4 character Meridian prefix |
| `issuer_app_code` | Existing lowercase owner token for the continuing allocator |
| `status` | `reserved`, `assigned`, `retired`, or `disputed` |

No grant UUID, hostname, password, tenant list, or object inventory is needed.
Do not publish personal data or private infrastructure details. Retain retired
records permanently; do not recycle their prefixes for unrelated objects.

Independent writable databases need separate allocation spaces. Several
processes sharing one native database allocator can share its assignment.
Supported recovery preserves the assignment and allocation history through
existing database recovery controls. Prefixes do not encode object type or tenant.

## Consume an accepted snapshot

Build `registry/generated/prefix_ownership.json` from an explicitly selected
accepted revision. Its `ownership` mapping uses Meridian's existing
`(domain, prefix) -> issuer_app_code` contract. Only assigned prefix records
under assigned/reserved domains are exported. Reserved, retired, and disputed
prefix records remain in the source ledger but confer no issuance authority.

Pass the export through the client's existing explicit prefix-registry input.
Keep the existing domain-issuance authorization configuration: the public
availability index and runtime domain-policy metadata have different shapes
and are not interchangeable. Domain reservation rules still apply, including
M's existing LSMC policy.

Clients allocate locally after provisioning, without contacting GitHub for
each EUID. A snapshot reflects its accepted revision; later changes require
an explicit operator update. This is not an instant revocation mechanism.

The hosted prefix registry starts empty. Import existing grants only through
holder-approved PRs. Existing private authority remains in place until that
explicit adoption; missing records do not prove global historical absence.

## Other holder registries

A domain record may point to its holder's public registry using
`prefix_registry.mode: public` and an explicit URL. Private or undeclared
registries retain their existing modes and a null URL. Hosting here is optional.
