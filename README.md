# nba_prep

[![TestPyPI](https://img.shields.io/badge/TestPyPI-v0.3.0-blue.svg?logo=pypi&logoColor=white)](https://test.pypi.org/project/nba-prep-26040826/0.3.0/)
[![Tests Status](https://github.com/16aryan/36120-26SP-group38-26040826-Python-package-Aryan-Goel/actions/workflows/test.yml/badge.svg)](https://github.com/16aryan/36120-26SP-group38-26040826-Python-package-Aryan-Goel/actions)

`nba_prep` is a Python utility package designed to clean and engineer features for predicting NBA career longevity.

## Installation

To install this package locally for development:
```bash
pip install -e .
```

To install from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ nba_prep_26040826
```

## Features

- **Height Cleaning**: Converts height strings (e.g. `6-7`) to numeric inches.
- **Year Cleaning**: Cleans college year categories (`Fr`, `So`, `Jr`, `Sr`) into standard integers (1 to 4).
- **Age Extraction**: Computes player age during a college season from date of birth (DOB) and season year.
- **Basketball Analytics**: Calculates Advanced Basketball Metrics (e.g. Assist-to-Turnover ratio, True Shooting percentage, Defensive Impact score, and Offensive Rating interaction).
- **Cumulative Career Features**: Calculates running career totals, averages, season-by-season progression deltas, and peak career maximums to date for tracking player consistency.
- **Recruiting & Conference Features**: Imputes high school recruiting ranks, handles Power Conference binary indexing, and calculates pace-adjusted per-minute production metrics.
- **Decision Support & Scouting Reports**: Includes prospect classification into success probability tiers and automated scouting report card generators summarizing collegiate metrics for front-office decision-makers.
- **Model Evaluation & Financial ROI**: Computes technical evaluation metrics (AUPRC, AUROC, F1-optimized decision thresholds) and translates model probabilities into financial business ROI (wasted rookie contract cap space avoided, scouting travel cost savings).

## Usage

Here is a quick example of how to use the package:

```python
from nba_prep import clean_height, categorize_prospect, generate_scouting_report

# 1. Clean height data
height_inches = clean_height("6-7")  # returns 79.0

# 2. Categorize a prospect's probability score
tier = categorize_prospect(0.82)     # returns "Tier 1: Franchise Core (Elite)"

# 3. Generate a scouting report card
report = generate_scouting_report(
    "Aryan Goel", 
    bpm=9.2, 
    true_shooting=0.61, 
    defensive_impact=11.0, 
    rec_rank=15.0
)
print(report)
```

## Development & Quality Standards

### 1. Robust Unit Test Coverage
This package is fully verified by 13 unit tests distributed across 5 specialized test suites:
* **`test_cleaning.py`**: Validates height parsing, collegiate year code standardization, and birthday age extraction.
* **`test_features.py`**: Validates advanced basketball metric calculations (Assist-to-Turnover ratio, True Shooting %, Defensive Impact score, and Offensive interaction features).
* **`test_cumulative.py`**: Validates career historical tracking logic (running career counts, running season averages, peak metrics to date, and season-over-season progression deltas).
* **`test_analytics.py`**: Validates prospect classification tiers and descriptive scouting report generators.
* **`test_evaluation.py`**: Validates prediction ranking metrics (AUPRC, AUROC, optimal classification thresholds) and financial decision ROI estimators.

To execute tests locally, run:
```bash
pytest
```

### 2. Continuous Integration (CI) Pipeline
A GitHub Actions workflow is configured in `.github/workflows/test.yml` to automatically verify code integrity. On every push and pull request, the test runner:
* Spins up containerized environments across multiple Python versions (`3.10`, `3.11`, `3.12`, `3.13`).
* Installs dependencies, sets up the package, and executes the entire unit test suite.

### 3. Packaging & Standards Compliance
* **Pyproject Configuration (`pyproject.toml`)**: Structured with PEP 621 metadata, dependencies (`numpy`, `pandas`), development requirements (`pytest`, `pytest-cov`), and default pytest search paths.
* **Licensing (`LICENSE`)**: Distributed under the permissive open-source MIT License.
* **Git Hygiene (`.gitignore`)**: Configured to ensure compilation caches (`__pycache__`), build directories (`dist/`, `build/`), test reports, and IDE configurations are kept out of source control tracking.


