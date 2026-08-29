"""
nba_prep Package Initializer
Exposes core modules and utility functions for cleaning, feature engineering,
scouting analytics, and model evaluation of collegiate basketball prospects.
"""

from .cleaning import clean_height, clean_year, calculate_age
from .features import (
    calculate_ast_tov_ratio,
    calculate_true_shooting_percentage,
    calculate_defensive_impact,
    calculate_scoring_efficiency,
    calculate_cumulative_features,
    calculate_advanced_recruit_and_conference_features,
)
from .analytics import categorize_prospect, generate_scouting_report
from .evaluation import calculate_model_metrics, estimate_draft_roi

__version__ = "0.3.3"

# Define clean namespace exports for the library package
__all__ = [
    "__version__",
    "clean_height",
    "clean_year",
    "calculate_age",
    "calculate_ast_tov_ratio",
    "calculate_true_shooting_percentage",
    "calculate_defensive_impact",
    "calculate_scoring_efficiency",
    "calculate_cumulative_features",
    "calculate_advanced_recruit_and_conference_features",
    "categorize_prospect",
    "generate_scouting_report",
    "calculate_model_metrics",
    "estimate_draft_roi",
]

