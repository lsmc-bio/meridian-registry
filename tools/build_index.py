from __future__ import annotations

import argparse
from pathlib import Path
import sys

from registry_common import ROOT, build_index_payload, load_records, write_json


def build_index(root: Path = ROOT, *, stable: bool = False) -> dict[str, object]:
    records = load_records(root)
    payload = build_index_payload(records, stable=stable)
    write_json(root / "registry" / "generated" / "domains.json", payload)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Meridian domain index.")
    parser.add_argument(
        "--stable",
        action="store_true",
        help="use the stable generated_at placeholder for committed output",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="registry repository root",
    )
    args = parser.parse_args(argv)

    try:
        payload = build_index(args.root.resolve(), stable=args.stable)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(
        "wrote registry/generated/domains.json "
        f"with {payload['domain_count']} domains"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
