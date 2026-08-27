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
--------
## Development & Quality Standards

### 1. Robust Unit Test Coverage
This package is fully verified by 13 unit tests distributed across 5 specialized test suites:
* **`test_cleaning.py`**: Validates data cleaning utilities under [`src/nba_prep/cleaning.py`](file:///Users/aryan/AT1_AML/36120-26SP-group38-26040826-package/src/nba_prep/cleaning.py).
  * `clean_height`: Verifies parsing height strings (e.g. `"6-7"` to `79.0` inches) and ensures missing (`None`) or invalid values safely return `NaN`.
  * `clean_year`: Validates mapping class year abbreviations (`"Fr"`, `"So"`, `"Jr"`, `"Sr"`) and floats/whitespace-padded strings to numeric ranks (`1` to `4`).
  * `calculate_age`: Confirms calculation of prospect age from birth date strings and season years, handling invalid formats gracefully.
* **`test_features.py`**: Validates core basketball features under [`src/nba_prep/features.py`](file:///Users/aryan/AT1_AML/36120-26SP-group38-26040826-package/src/nba_prep/features.py).
  * `calculate_ast_tov_ratio`: Tests assist-to-turnover ratio logic with division-by-zero protection (applying a $1e-5$ epsilon).
  * `calculate_true_shooting_percentage`: Verifies standard scoring efficiency formulas (True Shooting % accounting for FGA and FTA).
  * `calculate_defensive_impact`: Checks weighted defensive impact metrics (combining steals, blocks, and defensive rebounds).
  * `calculate_scoring_efficiency`: Tests production scaling relative to playing minutes percentage.
  * `calculate_advanced_recruit_and_conference_features`: Validates filling high school recruiting ranks, setting binary index flags, flagging Power Conferences, and computing per-minute stats.
* **`test_cumulative.py`**: Validates historical career progression logic under [`src/nba_prep/features.py`](file:///Users/aryan/AT1_AML/36120-26SP-group38-26040826-package/src/nba_prep/features.py).
  * `calculate_cumulative_features`: Tests grouped aggregation by Player ID (`pid`) over successive calendar years to calculate running career counts, running season averages (e.g., Box Plus-Minus, usage rates), seasonal progression deltas, and peak metrics to date.
* **`test_analytics.py`**: Validates scouting reports and tier classifications under [`src/nba_prep/analytics.py`](file:///Users/aryan/AT1_AML/36120-26SP-group38-26040826-package/src/nba_prep/analytics.py).
  * `categorize_prospect`: Tests categorization of draft prospects into four distinct talent tiers (Franchise Core, Rotation Contributor, G-League, High Risk) based on model probabilities.
  * `generate_scouting_report`: Confirms correct generation of text-based scouting profile reports with qualitative descriptors based on on-court statistics.
* **`test_evaluation.py`**: Validates model evaluation and business metrics under [`src/nba_prep/evaluation.py`](file:///Users/aryan/AT1_AML/36120-26SP-group38-26040826-package/src/nba_prep/evaluation.py).
  * `calculate_model_metrics`: Tests standard classification rankings (AUPRC, AUROC, base rate) and locates the F1-optimizing threshold.
  * `estimate_draft_roi`: Verifies business metrics like draft success rates, salary cap space wasted on busts, and scouting hours/travel saved.

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


--------
## Latest Model Performance & Credit

This training run was performed by **Aryan Goel (26040826)**.

### Performance Scores (OOF AUPRC)
* **LightGBM**: `0.48416`
* **Extra Trees**: `0.49197`
* **Logistic Regression**: `0.48983`
* **XGBoost**: `0.50970`
* **CatBoost**: `0.51188`
* **Blended Ensemble**: `0.52035`

### Generated Artifacts
* **Ensembled Models**: `models/final_lightgbm.txt`, `models/final_xgboost.json`, and `models/final_catboost.cbm`
* **Predictions**: `submission.csv` (6,261 rows, deduplicated unique player IDs)

--------

## Reproducibility Instructions

### 1. Install dependencies and local package
To set up the project environment and install the required libraries:
```bash
pip install -r requirements.txt
```
This will automatically install my custom `nba_prep` feature engineering package in editable mode.

### 2. Preprocess Data and Engineer Features
Run the dataset pipeline to clean the raw data (height, year, age) and generate the advanced basketball features:
```bash
python -m AT1_AML.dataset
```
This will save the processed training and test features to `data/processed/train_processed.csv` and `data/processed/test_processed.csv`.

### 3. Train Model and Generate Predictions
Run the cross-validated model training script:
```bash
python -m AT1_AML.modeling.train
```
This will:
- Execute a 5-Fold Stratified Group Cross-Validation (grouped by `pid` to prevent player-level leakage) using an ensemble of **LightGBM**, **XGBoost**, and **CatBoost**.
- Output overall AUPRC scores (target metric) for each individual model and the blended ensemble.
- Save the predicted probabilities on each player's final college season to `submission.csv` (deduplicated by `pid` and ready for Kaggle upload).

### 4. Interactive Analysis
My interactive end-to-end walkthrough notebook is available at `notebooks/36120-26SP-group38-26040826-AT1-experiment-1.ipynb`.

--------

