from decimal import Decimal

import httpx
import pytest

from cex_quality.rest_client import ApiError, MarketDataRestClient, RestContractError


def test_book_ticker_returns_validated_decimal_values():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v3/ticker/bookTicker"
        assert request.url.params["symbol"] == "BTCUSDT"
        return httpx.Response(
            200,
            json={
                "symbol": "BTCUSDT",
                "bidPrice": "100.10",
                "bidQty": "2.5",
                "askPrice": "100.20",
                "askQty": "3.5",
            },
        )

    with MarketDataRestClient(
        base_url="https://market-data.invalid",
        transport=httpx.MockTransport(handler),
    ) as client:
        ticker = client.book_ticker("btcusdt")

    assert ticker.symbol == "BTCUSDT"
    assert ticker.bid_price == Decimal("100.10")
    assert ticker.bid_quantity == Decimal("2.5")
    assert ticker.ask_price == Decimal("100.20")
    assert ticker.ask_quantity == Decimal("3.5")


def test_book_ticker_rejects_crossed_market_data():
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            json={
                "symbol": "BTCUSDT",
                "bidPrice": "100.30",
                "bidQty": "2.5",
                "askPrice": "100.20",
                "askQty": "3.5",
            },
        )
    )

    with MarketDataRestClient(
        base_url="https://market-data.invalid", transport=transport
    ) as client:
        with pytest.raises(RestContractError, match="best bid exceeds best ask"):
            client.book_ticker("BTCUSDT")


def test_depth_snapshot_is_validated_before_returning():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v3/depth"
        assert request.url.params["symbol"] == "BTCUSDT"
        assert request.url.params["limit"] == "5"
        return httpx.Response(
            200,
            json={
                "lastUpdateId": 100,
                "bids": [["100.10", "2"]],
                "asks": [["100.20", "3"]],
            },
        )

    with MarketDataRestClient(
        base_url="https://market-data.invalid",
        transport=httpx.MockTransport(handler),
    ) as client:
        snapshot = client.depth_snapshot("btcusdt", limit=5)

    assert snapshot["lastUpdateId"] == 100


def test_invalid_symbol_preserves_status_code_and_exchange_error():
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            400,
            json={"code": -1121, "msg": "Invalid symbol."},
        )
    )

    with MarketDataRestClient(
        base_url="https://market-data.invalid", transport=transport
    ) as client:
        with pytest.raises(ApiError) as caught:
            client.book_ticker("NOT_A_SYMBOL")

    assert caught.value.status_code == 400
    assert caught.value.code == -1121
    assert caught.value.message == "Invalid symbol."


def test_exchange_info_returns_requested_trading_symbol_and_filters():
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            json={
                "symbols": [
                    {
                        "symbol": "BTCUSDT",
                        "status": "TRADING",
                        "filters": [
                            {"filterType": "PRICE_FILTER"},
                            {"filterType": "LOT_SIZE"},
                        ],
                    }
                ]
            },
        )
    )

    with MarketDataRestClient(
        base_url="https://market-data.invalid", transport=transport
    ) as client:
        info = client.exchange_info("btcusdt")

    assert info.symbol == "BTCUSDT"
    assert info.status == "TRADING"
    assert info.filter_types == ("PRICE_FILTER", "LOT_SIZE")


def test_book_ticker_rejects_non_positive_price_or_quantity():
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            json={
                "symbol": "BTCUSDT",
                "bidPrice": "100.10",
                "bidQty": "0",
                "askPrice": "100.20",
                "askQty": "3.5",
            },
        )
    )

    with MarketDataRestClient(
        base_url="https://market-data.invalid", transport=transport
    ) as client:
        with pytest.raises(RestContractError, match="prices and quantities must be positive"):
            client.book_ticker("BTCUSDT")
