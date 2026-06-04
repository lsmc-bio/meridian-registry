# Contributing

## Add Or Change A Domain

1. Add or edit one source record under `registry/domains/<DOMAIN>.json`.
2. Keep `<DOMAIN>.json` exactly matched to the record's `domain` field.
3. Do not include personal data in public registry files.
4. Rebuild the generated index:

```bash
python tools/build_index.py --stable
```

5. Validate and test:

```bash
python tools/validate_registry.py
python -m pytest
git diff --exit-code
```

## Pull Request Requirements

Pull requests should include:

- The domain JSON source record.
- The regenerated `registry/generated/domains.json`.
- A clear claim rationale.
- Any public prefix-registry URL, if the holder chooses to publish one.

Maintainers review claim validity, conflict risk, schema compliance, and privacy compliance.

## Privacy

Do not commit raw emails, phone numbers, postal addresses, or private holder identity mappings. For private claims, use a pseudonymous `holder_ref` such as `holder_7FQ3M2` and keep the private mapping outside this repository.
