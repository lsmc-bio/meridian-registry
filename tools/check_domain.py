from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

from registry_common import GENERATED_INDEX, ROOT, read_json, validate_domain_code


def _load_index(root: Path) -> dict[str, dict[str, Any]]:
    index_path = root / "registry" / "generated" / "domains.json"
    if not index_path.is_file():
        raise ValueError(f"generated index is missing: {index_path}")
    data = read_json(index_path)
    if not isinstance(data, dict) or not isinstance(data.get("domains"), list):
        raise ValueError(f"generated index has invalid shape: {index_path}")
    records: dict[str, dict[str, Any]] = {}
    for item in data["domains"]:
        if not isinstance(item, dict) or not isinstance(item.get("domain"), str):
            raise ValueError(f"generated index contains an invalid domain record: {index_path}")
        records[item["domain"]] = item
    return records


def describe_record(domain: str, record: dict[str, Any]) -> str:
    status = record.get("status")
    holder = record.get("holder")
    holder_visibility = holder.get("visibility") if isinstance(holder, dict) else None
    public_label = holder.get("public_label") if isinstance(holder, dict) else None
    notes = record.get("notes")

    if status == "assigned":
        if holder_visibility == "private":
            return f"{domain} is assigned, holder private."
        if isinstance(public_label, str):
            return f"{domain} is assigned to {public_label}."
        return f"{domain} is assigned."

    if status == "reserved":
        if isinstance(public_label, str) and public_label != "Meridian Registry":
            return f"{domain} is reserved for {public_label}."
        if isinstance(notes, str):
            return f"{domain} is reserved: {notes}"
        return f"{domain} is reserved."

    if status == "retired":
        return f"{domain} is retired and unavailable."
    if status == "disputed":
        return f"{domain} is disputed and unavailable."
    raise ValueError(f"domain {domain!r} has unknown status {status!r} in {GENERATED_INDEX}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check Meridian domain availability.")
    parser.add_argument("domain", help="domain code to check")
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="registry repository root",
    )
    args = parser.parse_args(argv)

    domain_error = validate_domain_code(args.domain)
    if domain_error:
        print(f"invalid domain {args.domain!r}: {domain_error}")
        return 2

    try:
        records = _load_index(args.root.resolve())
        record = records.get(args.domain)
    except Exception as exc:
        print(f"registry error: {exc}", file=sys.stderr)
        return 2

    if record is None:
        print(f"{args.domain} is available.")
        return 0

    print(describe_record(args.domain, record))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
