import pytest

from cex_quality.rest_client import MarketDataRestClient


pytestmark = [pytest.mark.live, pytest.mark.timeout(30)]


def test_live_exchange_info_has_trading_symbol_and_core_filters():
    with MarketDataRestClient() as client:
        info = client.exchange_info("BTCUSDT")

    assert info.symbol == "BTCUSDT"
    assert info.status == "TRADING"
    assert "PRICE_FILTER" in info.filter_types
    assert "LOT_SIZE" in info.filter_types


def test_live_book_ticker_satisfies_market_invariants():
    with MarketDataRestClient() as client:
        ticker = client.book_ticker("BTCUSDT")

    assert ticker.symbol == "BTCUSDT"
    assert ticker.bid_price > 0
    assert ticker.ask_price > 0
    assert ticker.bid_quantity > 0
    assert ticker.ask_quantity > 0
    assert ticker.bid_price <= ticker.ask_price


def test_live_depth_snapshot_builds_a_valid_order_book():
    with MarketDataRestClient() as client:
        snapshot = client.depth_snapshot("BTCUSDT", limit=100)

    assert snapshot["lastUpdateId"] > 0
