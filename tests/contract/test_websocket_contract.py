import asyncio
import json
from decimal import Decimal

import pytest

from cex_quality.websocket_client import (
    WebSocketContractError,
    collect_book_tickers,
    synchronize_live_depth,
)


class FakeConnection:
    def __init__(self, messages):
        self.messages = [json.dumps(message) for message in messages]
        self.sent = []

    async def send(self, message):
        self.sent.append(json.loads(message))

    async def recv(self):
        return self.messages.pop(0)


class RawConnection(FakeConnection):
    def __init__(self, messages):
        self.messages = messages
        self.sent = []


class FakeConnectionContext:
    def __init__(self, connection):
        self.connection = connection

    async def __aenter__(self):
        return self.connection

    async def __aexit__(self, *exc_info):
        return None


@pytest.mark.asyncio
async def test_collect_book_tickers_subscribes_validates_and_unsubscribes():
    connection = FakeConnection(
        [
            {"result": None, "id": 1},
            {
                "u": 101,
                "s": "BTCUSDT",
                "b": "100.10",
                "B": "2.5",
                "a": "100.20",
                "A": "3.5",
            },
            {"result": None, "id": 2},
        ]
    )

    events = await collect_book_tickers(
        "btcusdt",
        count=1,
        connect=lambda url: FakeConnectionContext(connection),
    )

    assert len(events) == 1
    assert events[0].symbol == "BTCUSDT"
    assert events[0].bid_price == Decimal("100.10")
    assert events[0].ask_price == Decimal("100.20")
    assert connection.sent == [
        {"method": "SUBSCRIBE", "params": ["btcusdt@bookTicker"], "id": 1},
        {"method": "UNSUBSCRIBE", "params": ["btcusdt@bookTicker"], "id": 2},
    ]


@pytest.mark.asyncio
async def test_collect_book_tickers_rejects_decreasing_update_ids():
    connection = FakeConnection(
        [
            {"result": None, "id": 1},
            {"u": 102, "s": "BTCUSDT", "b": "100", "B": "2", "a": "101", "A": "3"},
            {"u": 101, "s": "BTCUSDT", "b": "100", "B": "2", "a": "101", "A": "3"},
        ]
    )

    with pytest.raises(WebSocketContractError, match="update ID decreased from 102 to 101"):
        await collect_book_tickers(
            "BTCUSDT",
            count=2,
            connect=lambda url: FakeConnectionContext(connection),
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "event, message",
    [
        (
            {"u": 101, "s": "ETHUSDT", "b": "100", "B": "2", "a": "101", "A": "3"},
            "expected symbol BTCUSDT, received ETHUSDT",
        ),
        (
            {"u": 101, "s": "BTCUSDT", "b": "100", "B": "0", "a": "101", "A": "3"},
            "prices and quantities must be positive",
        ),
        (
            {"u": 101, "s": "BTCUSDT", "b": "102", "B": "2", "a": "101", "A": "3"},
            "best bid exceeds best ask",
        ),
    ],
)
async def test_collect_book_tickers_rejects_invalid_market_events(event, message):
    connection = FakeConnection([{"result": None, "id": 1}, event])

    with pytest.raises(WebSocketContractError, match=message):
        await collect_book_tickers(
            "BTCUSDT",
            count=1,
            connect=lambda url: FakeConnectionContext(connection),
        )


@pytest.mark.asyncio
async def test_collect_book_tickers_rejects_invalid_subscription_acknowledgment():
    connection = FakeConnection([{"result": None, "id": 99}])

    with pytest.raises(WebSocketContractError, match="invalid acknowledgment"):
        await collect_book_tickers(
            "BTCUSDT",
            count=1,
            connect=lambda url: FakeConnectionContext(connection),
        )


@pytest.mark.asyncio
async def test_unsubscribe_waits_past_in_flight_market_events_for_acknowledgment():
    ticker = {"u": 101, "s": "BTCUSDT", "b": "100", "B": "2", "a": "101", "A": "3"}
    connection = FakeConnection(
        [
            {"result": None, "id": 1},
            ticker,
            ticker,
            {"result": None, "id": 2},
        ]
    )

    events = await collect_book_tickers(
        "BTCUSDT",
        count=1,
        connect=lambda url: FakeConnectionContext(connection),
    )

    assert len(events) == 1


@pytest.mark.asyncio
async def test_live_depth_sync_discards_stale_buffered_events_and_applies_continuous_updates():
    class FakeRestClient:
        def depth_snapshot(self, symbol, limit):
            assert symbol == "BTCUSDT"
            assert limit == 100
            return {
                "lastUpdateId": 100,
                "bids": [["100", "2"]],
                "asks": [["101", "3"]],
            }

    connection = FakeConnection(
        [
            {"U": 90, "u": 100, "b": [["100", "9"]], "a": []},
            {"U": 101, "u": 101, "b": [["100", "4"]], "a": []},
            {"U": 102, "u": 102, "b": [], "a": [["101", "5"]]},
        ]
    )

    book = await synchronize_live_depth(
        "BTCUSDT",
        applied_event_count=2,
        rest_client=FakeRestClient(),
        connect=lambda url: FakeConnectionContext(connection),
    )

    assert book.update_id == 102
    assert book.best_bid == (Decimal("100"), Decimal("4"))
    assert book.best_ask == (Decimal("101"), Decimal("5"))


@pytest.mark.asyncio
async def test_subscription_receive_timeout_is_bounded():
    class SlowConnection(FakeConnection):
        async def recv(self):
            await asyncio.sleep(1)
            return await super().recv()

    connection = SlowConnection([{"result": None, "id": 1}])

    with pytest.raises(TimeoutError):
        await collect_book_tickers(
            "BTCUSDT",
            count=1,
            timeout=0.01,
            connect=lambda url: FakeConnectionContext(connection),
        )


@pytest.mark.asyncio
async def test_collect_book_tickers_rejects_malformed_json():
    connection = RawConnection(["{not-json"])

    with pytest.raises(WebSocketContractError, match="invalid JSON payload"):
        await collect_book_tickers(
            "BTCUSDT",
            count=1,
            connect=lambda url: FakeConnectionContext(connection),
        )


@pytest.mark.asyncio
async def test_collect_book_tickers_rejects_non_object_json():
    connection = RawConnection([json.dumps([None, 1])])

    with pytest.raises(WebSocketContractError, match="expected a JSON object"):
        await collect_book_tickers(
            "BTCUSDT",
            count=1,
            connect=lambda url: FakeConnectionContext(connection),
        )


@pytest.mark.asyncio
async def test_collect_book_tickers_rejects_missing_event_field():
    connection = FakeConnection(
        [
            {"result": None, "id": 1},
            {"u": 101, "s": "BTCUSDT", "b": "100", "B": "2", "a": "101"},
        ]
    )

    with pytest.raises(
        WebSocketContractError,
        match="bookTicker event has invalid schema",
    ):
        await collect_book_tickers(
            "BTCUSDT",
            count=1,
            connect=lambda url: FakeConnectionContext(connection),
        )
