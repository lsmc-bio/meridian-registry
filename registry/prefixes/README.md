# Prefix requests and assignments

One JSON record per `DOMAIN/PREFIX`, stored as `<DOMAIN>/<PREFIX>.json`.
The four fields are `domain`, `prefix`, `issuer_app_code`, and `status`.

An assignment takes effect only after domain-holder approval and merge into
`main`. A request branch, tag, local file, or open PR is not a grant.
Reserved, retired, and disputed records remain here and are never available
for unrelated reuse. Only assigned records are included in the generated
ownership export.

This directory starts without imported client assignments. Existing private
grants remain with their current authority until the holder explicitly adopts
this registry. Absence here does not prove historical availability elsewhere.

See [the prefix guide](../../docs/prefix-registries.md) for the request process.
