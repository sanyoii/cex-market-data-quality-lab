# Exploratory Test Charters

Status: Designed, not executed. No human exploratory test evidence exists for these charters.

These charters complement the automated suites. An exploratory session requires a named tester, a time box, contemporaneous notes, observed results, and a dated evidence record. Safe fault injection replaces intentional load or disruption of public services. Every starter below uses `.invalid` or an injected fake; it must not make a network call.

## Shared setup

Run from `cex-market-data-quality-lab/` with Git Bash. The existing virtual environment and package are prerequisites:

```bash
PYTHONPATH=src .venv/Scripts/python.exe - <<'PY'
print("offline exploratory session ready")
PY
```

Before each charter, record the full SHA, branch, worktree state, tester, UTC start/end, time box, command, stdout/stderr, and observed classification. `Pass` means the declared contract was observed; an injected exception is an observation to classify, not automatic product failure. The existing source and test entry points are listed for each charter so the starter can be compared with the maintained interfaces.

| Charter | Focus | Existing setup and exact entry points | Starter scope | Remaining probes | Stop condition | Required evidence |
|---|---|---|---|---|---|---|
| EXP-001 | REST and WebSocket schema drift | `src/cex_quality/rest_client.py`; `src/cex_quality/websocket_client.py`; `tests/contract/test_rest_contract.py`; `tests/contract/test_websocket_contract.py` | Run one valid and one mutated REST payload plus one valid and one mutated WebSocket payload through existing parsers. | Remove each required field, change object types and numeric encodings, add unknown fields, and compare exception wording／classification. | Each public parser path has one valid and one changed payload recorded. | Payload label, parser result or exception, notes, start／end UTC. |
| EXP-002 | Disconnect and resynchronization behavior | `src/cex_quality/websocket_client.py::synchronize_live_depth`; `tests/contract/test_websocket_contract.py::test_live_depth_sync_discards_stale_buffered_events_and_applies_continuous_updates` and `FakeConnection` helpers | Inject disconnect before snapshot and after the first event has been applied; record that local state is unavailable. | Extend separately for a pre-apply buffer disconnect and teardown disconnect; inspect whether the caller exposes a safe recovery decision. | Each exercised boundary has an observed state and an explicit recovery requirement. | Fault phase, local state availability, exception, recovery decision, no-recovery-claim note. |
| EXP-003 | Symbol and filter boundaries | `src/cex_quality/rest_client.py::MarketDataRestClient.exchange_info`; `tests/contract/test_rest_contract.py::test_exchange_info_returns_requested_trading_symbol_and_filters` and `test_exchange_info_requires_exactly_one_symbol` | Use `httpx.MockTransport` with valid, missing-filter, and multiple-symbol payloads. | Zero symbols, unknown filters, lowercase caller input, wrong symbol in the returned item, and filter retention. | Cardinality and filter behavior are recorded for every injected payload. | Fixture label, requested symbol, result or exception, discrepancy notes. |
| EXP-004 | Rate-limit and network-policy responses | `src/cex_quality/rest_client.py`; `src/cex_quality/websocket_client.py`; `tests/contract/test_rest_contract.py::test_rest_transport_timeout_remains_diagnosable`; `tests/contract/test_websocket_contract.py::test_subscription_receive_timeout_is_bounded` | Inject HTTP 418／429, timeout, DNS-like `ConnectError`, WebSocket close, and WebSocket timeout without network. | Verify error preservation, bounded exit, retry classification, cleanup, and evidence wording for each signal. | Every injected infrastructure category has a recorded outcome and retry decision. | Injected signal, elapsed time, exception, classification, retry count, cleanup result. |

## EXP-001 starter — REST + WebSocket valid/mutated payloads

```bash
PYTHONPATH=src .venv/Scripts/python.exe - <<'PY'
import httpx
from cex_quality.rest_client import MarketDataRestClient
from cex_quality.websocket_client import BookTickerEvent

rest_payload = {"symbol": "BTCUSDT", "bidPrice": "100", "bidQty": "2", "askPrice": "101", "askQty": "3"}
def handler(request):
    return httpx.Response(200, json=rest_payload)

def observe(label, action):
    try:
        print(label, "OK", action())
    except Exception as exc:
        print(label, type(exc).__name__, str(exc))

with MarketDataRestClient(base_url="https://market-data.invalid", transport=httpx.MockTransport(handler)) as client:
    observe("REST valid", lambda: client.book_ticker("BTCUSDT"))
    rest_payload.pop("askQty")
    observe("REST missing askQty", lambda: client.book_ticker("BTCUSDT"))

valid_event = {"u": 1, "s": "BTCUSDT", "b": "100", "B": "2", "a": "101", "A": "3"}
observe("WS valid", lambda: BookTickerEvent.from_payload(valid_event, "BTCUSDT"))
mutated_event = {**valid_event, "A": 0}
observe("WS non-positive quantity", lambda: BookTickerEvent.from_payload(mutated_event, "BTCUSDT"))
PY
```

Declared expected output: `REST valid` is `OK` with `symbol='BTCUSDT'`; `REST missing askQty` is `RestContractError: bookTicker response has invalid schema`; `WS valid` is `OK`; and `WS non-positive quantity` is `WebSocketContractError: prices and quantities must be positive`. The output is only a starter observation. Continue with the listed missing fields, type changes, numeric encodings, and unknown fields; do not infer full schema coverage from these four observations.

## EXP-002 starter — injected disconnect phases

```bash
PYTHONPATH=src .venv/Scripts/python.exe - <<'PY'
import asyncio
import json
from tests.contract.test_websocket_contract import FakeConnectionContext
from cex_quality.websocket_client import synchronize_live_depth

class Disconnect:
    def __init__(self, phase): self.phase, self.recv_calls = phase, 0
    async def recv(self):
        self.recv_calls += 1
        if self.phase == "after_first_applied_event" and self.recv_calls == 1:
            return json.dumps({"U": 101, "u": 101, "b": [["100", "2"]], "a": []})
        raise ConnectionError(f"injected disconnect: {self.phase}")

class FakeRest:
    def __init__(self): self.calls = 0
    def depth_snapshot(self, symbol, limit):
        self.calls += 1
        return {"lastUpdateId": 100, "bids": [["100", "2"]], "asks": [["101", "3"]]}

async def run(phase):
    connection = Disconnect(phase)
    rest = FakeRest()
    try:
        await synchronize_live_depth(
            "BTCUSDT", rest_client=rest,
            connect=lambda url: FakeConnectionContext(connection),
        )
    except Exception as exc:
        print(phase, type(exc).__name__, str(exc), f"rest_calls={rest.calls}", f"recv_calls={connection.recv_calls}", "local_state=unavailable", "recovery_claim=none")

asyncio.run(run("before_snapshot"))
asyncio.run(run("after_first_applied_event"))
PY
```

Declared expected output: `before_snapshot` raises `ConnectionError` with `rest_calls=0`, `recv_calls=1`; `after_first_applied_event` returns one event, calls the fake REST snapshot once, applies that event, then raises `ConnectionError` on the next receive with `rest_calls=1`, `recv_calls=2`. Both remain `local_state=unavailable` and `recovery_claim=none`. This starter proves only that injected failures are observable. Extend the fake connection separately for a pre-apply buffer disconnect and teardown; do not call a live endpoint or label recovery supported without an explicit observed contract.

## EXP-003 starter — symbol and filter mutation

```bash
PYTHONPATH=src .venv/Scripts/python.exe - <<'PY'
import httpx
from cex_quality.rest_client import MarketDataRestClient

fixtures = [
    ("valid", {"symbols": [{"symbol": "BTCUSDT", "status": "TRADING", "filters": [{"filterType": "PRICE_FILTER"}]}]}),
    ("missing_filters", {"symbols": [{"symbol": "BTCUSDT", "status": "TRADING"}]}),
    ("multiple_symbols", {"symbols": [{"symbol": "BTCUSDT"}, {"symbol": "ETHUSDT"}]}),
]
for label, payload in fixtures:
    with MarketDataRestClient(
        base_url="https://market-data.invalid",
        transport=httpx.MockTransport(lambda request, payload=payload: httpx.Response(200, json=payload)),
    ) as client:
        try:
            print(label, client.exchange_info("btcusdt"))
        except Exception as exc:
            print(label, type(exc).__name__, str(exc))
PY
```

Declared expected output: `valid` returns one `SymbolInfo` with `BTCUSDT`, `TRADING`, and `('PRICE_FILTER',)`; `missing_filters` is accepted by the current parser and returns an empty filter tuple, which is a finding to classify rather than a rejection; `multiple_symbols` raises `RestContractError: exchangeInfo must return exactly one symbol`. Continue with zero symbols, unknown filters, lowercase input, and a returned symbol mismatch; record whether each is accepted, rejected, or leaves a coverage gap.

## EXP-004 starter — HTTP and WebSocket infrastructure faults

```bash
PYTHONPATH=src .venv/Scripts/python.exe - <<'PY'
import asyncio
import httpx
import time
from tests.contract.test_websocket_contract import FakeConnectionContext
from cex_quality.rest_client import MarketDataRestClient
from cex_quality.websocket_client import collect_book_tickers

def observe_http(label, outcome):
    def handler(request):
        if isinstance(outcome, Exception): raise outcome
        return httpx.Response(outcome, json={"code": outcome, "msg": label})
    try:
        with MarketDataRestClient(base_url="https://market-data.invalid", transport=httpx.MockTransport(handler)) as client:
            client.book_ticker("BTCUSDT")
    except Exception as exc:
        print(label, type(exc).__name__, str(exc))

observe_http("http_418", 418)
observe_http("http_429", 429)
observe_http("timeout", httpx.ReadTimeout("injected timeout"))
observe_http("dns_like", httpx.ConnectError("injected DNS-like failure"))

class Close:
    async def send(self, message): pass
    async def recv(self): raise ConnectionError("injected websocket close")

class Slow:
    async def send(self, message): pass
    async def recv(self):
        await asyncio.sleep(1)

async def ws(label, connection):
    started = time.perf_counter()
    try:
        await collect_book_tickers("BTCUSDT", timeout=0.01, connect=lambda url: FakeConnectionContext(connection))
    except Exception as exc:
        print(label, type(exc).__name__, str(exc), f"elapsed={time.perf_counter() - started:.3f}s")

asyncio.run(ws("ws_close", Close()))
asyncio.run(ws("ws_timeout", Slow()))
PY
```

Declared expected output: HTTP 418/429 produce `ApiError` with the matching status; the `code` and `msg` in those responses are synthetic fixture values, not Binance observations. The HTTP timeout and DNS-like cases preserve `ReadTimeout` and `ConnectError`; `ws_close` produces `ConnectionError`; `ws_timeout` produces `TimeoutError` with elapsed time near the declared 0.01-second bound. The starter records bounded error observations only. Continue by checking retry count, cleanup, and evidence classification for each injected category; it does not prove public rate-limit behavior or production reconnect behavior.

## Safety boundary

- Do not send load, burst traffic, destructive payloads, authenticated requests, orders, or account operations.
- Do not treat a simulated fault as proof of current public-service behavior.
- Do not mark a charter Passed without a completed session record.
