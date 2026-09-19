"""
Unit tests for the Weather Intelligence module (AT2).
"""

import numpy as np
import pandas as pd
import pytest

from nba_prep.weather import (
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
    aggregate_hourly_to_daily,
    add_cyclical_calendar_features,
    calculate_dry_streak,
)


def test_cci_component_scores():
    # Temp optimal at 22C
    assert calculate_temp_score(22.0) == pytest.approx(1.0)
    assert calculate_temp_score(42.0) == pytest.approx(0.0)
    assert calculate_temp_score(50.0) == pytest.approx(0.0)  # non-negative

    # Humidity optimal at 50%
    assert calculate_humidity_score(50.0) == pytest.approx(1.0)
    assert calculate_humidity_score(0.0) == pytest.approx(0.0)
    assert calculate_humidity_score(100.0) == pytest.approx(0.0)

    # Wind optimal at 10 km/h
    assert calculate_wind_score(10.0) == pytest.approx(1.0)
    assert calculate_wind_score(50.0) == pytest.approx(0.0)

    # Cloud optimal at 0%
    assert calculate_cloud_score(0.0) == pytest.approx(1.0)
    assert calculate_cloud_score(100.0) == pytest.approx(0.0)

    # Rain optimal at 0mm
    assert calculate_rain_score(0.0) == pytest.approx(1.0)
    assert calculate_rain_score(20.0) == pytest.approx(0.0)
    assert calculate_rain_score(50.0) == pytest.approx(0.0)


def test_climate_comfort_index_ideal():
    cci, comps = calculate_climate_comfort_index(
        temperature_2m=22.0,
        relative_humidity_2m=50.0,
        wind_speed_10m=10.0,
        cloud_cover=0.0,
        precipitation=0.0,
    )
    assert cci == pytest.approx(100.0)
    assert interpret_cci(cci) == "Excellent outdoor conditions"


def test_climate_comfort_index_series():
    temp = pd.Series([22.0, 45.0])
    hum = pd.Series([50.0, 10.0])
    wind = pd.Series([10.0, 60.0])
    cloud = pd.Series([0.0, 100.0])
    rain = pd.Series([0.0, 40.0])

    cci, _ = calculate_climate_comfort_index(temp, hum, wind, cloud, rain)
    assert cci.iloc[0] == pytest.approx(100.0)
    assert (cci >= 0.0).all() and (cci <= 100.0).all()


def test_whc_hazard_scores():
    assert calculate_rain_hazard(0.0) == pytest.approx(0.0)
    assert calculate_rain_hazard(30.0) == pytest.approx(1.0)
    assert calculate_rain_hazard(60.0) == pytest.approx(1.0)

    assert calculate_wind_hazard(0.0) == pytest.approx(0.0)
    assert calculate_wind_hazard(100.0) == pytest.approx(1.0)

    assert calculate_cloud_hazard(0.0) == pytest.approx(0.0)
    assert calculate_cloud_hazard(100.0) == pytest.approx(1.0)

    assert calculate_snow_hazard(0.0) == pytest.approx(0.0)
    assert calculate_snow_hazard(15.0) == pytest.approx(1.0)

    assert calculate_temp_hazard(22.0) == pytest.approx(0.0)
    assert calculate_temp_hazard(47.0) == pytest.approx(1.0)


def test_whc_classification_and_interpretation():
    # Low risk < 25
    assert convert_whi_to_whc(10.0) == 0
    assert interpret_whc(0) == "Low Risk"

    # Moderate risk 25 <= whi < 50
    assert convert_whi_to_whc(35.0) == 1
    assert interpret_whc(1) == "Moderate Risk"

    # High risk 50 <= whi < 75
    assert convert_whi_to_whc(65.0) == 2
    assert interpret_whc(2) == "High Risk"

    # Extreme risk >= 75
    assert convert_whi_to_whc(85.0) == 3
    assert interpret_whc(3) == "Extreme Risk"


def test_aggregate_hourly_to_daily():
    dates = pd.date_range("2024-01-01", periods=24, freq="h")
    df = pd.DataFrame({
        "date": dates,
        "temperature_2m": [20.0] * 24,
        "precipitation": [0.5] * 24,
        "wind_gusts_10m": list(range(24)),
    })
    daily = aggregate_hourly_to_daily(df)
    assert len(daily) == 1
    assert daily["temperature_2m"].iloc[0] == pytest.approx(20.0)   # mean
    assert daily["precipitation"].iloc[0] == pytest.approx(12.0)    # sum (0.5 * 24)
    assert daily["wind_gusts_10m"].iloc[0] == pytest.approx(23.0)   # max


def test_cyclical_features_and_dry_streak():
    dates = pd.date_range("2024-01-01", periods=5, freq="D")
    df = pd.DataFrame({"date": dates, "precipitation": [0.0, 0.0, 5.0, 0.0, 0.0]})
    cyclical = add_cyclical_calendar_features(df)
    assert "sin_dayofyear" in cyclical.columns
    assert "cos_dayofyear" in cyclical.columns

    streak = calculate_dry_streak(df["precipitation"])
    # Day 0: no prior days -> 0
    # Day 1: 1 dry day prior -> 1
    # Day 2: 2 dry days prior -> 2
    # Day 3: rain occurred on day 2 -> 0
    # Day 4: 1 dry day prior -> 1
    assert list(streak) == [0.0, 1.0, 2.0, 0.0, 1.0]
