"""
nba_prep Package Initializer

Exposes core modules and utility functions for:
1. Collegiate basketball prospect cleaning, analytics, and longevity modeling (AT1).
2. Weather Intelligence, Climate Comfort Index (CCI), Weather Hazard Category (WHC),
   and meteorological aggregation/feature engineering (AT2).
"""

# AT1 Basketball Modules
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

# AT2 Weather Intelligence Modules
from .weather import (
    calculate_temp_score,
    calculate_humidity_score,
    calculate_wind_score,
    calculate_cloud_score,
    calculate_rain_score,
    calculate_climate_comfort_index,
    interpret_cci,
    calculate_rain_hazard,
    calculate_wind_hazard,
    calculate_cloud_hazard,
    calculate_snow_hazard,
    calculate_temp_hazard,
    calculate_weather_hazard_index,
    convert_whi_to_whc,
    interpret_whc,
    WHC_LABEL_TO_NAME,
    aggregate_hourly_to_daily,
    add_cyclical_calendar_features,
    calculate_dry_streak,
)

__version__ = "0.4.0"

__all__ = [
    "__version__",
    # AT1 Exports
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
    # AT2 Weather Exports
    "calculate_temp_score",
    "calculate_humidity_score",
    "calculate_wind_score",
    "calculate_cloud_score",
    "calculate_rain_score",
    "calculate_climate_comfort_index",
    "interpret_cci",
    "calculate_rain_hazard",
    "calculate_wind_hazard",
    "calculate_cloud_hazard",
    "calculate_snow_hazard",
    "calculate_temp_hazard",
    "calculate_weather_hazard_index",
    "convert_whi_to_whc",
    "interpret_whc",
    "WHC_LABEL_TO_NAME",
    "aggregate_hourly_to_daily",
    "add_cyclical_calendar_features",
    "calculate_dry_streak",
]
