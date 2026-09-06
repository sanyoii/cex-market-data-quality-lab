# Current-head CI Status: 2026-08-15

Status: Incomplete publication verification. Deterministic jobs Passed; current-head live automation was not executed.

## Source and run

- Source revision: `8fd5081254b5429e480ec20a56ef09bcc6f5ab9e`
- Branch: `main`
- Event: `push`
- Workflow run: [31823105148](https://github.com/sanyoii/cex-market-data-quality-lab/actions/runs/31823105148)
- Workflow conclusion: `success`

## Results

| Job | Result | Evidence boundary |
|---|---|---|
| Deterministic, Python 3.12 | Passed, 39 pytest results | GitHub-hosted workflow result |
| Deterministic, Python 3.14 | Passed, 39 pytest results | GitHub-hosted workflow result |
| Live market data | Skipped | Push workflow rules do not execute the live job |

The deterministic result verifies the checked-in `8fd5081` state. It does not verify the uncommitted 40-result governance candidate.

## Live evidence boundary

No current-head live run exists. The latest public live receipt is [run 31813561202](https://github.com/sanyoii/cex-market-data-quality-lab/actions/runs/31813561202) at revision `9ce65e03b834c79c95bf2488c471be68cb7b1166`. That historical result cannot establish current-head live compatibility.

## Artifact check

The workflow run and job conclusions were checked. JUnit artifacts were not downloaded in this verification, so artifact contents, retention, and SHA-256 values remain unverified.
