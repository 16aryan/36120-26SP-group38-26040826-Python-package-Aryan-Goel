# nba_prep

`nba_prep` is a Python utility package designed to clean and engineer features for predicting NBA career longevity.

## Installation

To install this package locally for development:
```bash
pip install -e .
```

To install from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps nba_prep
```

## Features

- **Height Cleaning**: Converts height strings (e.g. `6-7`) to numeric inches.
- **Year Cleaning**: Cleans college year categories (`Fr`, `So`, `Jr`, `Sr`) into standard integers (1 to 4).
- **Age Extraction**: Computes player age during a college season from date of birth (DOB) and season year.
- **Basketball Analytics**: Calculates Advanced Basketball Metrics (e.g. Assist-to-Turnover ratio, True Shooting percentage, Defensive Impact score, and Offensive Rating interaction).
- **Cumulative Career Features**: Calculates running career totals, averages, season-by-season progression deltas, and peak career maximums to date for tracking player consistency.
- **Recruiting & Conference Features**: Imputes high school recruiting ranks, handles Power Conference binary indexing, and calculates pace-adjusted per-minute production metrics.

