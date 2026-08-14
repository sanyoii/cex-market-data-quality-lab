import ast
import inspect
import re
from pathlib import Path

from cex_quality.rest_client import MarketDataRestClient
from cex_quality.websocket_client import collect_book_tickers, synchronize_live_depth


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_every_requirement_is_present_in_the_traceability_matrix():
    requirement_ids = set(
        re.findall(
            r"^\| (REQ-[A-Z]+-\d+) \|",
            _read("docs/requirements.md"),
            re.MULTILINE,
        )
    )
    mapped_ids = set(
        re.findall(
            r"^\| (REQ-[A-Z]+-\d+) \|",
            _read("docs/traceability-matrix.md"),
            re.MULTILINE,
        )
    )

    assert mapped_ids == requirement_ids


def test_every_logical_case_maps_to_an_existing_pytest_function():
    case_ids = set(
        re.findall(
            r"^\| ((?:OB|REST|WS|LIVE|DOC)-[A-Z0-9-]+) \|",
            _read("docs/test-cases.md"),
            re.MULTILINE,
        )
    )
    automation_map = _read("docs/automation-map.md")
    mapped_case_ids = set(
        re.findall(r"\b(?:OB|REST|WS|LIVE|DOC)-[A-Z0-9-]+\b", automation_map)
    )

    assert mapped_case_ids == case_ids

    script_references = re.findall(
        r"`(tests/[^`]+\.py)::(test_[A-Za-z0-9_]+)`",
        automation_map,
    )
    assert script_references
    for relative_path, function_name in script_references:
        script_path = ROOT / relative_path
        assert script_path.is_file(), relative_path
        tree = ast.parse(script_path.read_text(encoding="utf-8"))
        defined_functions = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assert function_name in defined_functions, f"{relative_path}::{function_name}"


def test_all_relative_markdown_links_resolve():
    missing = []
    for markdown_path in ROOT.rglob("*.md"):
        text = markdown_path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative_target = target.split("#", maxsplit=1)[0]
            if relative_target and not (markdown_path.parent / relative_target).resolve().exists():
                missing.append(f"{markdown_path.relative_to(ROOT)} -> {target}")

    assert not missing, "\n".join(missing)


def test_public_scope_uses_only_allowlisted_market_data_interfaces():
    rest_source = _read("src/cex_quality/rest_client.py")
    endpoint_paths = set(re.findall(r'"(/api/v3/[^"?]+)"', rest_source))
    assert endpoint_paths == {
        "/api/v3/depth",
        "/api/v3/exchangeInfo",
        "/api/v3/ticker/bookTicker",
    }

    assert inspect.signature(MarketDataRestClient).parameters["base_url"].default == (
        "https://data-api.binance.vision"
    )
    assert inspect.signature(collect_book_tickers).parameters["base_url"].default == (
        "wss://data-stream.binance.vision"
    )
    assert inspect.signature(synchronize_live_depth).parameters["base_url"].default == (
        "wss://data-stream.binance.vision"
    )

    audited_paths = [
        *ROOT.glob("src/**/*.py"),
        *ROOT.glob("tests/unit/**/*.py"),
        *ROOT.glob("tests/contract/**/*.py"),
        *ROOT.glob("tests/live/**/*.py"),
        ROOT / ".github/workflows/tests.yml",
    ]
    audited_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in audited_paths)
    forbidden_fragments = (
        "/api/v3/account",
        "/api/v3/order",
        "api_key",
        "secret_key",
        "authorization:",
        "${{ secrets.",
    )
    assert all(fragment not in audited_text for fragment in forbidden_fragments)
