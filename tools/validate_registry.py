from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from registry_common import (
    ROOT,
    build_index_payload,
    canonical_json,
    domain_paths,
    pii_errors,
    read_json,
    string_content_errors,
    validate_domain_code,
)


def _json_path(error_path: object) -> str:
    parts = [str(part) for part in error_path]
    return "$" if not parts else "$." + ".".join(parts)


def load_schema(root: Path = ROOT) -> dict[str, Any]:
    schema_path = root / "schemas" / "domain.schema.json"
    schema = read_json(schema_path)
    if not isinstance(schema, dict):
        raise ValueError(f"{schema_path}: schema must be a JSON object")
    Draft202012Validator.check_schema(schema)
    return schema


def validate_domain_records(
    paths: list[Path],
    schema: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    records: list[dict[str, Any]] = []
    seen: dict[str, Path] = {}

    for path in sorted(paths, key=lambda item: item.name):
        try:
            data = read_json(path)
        except Exception as exc:
            errors.append(str(exc))
            continue

        if not isinstance(data, dict):
            errors.append(f"{path}: domain record must be a JSON object")
            continue

        for error in sorted(validator.iter_errors(data), key=lambda err: list(err.path)):
            errors.append(f"{path}: {_json_path(error.path)}: {error.message}")

        domain = data.get("domain")
        domain_error = validate_domain_code(domain)
        if domain_error:
            errors.append(f"{path}: {domain_error}")
        elif isinstance(domain, str):
            if path.stem != domain:
                errors.append(
                    f"{path}: filename {path.stem!r} must match domain field {domain!r}"
                )
            if domain in seen:
                errors.append(
                    f"{path}: duplicate domain {domain!r}; already defined in {seen[domain]}"
                )
            seen[domain] = path

        errors.extend(f"{path}: {message}" for message in string_content_errors(data))
        errors.extend(f"{path}: {message}" for message in pii_errors(data))
        records.append(data)

    return sorted(records, key=lambda record: record.get("domain", "")), errors


def validate_generated_index(root: Path, records: list[dict[str, Any]]) -> list[str]:
    index_path = root / "registry" / "generated" / "domains.json"
    if not index_path.is_file():
        return [f"{index_path}: generated index is missing; run python tools/build_index.py --stable"]

    expected = canonical_json(build_index_payload(records, stable=True))
    actual = index_path.read_text(encoding="utf-8")
    if actual != expected:
        return [
            f"{index_path}: generated index is stale or non-deterministic; "
            "run python tools/build_index.py --stable"
        ]
    return []


def validate_registry(root: Path = ROOT) -> list[str]:
    schema = load_schema(root)
    records, errors = validate_domain_records(domain_paths(root), schema)
    if not errors:
        errors.extend(validate_generated_index(root, records))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Meridian domain registry.")
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="registry repository root",
    )
    args = parser.parse_args(argv)

    try:
        errors = validate_registry(args.root.resolve())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print("registry validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
