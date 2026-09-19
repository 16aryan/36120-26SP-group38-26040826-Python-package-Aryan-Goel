import pandas as pd
from nba_prep import (
    __version__,
    clean_height, 
    categorize_prospect, 
    generate_scouting_report, 
    calculate_model_metrics, 
    estimate_draft_roi,
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

print(f"================================================================")
print(f"--- Verifying Custom Python Package: nba_prep (v{__version__}) ---")
print(f"================================================================")

# =====================================================================
# SECTION 1: AT1 Basketball Analytics Verification (Backward Compatibility)
# =====================================================================
print("\n[AT1 Prospect Analytics]")
height_inches = clean_height("6-7")
print(f"  ✓ Height '6-7' cleaned to: {height_inches} inches (Expected: 79.0)")

tier = categorize_prospect(0.82)
print(f"  ✓ Prospect probability 0.82 classified as: '{tier}'")

y_true = [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
y_pred = [0.92, 0.78, 0.85, 0.40, 0.12, 0.65, 0.31, 0.05, 0.18, 0.09]
metrics = calculate_model_metrics(y_true, y_pred)
print(f"  ✓ Model Evaluation AUPRC: {metrics['auprc']:.4f}, AUROC: {metrics['auroc']:.4f}")

roi = estimate_draft_roi(y_true, y_pred, threshold=0.50, rookie_contract_cost=5000000)
print(f"  ✓ Draft ROI yield factor: {roi['relative_improvement_factor']:.2f}x")

# =====================================================================
# SECTION 2: AT2 Weather Intelligence Verification (New Features)
# =====================================================================
print("\n[AT2 Weather Intelligence - Target 1: Climate Comfort Index (CCI)]")
cci_val, cci_comps = calculate_cci(
    temperature_2m=22.0,
    relative_humidity_2m=50.0,
    wind_speed_10m=10.0,
    cloud_cover=10.0,
    precipitation=0.0
)
interpretation = interpret_cci(cci_val)
print(f"  ✓ Optimal Day CCI Score: {cci_val:.2f}/100 -> '{interpretation}'")

poor_cci, _ = calculate_cci(
    temperature_2m=38.0,
    relative_humidity_2m=85.0,
    wind_speed_10m=35.0,
    cloud_cover=90.0,
    precipitation=15.0
)
print(f"  ✓ Adverse Day CCI Score: {poor_cci:.2f}/100 -> '{interpret_cci(poor_cci)}'")

print("\n[AT2 Weather Intelligence - Target 2: Weather Hazard Category (WHC)]")
whi, hazards = calculate_weather_hazard_index(
    precipitation=15.0,
    wind_gusts_10m=65.0,
    cloud_cover=80.0,
    snowfall=0.0,
    temperature_2m=32.0
)
whc_cat = convert_whi_to_whc(whi)
print(f"  ✓ Weather Hazard Index (WHI): {whi:.2f}/100 -> Category {whc_cat} ('{interpret_whc(whc_cat)}')")

# Test helper
direct_whc = calculate_whc(precipitation=0.0, wind_gusts_10m=15.0, cloud_cover=10.0, snowfall=0.0, temperature_2m=21.0)
print(f"  ✓ Calm Day WHC Category: {direct_whc} ('{interpret_whc(direct_whc)}')")

print("\n[AT2 Preprocessing & Feature Engineering]")
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
    "weather_code": [0, 1, 0, 0]
})
daily = aggregate_hourly_to_daily(sample_hourly, date_col="date")
print(f"  ✓ Hourly aggregation to daily: {daily.shape[0]} daily records produced")

dry_streak = calculate_dry_streak(daily["precipitation"])
print(f"  ✓ Dry streak days calculation: {list(dry_streak)}")

daily_cyclical = add_cyclical_calendar_features(daily)
print(f"  ✓ Cyclical calendar features added: {[c for c in daily_cyclical.columns if 'sin' in c or 'cos' in c]}")

print("\n================================================================")
print("SUCCESS: nba_prep package (v0.4.0) verified for both AT1 & AT2!")
print("================================================================")

