from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from validate_registry import load_schema, validate_domain_records, validate_registry  # noqa: E402


def _read_domain(domain: str) -> dict[str, object]:
    return json.loads((ROOT / "registry" / "domains" / f"{domain}.json").read_text())


def _write_record(path: Path, record: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")


def _valid_record(domain: str = "Q") -> dict[str, object]:
    record = copy.deepcopy(_read_domain("D"))
    record["domain"] = domain
    record["holder"] = {
        "visibility": "public",
        "public_label": "Example Holder",
        "holder_ref": "org_example_holder",
    }
    record["notes"] = "Test registry record."
    return record


def _validate_paths(paths: list[Path]) -> list[str]:
    schema = load_schema(ROOT)
    _, errors = validate_domain_records(paths, schema)
    return errors


def test_initial_registry_validates() -> None:
    assert validate_registry(ROOT) == []


def test_initial_records_present() -> None:
    domains = {
        path.stem
        for path in (ROOT / "registry" / "domains").glob("*.json")
    }
    assert {"Z", "M", "N", "D", "F", "A", "W", "X", "Y"} == domains


def test_generated_index_is_sorted() -> None:
    data = json.loads((ROOT / "registry" / "generated" / "domains.json").read_text())
    domains = [record["domain"] for record in data["domains"]]
    assert domains == sorted(domains)
    assert data["domain_count"] == len(domains) == 9
    assert data["generated_at"] == "1970-01-01T00:00:00Z"


def test_duplicate_domains_fail(tmp_path: Path) -> None:
    first = _valid_record("Q")
    second = _valid_record("Q")
    path_a = tmp_path / "a" / "Q.json"
    path_b = tmp_path / "b" / "Q.json"
    _write_record(path_a, first)
    _write_record(path_b, second)

    errors = _validate_paths([path_a, path_b])

    assert any("duplicate domain 'Q'" in error for error in errors)


def test_filename_domain_mismatch_fails(tmp_path: Path) -> None:
    path = tmp_path / "R.json"
    _write_record(path, _valid_record("Q"))

    errors = _validate_paths([path])

    assert any("filename 'R' must match domain field 'Q'" in error for error in errors)


def test_invalid_characters_fail_using_meridian_rules(tmp_path: Path) -> None:
    path = tmp_path / "O.json"
    _write_record(path, _valid_record("O"))

    errors = _validate_paths([path])

    assert any("forbidden Meridian character" in error for error in errors)


def test_check_domain_reports_assigned_holder() -> None:
    result = subprocess.run(
        [sys.executable, "tools/check_domain.py", "D"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "D is assigned to Daylily Informatics." in result.stdout


def test_check_domain_reports_reserved_holders_and_purpose() -> None:
    expected = {
        "M": "reserved for LSMC",
        "N": "reserved for LSMC",
        "F": "reserved for Inflection",
        "Z": "testing, examples, development",
    }
    for domain, text in expected.items():
        result = subprocess.run(
            [sys.executable, "tools/check_domain.py", domain],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert text in result.stdout


def test_check_domain_reports_available_for_valid_unassigned_q() -> None:
    result = subprocess.run(
        [sys.executable, "tools/check_domain.py", "Q"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Q is available." in result.stdout


def test_check_domain_rejects_invalid_input() -> None:
    result = subprocess.run(
        [sys.executable, "tools/check_domain.py", "o"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "lowercase is not permitted" in result.stdout


def test_private_holder_records_use_only_pseudonymous_public_identity(tmp_path: Path) -> None:
    private_record = _valid_record("Q")
    private_record["assignment_type"] = "private_owner"
    private_record["holder"] = {
        "visibility": "private",
        "public_label": None,
        "holder_ref": "holder_7FQ3M2",
    }
    private_path = tmp_path / "Q.json"
    _write_record(private_path, private_record)
    assert _validate_paths([private_path]) == []

    exposing_record = copy.deepcopy(private_record)
    exposing_record["holder"] = {
        "visibility": "private",
        "public_label": "Secret Holder",
        "holder_ref": "holder_7FQ3M2",
    }
    exposing_path = tmp_path / "R.json"
    exposing_record["domain"] = "R"
    _write_record(exposing_path, exposing_record)

    errors = _validate_paths([exposing_path])

    assert any(
        "public_label" in error and "not of type 'null'" in error
        for error in errors
    )


def test_public_prefix_registry_mode_requires_url(tmp_path: Path) -> None:
    record = _valid_record("Q")
    record["prefix_registry"] = {"mode": "public", "url": None}
    path = tmp_path / "Q.json"
    _write_record(path, record)

    errors = _validate_paths([path])

    assert any("url" in error and "None is not of type 'string'" in error for error in errors)


def test_non_public_prefix_registry_mode_requires_null_url(tmp_path: Path) -> None:
    record = _valid_record("Q")
    record["prefix_registry"] = {
        "mode": "private",
        "url": "https://example.org/private-prefixes.json",
    }
    path = tmp_path / "Q.json"
    _write_record(path, record)

    errors = _validate_paths([path])

    assert any("url" in error and "None was expected" in error for error in errors)


def test_no_raw_email_phone_or_postal_address_in_public_json(tmp_path: Path) -> None:
    cases = [
        ("Q", "Contact person@example.org."),
        ("R", "Call 555-123-4567."),
        ("S", "Mail 123 Main Street."),
    ]
    paths = []
    for domain, note in cases:
        record = _valid_record(domain)
        record["notes"] = note
        path = tmp_path / f"{domain}.json"
        _write_record(path, record)
        paths.append(path)

    errors = _validate_paths(paths)

    assert any("raw email address" in error for error in errors)
    assert any("raw phone number" in error for error in errors)
    assert any("raw postal address" in error for error in errors)
