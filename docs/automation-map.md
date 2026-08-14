# Test Script and Automation Map

## Production interfaces under test

| Interface | Version-controlled path | Responsibility |
|---|---|---|
| Order-book model | `src/cex_quality/order_book.py` | Snapshot construction, price-level updates, stale detection, sequence-gap detection, and market invariants |
| REST client | `src/cex_quality/rest_client.py` | Public request construction, response parsing, error preservation, and REST contract validation |
| WebSocket client | `src/cex_quality/websocket_client.py` | Subscription lifecycle, bounded receive, event validation, and live depth synchronization |

This API project has no UI locator or Page Object Model. Protocol adapters and injected transports／connections provide the equivalent test seams.

## Test Case to script mapping

| Test Case IDs | Script and test function |
|---|---|
| OB-001 | `tests/unit/test_order_book.py::test_snapshot_exposes_best_bid_and_ask_in_market_order` |
| OB-002 | `tests/unit/test_order_book.py::test_update_adds_and_removes_price_levels` |
| OB-003 | `tests/unit/test_order_book.py::test_stale_update_is_ignored_without_changing_state` |
| OB-004 | `tests/unit/test_order_book.py::test_sequence_gap_is_reported_before_state_changes` |
| OB-005 | `tests/unit/test_order_book.py::test_crossed_snapshot_is_rejected` |
| OB-006 | `tests/unit/test_order_book.py::test_snapshot_and_buffered_updates_form_a_synchronized_book` |
| OB-007 | `tests/unit/test_order_book.py::test_snapshot_rejects_non_positive_price_or_quantity` |
| OB-008 | `tests/unit/test_order_book.py::test_update_rejects_negative_quantity` |
| OB-009 | `tests/unit/test_order_book.py::test_snapshot_rejects_an_empty_market_side` |
| REST-001 | `tests/contract/test_rest_contract.py::test_book_ticker_returns_validated_decimal_values` |
| REST-002 | `tests/contract/test_rest_contract.py::test_book_ticker_rejects_crossed_market_data` |
| REST-003 | `tests/contract/test_rest_contract.py::test_depth_snapshot_is_validated_before_returning` |
| REST-004 | `tests/contract/test_rest_contract.py::test_invalid_symbol_preserves_status_code_and_exchange_error` |
| REST-005 | `tests/contract/test_rest_contract.py::test_exchange_info_returns_requested_trading_symbol_and_filters` |
| REST-006 | `tests/contract/test_rest_contract.py::test_book_ticker_rejects_non_positive_price_or_quantity` |
| REST-007 | `tests/contract/test_rest_contract.py::test_exchange_info_requires_exactly_one_symbol` |
| REST-008 | `tests/contract/test_rest_contract.py::test_book_ticker_rejects_invalid_response_schema` |
| REST-009 | `tests/contract/test_rest_contract.py::test_rest_transport_timeout_remains_diagnosable` |
| WS-001 | `tests/contract/test_websocket_contract.py::test_collect_book_tickers_subscribes_validates_and_unsubscribes` |
| WS-002 | `tests/contract/test_websocket_contract.py::test_collect_book_tickers_rejects_decreasing_update_ids` |
| WS-003, WS-004, WS-005 | `tests/contract/test_websocket_contract.py::test_collect_book_tickers_rejects_invalid_market_events` |
| WS-006 | `tests/contract/test_websocket_contract.py::test_collect_book_tickers_rejects_invalid_subscription_acknowledgement` |
| WS-007 | `tests/contract/test_websocket_contract.py::test_unsubscribe_waits_past_in_flight_market_events_for_acknowledgement` |
| WS-008 | `tests/contract/test_websocket_contract.py::test_live_depth_sync_discards_stale_buffered_events_and_applies_continuous_updates` |
| WS-009 | `tests/contract/test_websocket_contract.py::test_subscription_receive_timeout_is_bounded` |
| WS-010 | `tests/contract/test_websocket_contract.py::test_collect_book_tickers_rejects_malformed_json` |
| WS-011 | `tests/contract/test_websocket_contract.py::test_collect_book_tickers_rejects_non_object_json` |
| WS-012 | `tests/contract/test_websocket_contract.py::test_collect_book_tickers_rejects_missing_event_field` |
| DOC-001 | `tests/meta/test_documentation_contract.py::test_every_requirement_is_present_in_the_traceability_matrix` |
| DOC-002 | `tests/meta/test_documentation_contract.py::test_every_logical_case_maps_to_an_existing_pytest_function` |
| DOC-003 | `tests/meta/test_documentation_contract.py::test_all_relative_markdown_links_resolve` |
| DOC-004 | `tests/meta/test_documentation_contract.py::test_public_scope_uses_only_allowlisted_market_data_interfaces` |
| LIVE-REST-001 | `tests/live/test_rest_live.py::test_live_exchange_info_has_trading_symbol_and_core_filters` |
| LIVE-REST-002 | `tests/live/test_rest_live.py::test_live_book_ticker_satisfies_market_invariants` |
| LIVE-REST-003 | `tests/live/test_rest_live.py::test_live_depth_snapshot_builds_a_valid_order_book` |
| LIVE-WS-001 | `tests/live/test_websocket_live.py::test_live_book_ticker_stream_returns_ordered_valid_events` |
| LIVE-SYNC-001 | `tests/live/test_websocket_live.py::test_live_rest_snapshot_and_depth_stream_synchronize` |

## Assertions and exception policy

- Expected results use exact object values, exception types／messages, protocol payloads, and market invariants.
- REST and WebSocket operations use explicit timeout bounds; live cases also use `pytest-timeout`.
- The workflow performs no automatic test retry. pytest surfaces a contract failure at once.
- Mock transports and fake connections replace only external I/O. Assertions still exercise the same validation code used by live tests.
- Documentation contract tests verify repository mappings and paths. They do not replace behavioral tests.
