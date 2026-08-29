# nba_prep

[![TestPyPI](https://img.shields.io/badge/TestPyPI-v0.3.2-blue.svg?logo=pypi&logoColor=white)](https://test.pypi.org/project/nba-prep-26040826/0.3.2/)
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
* **`test_cleaning.py`** — Validates basic data cleaning utility functions under [`src/nba_prep/cleaning.py`](file:///Users/aryan/AT1_AML/36120-26SP-group38-26040826-package/src/nba_prep/cleaning.py):
  * **`clean_height`**: Verifies that standard height strings (e.g. `"6-7"` to `79.0` and `"6-2"` to `74.0` inches) are correctly parsed, and checks that missing (`None`), malformed strings (e.g., `"invalid"`), or floats (e.g., `6.7`) return `NaN`.
  * **`clean_year`**: Checks the mapping of college year codes (`"Fr" -> 1`, `"So" -> 2`, `"Jr" -> 3`, `"Sr" -> 4`), conversion of numeric strings (e.g., `" 2.0 "` to integer `2`), and ensures invalid year codes return `NaN`.
  * **`calculate_age`**: Validates calculation of a prospect's age during a college season from birthdate strings (e.g. `"1997-10-15"` in `2020` yields `23.0`), and asserts that malformed date strings, `None` inputs, or missing season years return `NaN`.
* **`test_features.py`** — Validates advanced player feature math under [`src/nba_prep/features.py`](file:///Users/aryan/AT1_AML/36120-26SP-group38-26040826-package/src/nba_prep/features.py):
  * **`calculate_ast_tov_ratio`**: Tests standard assist-to-turnover ratio computations (e.g., `10` assists, `2` turnovers -> `5.0`), and verifies division-by-zero protection (e.g., `10` assists, `0` turnovers uses a default $1e-5$ epsilon, yielding `1,000,000.0`).
  * **`calculate_true_shooting_percentage`**: Asserts that True Shooting Percentage calculations match standard basketball analytics formula ($PTS / (2 \times (FGA + 0.44 \times FTA))$).
  * **`calculate_defensive_impact`**: Checks custom weighted defensive contributions ($1.5 \times Steals + 1.5 \times Blocks + 1.0 \times DefRebounds$).
  * **`calculate_scoring_efficiency`**: Asserts points production scaled by playing minutes percentage ($PTS / Min\%$).
  * **`calculate_advanced_recruit_and_conference_features`**: Uses a mock DataFrame to verify features like imputing missing recruiting ranks with a default average (`150.0`), setting binary recruiting rank existence indicators, flagging Power Conferences (e.g. ACC, Big Ten) vs mid-majors (e.g. WAC), and computing per-minute production rates.
* **`test_cumulative.py`** — Validates historical player-level tracking logic under [`src/nba_prep/features.py`](file:///Users/aryan/AT1_AML/36120-26SP-group38-26040826-package/src/nba_prep/features.py):
  * **`calculate_cumulative_features`**: Feeds a multi-season DataFrame for two distinct players (pid 1 and 2) to test grouped career historical progression. Asserts that the function correctly tracks sequential season counts (`career_season_num`), running totals (`cum_GP`, `cum_pts`), running averages (`cum_mean_bpm`, `cum_mean_usg`), career peak values to date (`max_pts_to_date`, `max_min_per_to_date`), and season-over-season progression deltas (`pts_progression`).
* **`test_analytics.py`** — Validates classification and descriptive scouting card logic under [`src/nba_prep/analytics.py`](file:///Users/aryan/AT1_AML/36120-26SP-group38-26040826-package/src/nba_prep/analytics.py):
  * **`categorize_prospect`**: Validates player draft prospects categorization into four discrete scouting categories:
    * *Tier 1: Franchise Core (Elite)* for probabilities >= 0.70
    * *Tier 2: Rotation Contributor (Moderate)* for 0.40 <= P < 0.70
    * *Tier 3: G-League / Development Project (Low-Moderate)* for 0.10 <= P < 0.40
    * *Tier 4: High Risk / Undrafted Profile (Very Low)* for P < 0.10
    * Asserts bounds checking for out-of-range probabilities (1.5 -> "Invalid Probability") and type mismatches.
  * **`generate_scouting_report`**: Validates the automated text card generator. Verifies that report descriptions contain appropriate qualitative descriptors based on statistics (e.g., asserts that an elite player report contains "Elite collegiate contributor", "Exceptionally efficient", and "Five-star high school recruit", while a bench player report prints "Below-average impact" and "Highly inefficient scorer").
* **`test_evaluation.py`** — Validates technical scoring metrics and business financial ROI outputs under [`src/nba_prep/evaluation.py`](file:///Users/aryan/AT1_AML/36120-26SP-group38-26040826-package/src/nba_prep/evaluation.py):
  * **`calculate_model_metrics`**: Confirms that model metric helper computes AUPRC, AUROC, base rate, and the optimal classification threshold (based on maximizing the F1-score) for a simulated prediction array.
  * **`estimate_draft_roi`**: Validates front-office financial models. Sets a decision threshold of 0.5 on a mock group of 10 prospects to assert total players drafted, successes, busts, draft success rate (e.g. 60.0% vs base rate of 30.0%), wasted salary cap dollars (e.g., 2 busts * $5,000,000 = $10,000,000), and percentage of travel and scouting hours saved (e.g. 50.0%). Also checks handling of high thresholds resulting in zero prospects drafted.

To execute tests locally, run:
```bash
pytest
```

### 2. Continuous Integration (CI) Pipeline
A GitHub Actions workflow is configured in `.github/workflows/test.yml` to automatically verify code integrity. On every push and pull request, the test runner:
* Spins up containerized environments across multiple Python versions (`3.10`, `3.11`, `3.12`, `3.13`).
* Installs dependencies, sets up the package, and executes the entire unit test suite.

#### Pipeline Run Execution & Status
The CI pipeline has run successfully across multiple iterations and code updates, verifying code standards, package builds, PyPI package structure, and full unit test compliance. Below is the record of the successful workflow runs demonstrating the validation:

![GitHub Actions CI Workflow Runs](docs/pipeline_runs.png)

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

### Generated Model Artifacts (`models/`)
* **LightGBM**: `models/final_lightgbm.joblib`, `models/final_lightgbm.txt`, `models/36120-26SP-group38-26040826-final_lightgbm.joblib`
* **XGBoost**: `models/final_xgboost.joblib`, `models/final_xgboost.json`, `models/36120-26SP-group38-26040826-final_xgboost.joblib`
* **CatBoost**: `models/final_catboost.joblib`, `models/final_catboost.cbm`, `models/36120-26SP-group38-26040826-final_catboost.joblib`
* **Experiment 3 Final Model**: `models/36120-26SP-group38-26040826-experiment3-model.joblib`
* **Predictions**: `submission.csv` (6,261 unique player rows, 0 duplicates, 0 nulls, ready for Kaggle submission)

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

### 4. Interactive Analysis Notebooks
The complete series of experimental notebooks conducted for this assessment:
* **Experiment 1 (Baseline):** `notebooks/36120-26SP-group38-26040826-AT1-experiment-1.ipynb` — Initial baseline LightGBM model and data cleaning exploration.
* **Experiment 2 (Model Exploration):** `notebooks/36120-26SP-group38-26040826-AT1-experiment-2.ipynb` — Systematic architecture comparison between Random Forest, HistGradientBoosting, and Tuned LightGBM.
* **Experiment 3 (Feature Selection & Ensembling):** `notebooks/36120-26SP-group38-26040826-AT1-experiment-3.ipynb` — Multi-model GBDT ensemble (LightGBM, XGBoost, CatBoost) trained on peak final-college seasons with correlation and gain-based feature selection.

--------

