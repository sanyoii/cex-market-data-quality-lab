"""Order-book state derived from a REST snapshot and WebSocket updates."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any


PriceLevel = tuple[Decimal, Decimal]


class SequenceGapError(RuntimeError):
    """Raised when an update cannot follow the current local order-book state."""


class MarketInvariantError(ValueError):
    """Raised when public market data forms an impossible local book."""


@dataclass
class OrderBook:
    """A small public interface around synchronized bid and ask state."""

    _bids: dict[Decimal, Decimal]
    _asks: dict[Decimal, Decimal]
    update_id: int

    @classmethod
    def from_snapshot(cls, snapshot: dict[str, Any]) -> OrderBook:
        book = cls(
            _bids={Decimal(price): Decimal(quantity) for price, quantity in snapshot["bids"]},
            _asks={Decimal(price): Decimal(quantity) for price, quantity in snapshot["asks"]},
            update_id=int(snapshot["lastUpdateId"]),
        )
        book._assert_positive_levels()
        book._assert_market_order()
        return book

    @property
    def best_bid(self) -> PriceLevel:
        price = max(self._bids)
        return price, self._bids[price]

    @property
    def best_ask(self) -> PriceLevel:
        price = min(self._asks)
        return price, self._asks[price]

    def apply_update(self, event: dict[str, Any]) -> bool:
        """Apply one Binance diff-depth event and report whether state changed."""
        if int(event["u"]) <= self.update_id:
            return False
        expected = self.update_id + 1
        first_update = int(event["U"])
        final_update = int(event["u"])
        if first_update > expected:
            raise SequenceGapError(
                f"expected update {expected}, received {first_update}-{final_update}"
            )
        self._apply_levels(self._bids, event["b"])
        self._apply_levels(self._asks, event["a"])
        self.update_id = int(event["u"])
        self._assert_market_order()
        return True

    @staticmethod
    def _apply_levels(
        side: dict[Decimal, Decimal], levels: list[list[str]]
    ) -> None:
        for raw_price, raw_quantity in levels:
            price = Decimal(raw_price)
            quantity = Decimal(raw_quantity)
            if price <= 0 or quantity < 0:
                raise MarketInvariantError(
                    "price must be positive and quantity cannot be negative"
                )
            if quantity == 0:
                side.pop(price, None)
            else:
                side[price] = quantity

    def _assert_market_order(self) -> None:
        if not self._bids or not self._asks:
            raise MarketInvariantError("order book must contain both bids and asks")
        bid_price, _ = self.best_bid
        ask_price, _ = self.best_ask
        if bid_price > ask_price:
            raise MarketInvariantError(
                f"best bid {bid_price} exceeds best ask {ask_price}"
            )

    def _assert_positive_levels(self) -> None:
        if any(price <= 0 or quantity <= 0 for price, quantity in self._bids.items()):
            raise MarketInvariantError("price and quantity must be positive")
        if any(price <= 0 or quantity <= 0 for price, quantity in self._asks.items()):
            raise MarketInvariantError("price and quantity must be positive")


def synchronize_order_book(
    snapshot: dict[str, Any], events: list[dict[str, Any]]
) -> OrderBook:
    """Build a local book from a REST snapshot and buffered diff-depth events."""
    book = OrderBook.from_snapshot(snapshot)
    for event in events:
        book.apply_update(event)
    return book
