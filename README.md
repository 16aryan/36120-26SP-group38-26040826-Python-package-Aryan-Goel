# nba_prep

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

