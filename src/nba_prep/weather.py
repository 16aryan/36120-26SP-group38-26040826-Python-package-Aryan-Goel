"""
Weather Intelligence Module (AT2 Extension)

This module provides reusable utilities for weather data processing,
target variable derivations (Climate Comfort Index and Weather Hazard Category),
daily temporal aggregations, and feature engineering for weather forecasting.
"""

from typing import Dict, List, Tuple, Union
import numpy as np
import pandas as pd


def _preserve_type(result: np.ndarray, original: Union[pd.Series, np.ndarray, float]) -> Union[pd.Series, np.ndarray, float]:
    """Helper to preserve pandas Series or scalar types from numpy operations."""
    if isinstance(original, pd.Series):
        return pd.Series(result, index=original.index)
    elif isinstance(original, (int, float, np.number)):
        return float(result)
    return result


# =====================================================================
# Target 1: Climate Comfort Index (CCI) - Regression
# =====================================================================

def calculate_temp_score(temperature_2m: Union[pd.Series, np.ndarray, float]) -> Union[pd.Series, np.ndarray, float]:
    """TempScore = MAX(0, 1 - ABS(temperature_2m - 22) / 20)"""
    res = np.maximum(0.0, 1.0 - np.abs(np.asanyarray(temperature_2m) - 22.0) / 20.0)
    return _preserve_type(res, temperature_2m)


def calculate_humidity_score(relative_humidity_2m: Union[pd.Series, np.ndarray, float]) -> Union[pd.Series, np.ndarray, float]:
    """HumidityScore = MAX(0, 1 - ABS(relative_humidity_2m - 50) / 50)"""
    res = np.maximum(0.0, 1.0 - np.abs(np.asanyarray(relative_humidity_2m) - 50.0) / 50.0)
    return _preserve_type(res, relative_humidity_2m)


def calculate_wind_score(wind_speed_10m: Union[pd.Series, np.ndarray, float]) -> Union[pd.Series, np.ndarray, float]:
    """WindScore = MAX(0, 1 - ABS(wind_speed_10m - 10) / 40)"""
    res = np.maximum(0.0, 1.0 - np.abs(np.asanyarray(wind_speed_10m) - 10.0) / 40.0)
    return _preserve_type(res, wind_speed_10m)


def calculate_cloud_score(cloud_cover: Union[pd.Series, np.ndarray, float]) -> Union[pd.Series, np.ndarray, float]:
    """CloudScore = MAX(0, 1 - cloud_cover / 100)"""
    res = np.maximum(0.0, 1.0 - np.asanyarray(cloud_cover) / 100.0)
    return _preserve_type(res, cloud_cover)


def calculate_rain_score(precipitation: Union[pd.Series, np.ndarray, float]) -> Union[pd.Series, np.ndarray, float]:
    """RainScore = MAX(0, 1 - precipitation / 20)"""
    res = np.maximum(0.0, 1.0 - np.asanyarray(precipitation) / 20.0)
    return _preserve_type(res, precipitation)


def calculate_climate_comfort_index(
    temperature_2m: Union[pd.Series, np.ndarray, float],
    relative_humidity_2m: Union[pd.Series, np.ndarray, float],
    wind_speed_10m: Union[pd.Series, np.ndarray, float],
    cloud_cover: Union[pd.Series, np.ndarray, float],
    precipitation: Union[pd.Series, np.ndarray, float],
) -> Tuple[Union[pd.Series, np.ndarray, float], Dict[str, Union[pd.Series, np.ndarray, float]]]:
    """Calculate the Climate Comfort Index (CCI) and its component scores.

    CCI = 100 * (0.35*TempScore + 0.20*HumidityScore + 0.15*WindScore + 0.15*CloudScore + 0.15*RainScore)
    Range: 0 to 100. Higher values indicate more comfortable outdoor conditions.
    """
    temp_score = calculate_temp_score(temperature_2m)
    humidity_score = calculate_humidity_score(relative_humidity_2m)
    wind_score = calculate_wind_score(wind_speed_10m)
    cloud_score = calculate_cloud_score(cloud_cover)
    rain_score = calculate_rain_score(precipitation)

    cci = 100.0 * (
        0.35 * temp_score
        + 0.20 * humidity_score
        + 0.15 * wind_score
        + 0.15 * cloud_score
        + 0.15 * rain_score
    )

    components = {
        "temp_score": temp_score,
        "humidity_score": humidity_score,
        "wind_score": wind_score,
        "cloud_score": cloud_score,
        "rain_score": rain_score,
    }
    return cci, components


calculate_cci = calculate_climate_comfort_index


def interpret_cci(score: float) -> str:
    """Return textual interpretation for a CCI score according to AT2 brief."""
    val = float(score)
    if val >= 80:
        return "Excellent outdoor conditions"
    elif val >= 60:
        return "Comfortable conditions"
    elif val >= 40:
        return "Moderate comfort"
    elif val >= 20:
        return "Poor comfort"
    else:
        return "Very poor comfort"


# =====================================================================
# Target 2: Weather Hazard Category (WHC) - Multiclass Classification
# =====================================================================

def calculate_rain_hazard(precipitation: Union[pd.Series, np.ndarray, float]) -> Union[pd.Series, np.ndarray, float]:
    """RainHazard = MIN(precipitation / 30, 1)"""
    res = np.minimum(np.asanyarray(precipitation) / 30.0, 1.0)
    return _preserve_type(res, precipitation)


def calculate_wind_hazard(wind_gusts_10m: Union[pd.Series, np.ndarray, float]) -> Union[pd.Series, np.ndarray, float]:
    """WindHazard = MIN(wind_gusts_10m / 100, 1)"""
    res = np.minimum(np.asanyarray(wind_gusts_10m) / 100.0, 1.0)
    return _preserve_type(res, wind_gusts_10m)


def calculate_cloud_hazard(cloud_cover: Union[pd.Series, np.ndarray, float]) -> Union[pd.Series, np.ndarray, float]:
    """CloudHazard = MIN(cloud_cover / 100, 1)"""
    res = np.minimum(np.asanyarray(cloud_cover) / 100.0, 1.0)
    return _preserve_type(res, cloud_cover)


def calculate_snow_hazard(snowfall: Union[pd.Series, np.ndarray, float]) -> Union[pd.Series, np.ndarray, float]:
    """SnowHazard = MIN(snowfall / 15, 1)"""
    res = np.minimum(np.asanyarray(snowfall) / 15.0, 1.0)
    return _preserve_type(res, snowfall)


def calculate_temp_hazard(temperature_2m: Union[pd.Series, np.ndarray, float]) -> Union[pd.Series, np.ndarray, float]:
    """TempHazard = MIN(ABS(temperature_2m - 22) / 25, 1)"""
    res = np.minimum(np.abs(np.asanyarray(temperature_2m) - 22.0) / 25.0, 1.0)
    return _preserve_type(res, temperature_2m)


def calculate_weather_hazard_index(
    precipitation: Union[pd.Series, np.ndarray, float],
    wind_gusts_10m: Union[pd.Series, np.ndarray, float],
    cloud_cover: Union[pd.Series, np.ndarray, float],
    snowfall: Union[pd.Series, np.ndarray, float],
    temperature_2m: Union[pd.Series, np.ndarray, float],
) -> Tuple[Union[pd.Series, np.ndarray, float], Dict[str, Union[pd.Series, np.ndarray, float]]]:
    """Calculate Weather Hazard Index (WHI) and its component hazard scores.

    WHI = 100 * (0.30*RainHazard + 0.30*WindHazard + 0.20*CloudHazard + 0.10*SnowHazard + 0.10*TempHazard)
    """
    rain_h = calculate_rain_hazard(precipitation)
    wind_h = calculate_wind_hazard(wind_gusts_10m)
    cloud_h = calculate_cloud_hazard(cloud_cover)
    snow_h = calculate_snow_hazard(snowfall)
    temp_h = calculate_temp_hazard(temperature_2m)

    whi = 100.0 * (
        0.30 * rain_h
        + 0.30 * wind_h
        + 0.20 * cloud_h
        + 0.10 * snow_h
        + 0.10 * temp_h
    )

    hazards = {
        "rain_hazard": rain_h,
        "wind_hazard": wind_h,
        "cloud_hazard": cloud_h,
        "snow_hazard": snow_h,
        "temp_hazard": temp_h,
    }
    return whi, hazards


def convert_whi_to_whc(whi: Union[pd.Series, np.ndarray, float]) -> Union[pd.Series, np.ndarray, int]:
    """Convert continuous WHI into 4 multiclass classification labels (0, 1, 2, 3).

    - WHI < 25       -> 0 (Low Risk)
    - 25 <= WHI < 50 -> 1 (Moderate Risk)
    - 50 <= WHI < 75 -> 2 (High Risk)
    - WHI >= 75      -> 3 (Extreme Risk)
    """
    whi_arr = np.asanyarray(whi)
    conditions = [
        (whi_arr < 25.0),
        (whi_arr >= 25.0) & (whi_arr < 50.0),
        (whi_arr >= 50.0) & (whi_arr < 75.0),
        (whi_arr >= 75.0),
    ]
    choices = [0, 1, 2, 3]
    result = np.select(conditions, choices, default=0)
    if isinstance(whi, pd.Series):
        return pd.Series(result, index=whi.index)
    elif np.ndim(whi) == 0:
        return int(result)
    return result


def calculate_whc(
    precipitation: Union[pd.Series, np.ndarray, float],
    wind_gusts_10m: Union[pd.Series, np.ndarray, float],
    cloud_cover: Union[pd.Series, np.ndarray, float],
    snowfall: Union[pd.Series, np.ndarray, float],
    temperature_2m: Union[pd.Series, np.ndarray, float],
) -> Union[pd.Series, np.ndarray, int]:
    """Convenience helper to compute WHC category (0, 1, 2, 3) directly from weather variables."""
    whi, _ = calculate_weather_hazard_index(
        precipitation=precipitation,
        wind_gusts_10m=wind_gusts_10m,
        cloud_cover=cloud_cover,
        snowfall=snowfall,
        temperature_2m=temperature_2m,
    )
    return convert_whi_to_whc(whi)


WHC_LABEL_TO_NAME: Dict[int, str] = {
    0: "Low Risk",
    1: "Moderate Risk",
    2: "High Risk",
    3: "Extreme Risk",
}


def interpret_whc(label: int) -> str:
    """Return textual interpretation for a WHC class label."""
    return WHC_LABEL_TO_NAME.get(int(label), "Unknown Risk")


# =====================================================================
# Preprocessing: Hourly-to-Daily Aggregation
# =====================================================================

def aggregate_hourly_to_daily(hourly_df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Aggregate raw hourly Open-Meteo observations to daily values strictly per AT2 rules.

    Aggregation specifications:
    - Temperature (temperature_2m): Daily Mean
    - Relative Humidity (relative_humidity_2m): Daily Mean
    - Wind Speed (wind_speed_10m): Daily Mean
    - Cloud Cover (cloud_cover): Daily Mean
    - Precipitation (precipitation): Daily Total (sum)
    - Wind Gusts (wind_gusts_10m): Daily Maximum (max)
    - Snowfall (snowfall): Daily Total (sum)
    """
    df = hourly_df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])

    df["day"] = df[date_col].dt.date

    agg_rules = {}
    if "temperature_2m" in df.columns:
        agg_rules["temperature_2m"] = "mean"
    if "relative_humidity_2m" in df.columns:
        agg_rules["relative_humidity_2m"] = "mean"
    if "wind_speed_10m" in df.columns:
        agg_rules["wind_speed_10m"] = "mean"
    if "cloud_cover" in df.columns:
        agg_rules["cloud_cover"] = "mean"
    if "precipitation" in df.columns:
        agg_rules["precipitation"] = "sum"
    if "wind_gusts_10m" in df.columns:
        agg_rules["wind_gusts_10m"] = "max"
    if "snowfall" in df.columns:
        agg_rules["snowfall"] = "sum"

    daily = df.groupby("day").agg(agg_rules).reset_index()
    daily.rename(columns={"day": "date"}, inplace=True)
    daily["date"] = pd.to_datetime(daily["date"])
    return daily


# =====================================================================
# Feature Engineering Helpers
# =====================================================================

def add_cyclical_calendar_features(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Add smooth trigonometric calendar encodings (sine & cosine)."""
    res = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(res[date_col]):
        res[date_col] = pd.to_datetime(res[date_col])

    day_of_year = res[date_col].dt.dayofyear
    month = res[date_col].dt.month

    res["sin_dayofyear"] = np.sin(2 * np.pi * day_of_year / 365.25)
    res["cos_dayofyear"] = np.cos(2 * np.pi * day_of_year / 365.25)
    res["sin_month"] = np.sin(2 * np.pi * month / 12.0)
    res["cos_month"] = np.cos(2 * np.pi * month / 12.0)
    return res


def calculate_dry_streak(precipitation_series: pd.Series, threshold: float = 1.0) -> pd.Series:
    """Calculate consecutive dry days prior to prediction day with strict shift(1) (zero leakage)."""
    is_rainy = (precipitation_series >= threshold).astype(int)
    dry_streak = is_rainy.eq(0).astype(int).groupby(
        is_rainy.eq(1).cumsum()
    ).cumsum().shift(1).fillna(0)
    return dry_streak
