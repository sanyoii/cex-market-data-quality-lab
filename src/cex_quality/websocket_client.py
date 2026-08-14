"""WebSocket checks for Binance public market-data streams."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

import websockets

from cex_quality.order_book import OrderBook
from cex_quality.rest_client import MarketDataRestClient


class WebSocketContractError(ValueError):
    """Raised when a stream acknowledgement or event violates its contract."""


@dataclass(frozen=True)
class BookTickerEvent:
    update_id: int
    symbol: str
    bid_price: Decimal
    bid_quantity: Decimal
    ask_price: Decimal
    ask_quantity: Decimal

    @classmethod
    def from_payload(cls, payload: dict[str, Any], expected_symbol: str) -> BookTickerEvent:
        try:
            event = cls(
                update_id=int(payload["u"]),
                symbol=str(payload["s"]),
                bid_price=Decimal(payload["b"]),
                bid_quantity=Decimal(payload["B"]),
                ask_price=Decimal(payload["a"]),
                ask_quantity=Decimal(payload["A"]),
            )
        except (InvalidOperation, KeyError, TypeError, ValueError) as exc:
            raise WebSocketContractError(
                "bookTicker event has invalid schema"
            ) from exc
        if event.symbol != expected_symbol:
            raise WebSocketContractError(
                f"expected symbol {expected_symbol}, received {event.symbol}"
            )
        if min(
            event.bid_price,
            event.bid_quantity,
            event.ask_price,
            event.ask_quantity,
        ) <= 0:
            raise WebSocketContractError("prices and quantities must be positive")
        if event.bid_price > event.ask_price:
            raise WebSocketContractError("best bid exceeds best ask")
        return event


async def collect_book_tickers(
    symbol: str,
    *,
    count: int = 3,
    timeout: float = 10.0,
    base_url: str = "wss://data-stream.binance.vision",
    connect: Callable[[str], Any] = websockets.connect,
) -> list[BookTickerEvent]:
    normalized = symbol.upper()
    stream = f"{symbol.lower()}@bookTicker"
    async with connect(f"{base_url}/ws") as connection:
        await connection.send(
            json.dumps({"method": "SUBSCRIBE", "params": [stream], "id": 1})
        )
        await _expect_ack(connection, request_id=1, timeout=timeout)

        events = []
        for _ in range(count):
            payload = await _receive_json(connection, timeout)
            event = BookTickerEvent.from_payload(payload, normalized)
            if events and event.update_id < events[-1].update_id:
                raise WebSocketContractError(
                    f"update ID decreased from {events[-1].update_id} to {event.update_id}"
                )
            events.append(event)

        await connection.send(
            json.dumps({"method": "UNSUBSCRIBE", "params": [stream], "id": 2})
        )
        await _expect_ack(connection, request_id=2, timeout=timeout)
        return events


async def synchronize_live_depth(
    symbol: str,
    *,
    applied_event_count: int = 3,
    timeout: float = 10.0,
    base_url: str = "wss://data-stream.binance.vision",
    rest_client: Any | None = None,
    connect: Callable[[str], Any] = websockets.connect,
) -> OrderBook:
    """Synchronize one REST snapshot with buffered public diff-depth events."""
    own_client = rest_client is None
    client = rest_client or MarketDataRestClient()
    stream = f"{symbol.lower()}@depth"
    try:
        async with connect(f"{base_url}/ws/{stream}") as connection:
            first_event = await _receive_json(connection, timeout)
            snapshot = await asyncio.to_thread(
                lambda: client.depth_snapshot(symbol.upper(), limit=100)
            )
            book = OrderBook.from_snapshot(snapshot)
            event = first_event
            applied = 0
            while applied < applied_event_count:
                if book.apply_update(event):
                    applied += 1
                if applied < applied_event_count:
                    event = await _receive_json(connection, timeout)
            return book
    finally:
        if own_client:
            client.close()


async def _expect_ack(connection: Any, *, request_id: int, timeout: float) -> None:
    async with asyncio.timeout(timeout):
        while True:
            payload = await _receive_json(connection, timeout)
            if payload == {"result": None, "id": request_id}:
                return
            if "id" in payload or "result" in payload:
                raise WebSocketContractError(
                    f"invalid acknowledgement for request {request_id}: {payload}"
                )


async def _receive_json(connection: Any, timeout: float) -> dict[str, Any]:
    raw = await asyncio.wait_for(connection.recv(), timeout=timeout)
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, TypeError, UnicodeDecodeError) as exc:
        raise WebSocketContractError("invalid JSON payload") from exc
    if not isinstance(payload, dict):
        raise WebSocketContractError("expected a JSON object")
    return payload
