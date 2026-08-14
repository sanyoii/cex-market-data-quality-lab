from decimal import Decimal

import pytest

from cex_quality.order_book import (
    MarketInvariantError,
    OrderBook,
    SequenceGapError,
    synchronize_order_book,
)


def test_snapshot_exposes_best_bid_and_ask_in_market_order():
    book = OrderBook.from_snapshot(
        {
            "lastUpdateId": 100,
            "bids": [["100.00", "2"], ["101.00", "1"]],
            "asks": [["103.00", "4"], ["102.00", "3"]],
        }
    )

    assert book.best_bid == (Decimal("101.00"), Decimal("1"))
    assert book.best_ask == (Decimal("102.00"), Decimal("3"))


def test_update_adds_and_removes_price_levels():
    book = OrderBook.from_snapshot(
        {
            "lastUpdateId": 100,
            "bids": [["101.00", "1"], ["100.00", "2"]],
            "asks": [["102.00", "3"], ["103.00", "4"]],
        }
    )

    applied = book.apply_update(
        {
            "U": 101,
            "u": 101,
            "b": [["101.00", "0"], ["100.50", "5"]],
            "a": [["102.00", "0"], ["102.50", "6"]],
        }
    )

    assert applied is True
    assert book.update_id == 101
    assert book.best_bid == (Decimal("100.50"), Decimal("5"))
    assert book.best_ask == (Decimal("102.50"), Decimal("6"))


def test_stale_update_is_ignored_without_changing_state():
    book = OrderBook.from_snapshot(
        {
            "lastUpdateId": 100,
            "bids": [["101.00", "1"]],
            "asks": [["102.00", "3"]],
        }
    )

    applied = book.apply_update(
        {
            "U": 90,
            "u": 99,
            "b": [["101.00", "0"]],
            "a": [["102.00", "0"]],
        }
    )

    assert applied is False
    assert book.update_id == 100
    assert book.best_bid == (Decimal("101.00"), Decimal("1"))
    assert book.best_ask == (Decimal("102.00"), Decimal("3"))


def test_sequence_gap_is_reported_before_state_changes():
    book = OrderBook.from_snapshot(
        {
            "lastUpdateId": 100,
            "bids": [["101.00", "1"]],
            "asks": [["102.00", "3"]],
        }
    )

    with pytest.raises(SequenceGapError, match="expected update 101, received 105-106"):
        book.apply_update(
            {
                "U": 105,
                "u": 106,
                "b": [["101.00", "0"]],
                "a": [["102.00", "0"]],
            }
        )

    assert book.update_id == 100
    assert book.best_bid == (Decimal("101.00"), Decimal("1"))
    assert book.best_ask == (Decimal("102.00"), Decimal("3"))


def test_crossed_snapshot_is_rejected():
    with pytest.raises(MarketInvariantError, match="best bid 103.00 exceeds best ask 102.00"):
        OrderBook.from_snapshot(
            {
                "lastUpdateId": 100,
                "bids": [["103.00", "1"]],
                "asks": [["102.00", "3"]],
            }
        )


def test_snapshot_and_buffered_updates_form_a_synchronized_book():
    book = synchronize_order_book(
        snapshot={
            "lastUpdateId": 100,
            "bids": [["101.00", "1"], ["100.00", "2"]],
            "asks": [["102.00", "3"], ["103.00", "4"]],
        },
        events=[
            {"U": 90, "u": 100, "b": [["101.00", "9"]], "a": []},
            {"U": 99, "u": 101, "b": [["101.00", "2"]], "a": []},
            {"U": 102, "u": 102, "b": [], "a": [["102.00", "5"]]},
        ],
    )

    assert book.update_id == 102
    assert book.best_bid == (Decimal("101.00"), Decimal("2"))
    assert book.best_ask == (Decimal("102.00"), Decimal("5"))


@pytest.mark.parametrize("price, quantity", [("0", "1"), ("101", "0"), ("101", "-1")])
def test_snapshot_rejects_non_positive_price_or_quantity(price, quantity):
    with pytest.raises(MarketInvariantError, match="price and quantity must be positive"):
        OrderBook.from_snapshot(
            {
                "lastUpdateId": 100,
                "bids": [[price, quantity]],
                "asks": [["102.00", "3"]],
            }
        )


def test_update_rejects_negative_quantity():
    book = OrderBook.from_snapshot(
        {
            "lastUpdateId": 100,
            "bids": [["101", "1"]],
            "asks": [["102", "3"]],
        }
    )

    with pytest.raises(
        MarketInvariantError,
        match="price must be positive and quantity cannot be negative",
    ):
        book.apply_update(
            {
                "U": 101,
                "u": 101,
                "b": [["101", "-1"]],
                "a": [],
            }
        )


@pytest.mark.parametrize(
    "bids, asks",
    [
        ([], [["102", "3"]]),
        ([["101", "1"]], []),
    ],
)
def test_snapshot_rejects_an_empty_market_side(bids, asks):
    with pytest.raises(
        MarketInvariantError,
        match="order book must contain both bids and asks",
    ):
        OrderBook.from_snapshot(
            {
                "lastUpdateId": 100,
                "bids": bids,
                "asks": asks,
            }
        )
