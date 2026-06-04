# Prefix Registries

Prefix governance belongs to the domain holder.

This registry may list a holder's public prefix-registry URL with:

```json
{
  "prefix_registry": {
    "mode": "public",
    "url": "https://example.org/meridian-prefixes.json"
  }
}
```

If `prefix_registry.mode` is `private` or `none_declared`, the URL must be `null`.

Private prefix governance is allowed. Undeclared prefix governance is allowed. This repository does not approve or validate prefix assignments below a domain.

Software must not treat domain or prefix strings as authoritative object type, workflow, assay, clinical, or business meaning.
