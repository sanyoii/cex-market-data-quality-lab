import pytest

from cex_quality.websocket_client import collect_book_tickers, synchronize_live_depth


pytestmark = [pytest.mark.live, pytest.mark.timeout(30)]


@pytest.mark.asyncio
async def test_live_book_ticker_stream_returns_ordered_valid_events():
    events = await collect_book_tickers("BTCUSDT", count=3, timeout=10)

    assert len(events) == 3
    assert all(event.symbol == "BTCUSDT" for event in events)
    assert all(
        current.update_id <= following.update_id
        for current, following in zip(events, events[1:])
    )


@pytest.mark.asyncio
async def test_live_rest_snapshot_and_depth_stream_synchronize():
    book = await synchronize_live_depth(
        "BTCUSDT",
        applied_event_count=3,
        timeout=10,
    )

    assert book.update_id > 0
    assert book.best_bid[0] <= book.best_ask[0]
