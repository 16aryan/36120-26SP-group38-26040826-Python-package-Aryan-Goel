# nba_prep (v0.4.0)

[![TestPyPI](https://img.shields.io/badge/TestPyPI-v0.4.0-blue.svg?logo=pypi&logoColor=white)](https://test.pypi.org/project/nba-prep-26040826/0.4.0/)
[![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Tests Status](https://img.shields.io/badge/tests-20%2F20%20passed-brightgreen.svg)](https://github.com/16aryan/36120-26SP-group38-26040826-Python-package-Aryan-Goel)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`nba_prep` (`nba-prep-26040826`) is a dual-domain production Python package developed for UTS **36120 Advanced Machine Learning Applications**. It provides reusable data preprocessing, feature engineering, and target variable derivation pipelines for:

1. **AT1 — Collegiate Basketball Prospect Analytics & Career Longevity Prediction:**
   - Raw anthropometric and career data cleaning.
   - Advanced basketball metric calculations (True Shooting %, Defensive Impact, Assist/TO ratio, Scoring Efficiency).
   - Multi-season cumulative statistics, progression deltas, and peak career maximums.
   - Decision support scouting report generation and prospect classification tiers.
   - Technical model scoring (AUPRC, AUROC, F1-optimal thresholding) and front-office financial ROI analysis.

2. **AT2 — Open-Meteo Weather Intelligence & Machine Learning as a Service (MLaaS):**
   - **Target 1:** Climate Comfort Index (CCI) regression target engineering (+3-day forecast horizon) and 5-tier descriptive condition interpretation.
   - **Target 2:** Weather Hazard Category (WHC) 4-class multiclass classification target engineering (+7-day forecast horizon) and risk category interpretation.
   - Raw hourly-to-daily meteorological aggregations strictly following Open-Meteo aggregation rules.
   - Zero-leakage cyclical trigonometric solar calendar encodings (sine and cosine).
   - Strict backward-shifted consecutive dry-streak day tracking without temporal lookahead bias.

---

## Installation

### From TestPyPI (Recommended)
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ nba-prep-26040826==0.4.0
```

### Local Development Installation
Clone the repository and install in editable mode:
```bash
git clone https://github.com/16aryan/36120-26SP-group38-26040826-Python-package-Aryan-Goel.git
cd 36120-26SP-group38-26040826-Python-package-Aryan-Goel
pip install -e .
```

---

## Module Architecture

```
nba_prep/
├── __init__.py           # Unified top-level exports for AT1 & AT2
├── cleaning.py           # [AT1] Data cleaning (height, year, age)
├── features.py           # [AT1] Advanced basketball metrics & cumulative career tracking
├── analytics.py          # [AT1] Prospect tier categorization & scouting report generation
├── evaluation.py         # [AT1] Technical evaluation metrics (AUPRC/AUROC) & financial ROI
└── weather.py            # [AT2] Weather Intelligence (CCI, WHC, daily aggregations, dry streak)
```

---

## Quickstart & Usage

### 1. AT1 — Basketball Prospect Analytics

```python
import numpy as np
from nba_prep import (
    clean_height,
    clean_year,
    calculate_age,
    calculate_true_shooting_percentage,
    calculate_defensive_impact,
    categorize_prospect,
    generate_scouting_report,
    calculate_model_metrics,
    estimate_draft_roi,
)

# --- Data Cleaning ---
height_in = clean_height("6-7")          # Returns 79.0 inches
year_code = clean_year("Jr")              # Returns 3
age = calculate_age("2001-04-12", 2023)   # Returns 22.0

# --- Advanced Basketball Metrics ---
ts_pct = calculate_true_shooting_percentage(pts=450, fga=320, fta=110)
def_impact = calculate_defensive_impact(stl=45, blk=30, drb=120)

# --- Front-Office Decision Support ---
tier = categorize_prospect(0.82)
# Returns: "Tier 1: Franchise Core (Elite)"

report = generate_scouting_report(
    "Aryan Goel",
    bpm=9.2,
    true_shooting=0.61,
    defensive_impact=11.0,
    rec_rank=15.0
)
print(report)

# --- Model Evaluation & Financial ROI ---
y_true = [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
y_pred = [0.92, 0.78, 0.85, 0.40, 0.12, 0.65, 0.31, 0.05, 0.18, 0.09]

metrics = calculate_model_metrics(y_true, y_pred)
print(f"AUPRC: {metrics['auprc']:.4f} | Optimal Threshold: {metrics['optimal_threshold']:.2f}")

roi = estimate_draft_roi(y_true, y_pred, threshold=0.50, rookie_contract_cost=5000000)
print(f"Scouting Yield Improvement: {roi['relative_improvement_factor']:.2f}x")
print(f"Wasted Cap Dollars: ${roi['wasted_salary_cap_dollars']:,}")
```

---

### 2. AT2 — Weather Intelligence (CCI & WHC)

```python
import pandas as pd
from nba_prep import (
    calculate_cci,
    interpret_cci,
    calculate_weather_hazard_index,
    convert_whi_to_whc,
    calculate_whc,
    interpret_whc,
    aggregate_hourly_to_daily,
    calculate_dry_streak,
    add_cyclical_calendar_features,
)

# --- Target 1: Climate Comfort Index (Regression) ---
# Formula: CCI = 100 * (0.35*Temp + 0.25*Humidity + 0.20*Wind + 0.10*Cloud + 0.10*Rain)
cci_score, components = calculate_cci(
    temperature_2m=22.0,
    relative_humidity_2m=50.0,
    wind_speed_10m=10.0,
    cloud_cover=10.0,
    precipitation=0.0
)
print(f"CCI Score: {cci_score:.1f}/100 -> {interpret_cci(cci_score)}")
# Output: CCI Score: 98.5/100 -> Excellent outdoor conditions

# --- Target 2: Weather Hazard Category (Classification) ---
# Formula: WHI = 100 * (0.30*Rain + 0.30*Wind + 0.20*Cloud + 0.10*Snow + 0.10*Temp)
# Discretized into: 0: Low Risk (<25), 1: Moderate (25-49), 2: High (50-74), 3: Extreme (>=75)
whi, hazards = calculate_weather_hazard_index(
    precipitation=15.0,
    wind_gusts_10m=65.0,
    cloud_cover=80.0,
    snowfall=0.0,
    temperature_2m=32.0
)
category = convert_whi_to_whc(whi)
print(f"WHI: {whi:.1f} -> Category {category} ({interpret_whc(category)})")
# Output: WHI: 54.5 -> Category 2 (High Risk)

# Convenience helper for direct categorization:
direct_cat = calculate_whc(
    precipitation=0.0, wind_gusts_10m=15.0, cloud_cover=10.0, snowfall=0.0, temperature_2m=21.0
)
print(f"Direct Category: {direct_cat} ({interpret_whc(direct_cat)})")

# --- Meteorological Preprocessing & Aggregations ---
sample_hourly = pd.DataFrame({
    "date": ["2024-01-01 00:00", "2024-01-01 12:00", "2024-01-02 00:00", "2024-01-02 12:00"],
    "temperature_2m": [18.0, 26.0, 20.0, 24.0],
    "relative_humidity_2m": [70.0, 45.0, 65.0, 50.0],
    "precipitation": [0.0, 2.5, 0.0, 0.0],
    "wind_speed_10m": [8.0, 15.0, 10.0, 12.0],
    "wind_gusts_10m": [15.0, 30.0, 20.0, 25.0],
    "cloud_cover": [20.0, 60.0, 10.0, 30.0],
    "snowfall": [0.0, 0.0, 0.0, 0.0],
    "shortwave_radiation_sum": [10.0, 50.0, 15.0, 45.0],
    "direct_normal_irradiance": [5.0, 40.0, 10.0, 35.0],
    "surface_pressure": [1013.0, 1012.0, 1014.0, 1013.0],
    "weather_code": [0, 1, 0, 0],
})

# Aggregate hourly to daily:
daily = aggregate_hourly_to_daily(sample_hourly, date_col="date")

# Calculate zero-leakage consecutive dry-streak days:
daily["dry_streak_days"] = calculate_dry_streak(daily["precipitation"])

# Add cyclical solar calendar encodings:
daily = add_cyclical_calendar_features(daily)
```

---

## Built-In Verification Script

To verify that all AT1 and AT2 features run correctly in your active environment:

```bash
python verify_package.py
```

Expected output:
```text
================================================================
--- Verifying Custom Python Package: nba_prep (v0.4.0) ---
================================================================

[AT1 Prospect Analytics]
  ✓ Height '6-7' cleaned to: 79.0 inches (Expected: 79.0)
  ✓ Prospect probability 0.82 classified as: 'Tier 1: Franchise Core (Elite)'
  ✓ Model Evaluation AUPRC: 0.9167, AUROC: 0.9524
  ✓ Draft ROI yield factor: 2.50x

[AT2 Weather Intelligence - Target 1: Climate Comfort Index (CCI)]
  ✓ Optimal Day CCI Score: 98.50/100 -> 'Excellent outdoor conditions'
  ✓ Adverse Day CCI Score: 23.88/100 -> 'Poor comfort'

[AT2 Weather Intelligence - Target 2: Weather Hazard Category (WHC)]
  ✓ Weather Hazard Index (WHI): 54.50/100 -> Category 2 ('High Risk')
  ✓ Calm Day WHC Category: 0 ('Low Risk')

[AT2 Preprocessing & Feature Engineering]
  ✓ Hourly aggregation to daily: 2 daily records produced
  ✓ Dry streak days calculation: [0.0, 0.0]
  ✓ Cyclical calendar features added: ['sin_dayofyear', 'cos_dayofyear', 'sin_month', 'cos_month']

================================================================
SUCCESS: nba_prep package (v0.4.0) verified for both AT1 & AT2!
================================================================
```

---

## Unit Testing & Quality Standards

The package is fully covered by 20 unit tests across 6 suites:

| Test Suite | Focus Area | Description |
| :--- | :--- | :--- |
| `tests/test_cleaning.py` | AT1 Data Cleaning | Validates `clean_height`, `clean_year`, and `calculate_age` edge cases, formats, and missing values. |
| `tests/test_features.py` | AT1 Basketball Metrics | Tests `calculate_ast_tov_ratio` (with division-by-zero epsilon), `calculate_true_shooting_percentage`, `calculate_defensive_impact`, and recruit/conference features. |
| `tests/test_cumulative.py` | AT1 Career Progression | Tests grouped multi-season player statistics, progression deltas, and peak career maximums to date. |
| `tests/test_analytics.py` | AT1 Decision Support | Tests 4-tier probability classification and qualitative text report generation. |
| `tests/test_evaluation.py` | AT1 Evaluation & ROI | Verifies AUPRC, AUROC, F1 optimization, and draft cap space financial analysis. |
| `tests/test_weather.py` | AT2 Weather Intelligence | Verifies Climate Comfort Index (0-100), component scores, Weather Hazard Category (0-3), hourly-to-daily aggregations, dry streak tracking, and cyclical calendar transforms. |

To execute the entire test suite locally:
```bash
pytest tests/ -v
```

---

## Related Repositories

- **Package Repository (TestPyPI):** [36120-26SP-group38-26040826-Python-package-Aryan-Goel](https://github.com/16aryan/36120-26SP-group38-26040826-Python-package-Aryan-Goel)
- **AT2 Experimentation Repository:** [36120-26SP-AT2-26040826-experiments](https://github.com/16aryan/36120-26SP-AT2-26040826-experiments)
- **AT2 FastAPI Deployment Repository:** [36120-26SP-AT2-26040826-api](https://github.com/16aryan/36120-26SP-AT2-26040826-api)

---

## Author & Academic Credit

- **Student:** Aryan Goel
- **Student ID:** 26040826
- **Institution:** University of Technology Sydney (UTS)
- **Subject:** 36120 — Advanced Machine Learning Applications
