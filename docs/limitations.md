# Limitations

- The project covers public Spot market data. It does not test authentication, balances, orders, matching-engine execution, deposits, withdrawals, wallets, chain confirmations, funding, liquidation, KYC, or AML.
- Live tests depend on Binance availability and network access. A runner block, DNS failure, rate limit, or disconnect is an external failure signal; deterministic contract tests do not prove live availability.
- Tests assert market invariants and documented fields. They do not assert a fixed price, quantity, spread, latency, or event frequency.
- The local order book uses a 100-level snapshot for a short test window. It does not provide a production trading view or cover price levels outside that snapshot.
- The client stops on a sequence gap. It reports the need to resynchronize but does not run a long-lived reconnect loop.
- The project uses one exchange and one default symbol. It does not claim cross-exchange compatibility.
- Local evidence comes from Windows and Python 3.14. Public GitHub Actions evidence verifies deterministic execution on Python 3.12 and 3.14 and a manually triggered live automation run on Python 3.14.
- Human exploratory charters are designed but have not been executed.
