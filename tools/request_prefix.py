"""Prepare one prefix request locally. This does not grant or publish anything."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from registry_common import ROOT, canonical_json, load_records, validate_prefix_record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("domain")
    parser.add_argument("prefix")
    parser.add_argument("--issuer-app-code", required=True)
    parser.add_argument("--status", choices=("reserved", "assigned"), required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    record = {
        "domain": args.domain,
        "prefix": args.prefix,
        "issuer_app_code": args.issuer_app_code,
        "status": args.status,
    }
    try:
        domains = {item["domain"]: item for item in load_records(root)}
        validate_prefix_record(record, domains)
        if domains[args.domain]["status"] not in {"assigned", "reserved"}:
            raise ValueError("cannot request a prefix under a retired or disputed domain")
        path = root / "registry" / "prefixes" / args.domain / f"{args.prefix}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as handle:
            handle.write(canonical_json(record))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"Prepared request: {path}")
    print("Rebuild indexes and open a PR to main. This local file grants no assignment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
