# Evidence Records

Each execution record must include:

- UTC timestamp and environment.
- Python and dependency versions.
- Source revision, or `uncommitted local candidate` before the first commit.
- Exact commands and exit codes.
- Collected, passed, failed, skipped, and deselected counts.
- Warnings, blockers, and external-service failures.
- Generated JUnit paths and hashes when available.

Keep failed and blocked attempts after a later pass. A successful rerun does not erase the original failure or its cause.

## Records

- [2026-08-14 local deterministic and live run](2026-08-14-local-live-run.md)
- [2026-08-14 public CI and live verification](2026-08-14-public-ci-run.md)
