"""REST client for Binance public market-data contracts."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

import httpx

from cex_quality.order_book import OrderBook


class RestContractError(ValueError):
    """Raised when a successful response violates the documented market contract."""


class ApiError(RuntimeError):
    def __init__(self, status_code: int, code: int | None, message: str) -> None:
        super().__init__(f"HTTP {status_code}: {code} {message}")
        self.status_code = status_code
        self.code = code
        self.message = message


@dataclass(frozen=True)
class BookTicker:
    symbol: str
    bid_price: Decimal
    bid_quantity: Decimal
    ask_price: Decimal
    ask_quantity: Decimal


@dataclass(frozen=True)
class SymbolInfo:
    symbol: str
    status: str
    filter_types: tuple[str, ...]


class MarketDataRestClient:
    def __init__(
        self,
        base_url: str = "https://data-api.binance.vision",
        *,
        timeout: float = 10.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            transport=transport,
        )

    def __enter__(self) -> MarketDataRestClient:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    def book_ticker(self, symbol: str) -> BookTicker:
        payload = self._get_json(
            "/api/v3/ticker/bookTicker",
            params={"symbol": symbol.upper()},
        )
        try:
            ticker = BookTicker(
                symbol=str(payload["symbol"]),
                bid_price=Decimal(payload["bidPrice"]),
                bid_quantity=Decimal(payload["bidQty"]),
                ask_price=Decimal(payload["askPrice"]),
                ask_quantity=Decimal(payload["askQty"]),
            )
        except (InvalidOperation, KeyError, TypeError, ValueError) as exc:
            raise RestContractError(
                "bookTicker response has invalid schema"
            ) from exc
        if min(
            ticker.bid_price,
            ticker.bid_quantity,
            ticker.ask_price,
            ticker.ask_quantity,
        ) <= 0:
            raise RestContractError("prices and quantities must be positive")
        if ticker.bid_price > ticker.ask_price:
            raise RestContractError("best bid exceeds best ask")
        return ticker

    def depth_snapshot(self, symbol: str, *, limit: int = 100) -> dict[str, Any]:
        payload = self._get_json(
            "/api/v3/depth",
            params={"symbol": symbol.upper(), "limit": limit},
        )
        OrderBook.from_snapshot(payload)
        return payload

    def exchange_info(self, symbol: str) -> SymbolInfo:
        payload = self._get_json(
            "/api/v3/exchangeInfo",
            params={"symbol": symbol.upper()},
        )
        symbols = payload.get("symbols", [])
        if len(symbols) != 1:
            raise RestContractError("exchangeInfo must return exactly one symbol")
        item = symbols[0]
        return SymbolInfo(
            symbol=str(item["symbol"]),
            status=str(item["status"]),
            filter_types=tuple(
                str(entry["filterType"]) for entry in item.get("filters", [])
            ),
        )

    def _get_json(self, path: str, *, params: dict[str, Any]) -> dict[str, Any]:
        response = self._client.get(path, params=params)
        payload: dict[str, Any] = response.json()
        if response.is_error:
            raise ApiError(
                status_code=response.status_code,
                code=payload.get("code"),
                message=str(payload.get("msg", response.reason_phrase)),
            )
        return payload
