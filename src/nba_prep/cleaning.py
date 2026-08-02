import pandas as pd
import numpy as np

def clean_height(ht_str):
    """
    Converts height string in feet-inches format (e.g. '6-7') to numeric inches (e.g. 79.0).
    Returns np.nan if format is invalid or missing.
    """
    if pd.isna(ht_str) or not isinstance(ht_str, str):
        return np.nan
    try:
        parts = ht_str.split("-")
        if len(parts) == 2:
            return float(int(parts[0]) * 12 + int(parts[1]))
    except Exception:
        pass
    return np.nan

def clean_year(yr_str):
    """
    Cleans year category (e.g. 'Fr', 'So', 'Jr', 'Sr') into standard integers (1 to 4).
    Handles string numeric values and ignores noise.
    """
    if pd.isna(yr_str):
        return np.nan
    yr_str = str(yr_str).strip()
    mapping = {"Fr": 1, "So": 2, "Jr": 3, "Sr": 4}
    if yr_str in mapping:
        return mapping[yr_str]
    try:
        val = float(yr_str)
        if val == 0.0 or val == 0:
            return np.nan
        if val in [1.0, 2.0, 3.0, 4.0]:
            return int(val)
    except Exception:
        pass
    return np.nan

def calculate_age(season_year, dob_str):
    """
    Calculates the player's age in years during a season from DOB string and season year.
    Returns np.nan if DOB or season_year is missing or invalid.
    """
    if pd.isna(season_year) or pd.isna(dob_str):
        return np.nan
    try:
        dob_dt = pd.to_datetime(dob_str, errors="coerce")
        if pd.isna(dob_dt):
            return np.nan
        return float(season_year - dob_dt.year)
    except Exception:
        pass
    return np.nan
