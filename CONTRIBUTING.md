# Request a domain or prefix

**Open a pull request targeting `main`.** This covers new assignments, reserved
domains/prefixes, activation, transfers, and retirement. Discussion issues do
not grant or reserve names.

1. Start a working branch from current `main`.
2. Add or edit the exact source record:
   - Domain: `registry/domains/<DOMAIN>.json`, following the domain schema.
   - Prefix: `registry/prefixes/<DOMAIN>/<PREFIX>.json`, following the
     [four-field contract](docs/prefix-registries.md).
3. Explain the requested owner and purpose in the PR. Reserved namespaces need
   approval from their current authority. Prefixes need domain-holder approval.
4. Regenerate the committed outputs:

```bash
python tools/build_index.py --stable
```

5. Include source records and generated outputs in the PR to `main`. Existing
   repository checks and maintainer review apply. Do not resolve conflicts by
   overwriting another assignment.

Only an authorized merge into `main` makes the assignment effective. Git
history records its provenance. Retired records remain permanently; domains
and prefixes are not recycled for unrelated identities.

The optional `tools/request_prefix.py` helper prepares a new prefix request
without publishing or granting it. See the [prefix guide](docs/prefix-registries.md).

## Public records

Use public organization labels or pseudonymous holder/issuer tokens. Do not
commit personal information, private holder mappings, internal endpoints,
credentials, tenant details, or object inventories. Private holder mappings
remain outside this public repository.
