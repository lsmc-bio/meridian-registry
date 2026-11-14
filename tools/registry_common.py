from __future__ import annotations

from datetime import UTC, datetime
import json
import re
from pathlib import Path
from typing import Any

ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
FORBIDDEN = frozenset("ILOU")
REGISTRY_VERSION = "0.1.1"
STABLE_GENERATED_AT = "1970-01-01T00:00:00Z"

ROOT = Path(__file__).resolve().parents[1]
DOMAIN_DIR = ROOT / "registry" / "domains"
GENERATED_INDEX = ROOT / "registry" / "generated" / "domains.json"
SCHEMA_PATH = ROOT / "schemas" / "domain.schema.json"

_LOWERCASE_RE = re.compile(r"[a-z]")
_ISSUER_RE = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
PREFIX_STATUSES = frozenset({"reserved", "assigned", "retired", "disputed"})
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d .()/-]{7,}\d)(?!\w)")
_POSTAL_RE = re.compile(
    r"\b\d{1,6}\s+[A-Za-z0-9 .'-]+\s+"
    r"(?:Street|St\.?|Avenue|Ave\.?|Road|Rd\.?|Boulevard|Blvd\.?|"
    r"Lane|Ln\.?|Drive|Dr\.?|Court|Ct\.?)\b",
    re.IGNORECASE,
)
_ISO_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def canonical_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc


def write_json(path: Path, data: Any) -> None:
    path.write_text(canonical_json(data), encoding="utf-8")


def domain_paths(root: Path = ROOT) -> list[Path]:
    domain_dir = root / "registry" / "domains"
    if not domain_dir.is_dir():
        raise ValueError(f"missing domain directory: {domain_dir}")
    return sorted(domain_dir.glob("*.json"), key=lambda path: path.name)


def validate_domain_code(code: Any) -> str | None:
    if not isinstance(code, str):
        return "domain must be a string"
    if code != code.strip():
        return "domain must not have leading or trailing whitespace"
    if not code:
        return "domain must be 1-4 characters"
    if not code.isascii():
        return "domain must be ASCII"
    if _LOWERCASE_RE.search(code):
        return "domain must be uppercase; lowercase is not permitted"
    if not (1 <= len(code) <= 4):
        return "domain must be 1-4 characters"
    invalid = sorted({ch for ch in code if ch not in ALPHABET})
    if invalid:
        forbidden = sorted(set(invalid) & FORBIDDEN)
        if forbidden:
            return (
                "domain contains forbidden Meridian character(s) "
                f"{', '.join(forbidden)}; forbidden characters are I, L, O, U"
            )
        return (
            "domain must use Meridian Crockford Base32 alphabet "
            f"{ALPHABET}; invalid character(s): {', '.join(invalid)}"
        )
    return None


def walk_strings(value: Any, path: str = "$") -> list[tuple[str, str]]:
    if isinstance(value, str):
        return [(path, value)]
    if isinstance(value, list):
        found: list[tuple[str, str]] = []
        for index, item in enumerate(value):
            found.extend(walk_strings(item, f"{path}[{index}]"))
        return found
    if isinstance(value, dict):
        found = []
        for key, item in value.items():
            found.extend(walk_strings(item, f"{path}.{key}"))
        return found
    return []


def string_content_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for path, text in walk_strings(record):
        if text != text.strip():
            errors.append(f"{path}: string must not have leading or trailing whitespace")
    return errors


def pii_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for path, text in walk_strings(record):
        if _EMAIL_RE.search(text):
            errors.append(f"{path}: raw email address is not allowed in public JSON")
        for match in _PHONE_RE.finditer(text):
            candidate = match.group(0)
            if not _ISO_DATE_RE.fullmatch(candidate):
                errors.append(f"{path}: raw phone number is not allowed in public JSON")
                break
        if _POSTAL_RE.search(text):
            errors.append(f"{path}: raw postal address is not allowed in public JSON")
    return errors


def build_index_payload(records: list[dict[str, Any]], *, stable: bool) -> dict[str, Any]:
    sorted_records = sorted(records, key=lambda record: record["domain"])
    generated_at = (
        STABLE_GENERATED_AT
        if stable
        else datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    return {
        "generated_at": generated_at,
        "registry_version": REGISTRY_VERSION,
        "domain_count": len(sorted_records),
        "domains": sorted_records,
    }


def load_records(root: Path = ROOT) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in domain_paths(root):
        data = read_json(path)
        if not isinstance(data, dict):
            raise ValueError(f"{path}: domain record must be a JSON object")
        domain = data.get("domain")
        error = validate_domain_code(domain)
        if error:
            raise ValueError(f"{path}: {error}")
        if path.stem != domain:
            raise ValueError(f"{path}: filename {path.stem!r} must match domain {domain!r}")
        records.append(data)
    return sorted(records, key=lambda record: record["domain"])


def validate_prefix_record(record: Any, domains: dict[str, dict[str, Any]]) -> None:
    """Validate the small prefix-request contract; approval remains a main PR."""
    fields = {"domain", "prefix", "issuer_app_code", "status"}
    if not isinstance(record, dict) or set(record) != fields:
        raise ValueError("prefix record requires exactly: " + ", ".join(sorted(fields)))
    for field in ("domain", "prefix"):
        error = validate_domain_code(record[field])
        if error:
            raise ValueError(f"{field}: {error}")
    domain = domains.get(record["domain"])
    if domain is None or domain.get("prefix_authority") != "domain_holder":
        raise ValueError("prefix requires a registered domain with domain-holder authority")
    owner = record["issuer_app_code"]
    if not isinstance(owner, str) or not _ISSUER_RE.fullmatch(owner):
        raise ValueError("issuer_app_code must be an exact lowercase governance token")
    if not isinstance(record["status"], str) or record["status"] not in PREFIX_STATUSES:
        raise ValueError("prefix status must be reserved, assigned, retired, or disputed")


def load_prefix_records(root: Path, domains: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prefix_dir = root / "registry" / "prefixes"
    if not prefix_dir.is_dir():
        raise ValueError(f"missing prefix directory: {prefix_dir}")
    by_domain = {record["domain"]: record for record in domains}
    records = []
    for path in sorted(prefix_dir.glob("*/*.json")):
        record = read_json(path)
        validate_prefix_record(record, by_domain)
        if (path.parent.name, path.stem) != (record["domain"], record["prefix"]):
            raise ValueError(f"{path}: path must match the record's domain and prefix")
        records.append(record)
    return records


def build_prefix_ownership_payload(
    records: list[dict[str, Any]], domains: list[dict[str, Any]]
) -> dict[str, Any]:
    """Export only assigned prefixes under issuable domain states for Meridian."""
    domain_states = {record["domain"]: record["status"] for record in domains}
    ownership: dict[str, dict[str, dict[str, str]]] = {}
    for record in records:
        if record["status"] != "assigned":
            continue
        if domain_states[record["domain"]] not in {"assigned", "reserved"}:
            continue
        ownership.setdefault(record["domain"], {})[record["prefix"]] = {
            "issuer_app_code": record["issuer_app_code"]
        }
    return {"version": "1", "ownership": ownership}
