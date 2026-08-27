"""
nba_prep - Data Cleaning Utilities
This module provides functions to parse, clean, and standardize raw player attributes
such as heights, academic class years, and birthdays.
"""

import pandas as pd
import numpy as np

def clean_height(ht_str):
    """
    Converts height string in feet-inches format (e.g. '6-7') to numeric inches (e.g. 79.0).
    
    Parameters:
        ht_str (str): The height representation (e.g., "6-8" or "5-11").
        
    Returns:
        float: Height in inches, or np.nan if format is invalid or missing.
    """
    if pd.isna(ht_str) or not isinstance(ht_str, str):
        return np.nan
    try:
        parts = ht_str.split("-")
        if len(parts) == 2:
            # 1 foot = 12 inches
            return float(int(parts[0]) * 12 + int(parts[1]))
    except Exception:
        pass
    return np.nan

def clean_year(yr_str):
    """
    Cleans year category (e.g. 'Fr', 'So', 'Jr', 'Sr') into standard integers (1 to 4).
    Handles string numeric values and ignores noise.
    
    Parameters:
        yr_str (str/float): The class year category description.
        
    Returns:
        int: The standardized academic sequence number (1-4), or np.nan if invalid.
    """
    if pd.isna(yr_str):
        return np.nan
    yr_str = str(yr_str).strip()
    
    # Map class strings to chronological levels
    mapping = {"Fr": 1, "So": 2, "Jr": 3, "Sr": 4}
    if yr_str in mapping:
        return mapping[yr_str]
        
    try:
        val = float(yr_str)
        # 0.0 or other indices are invalid
        if val == 0.0 or val == 0:
            return np.nan
        # If float represents 1.0, 2.0, 3.0, 4.0, cast to int
        if val in [1.0, 2.0, 3.0, 4.0]:
            return int(val)
    except Exception:
        pass
    return np.nan

def calculate_age(season_year, dob_str):
    """
    Calculates the player's age in years during a season from DOB string and season year.
    
    Parameters:
        season_year (int): Calendar year of the season (e.g. 2021).
        dob_str (str): Date of birth string representation (YYYY-MM-DD).
        
    Returns:
        float: Estimated age in years, or np.nan if DOB or season_year is missing or invalid.
    """
    if pd.isna(season_year) or pd.isna(dob_str):
        return np.nan
    try:
        dob_dt = pd.to_datetime(dob_str, errors="coerce")
        if pd.isna(dob_dt):
            return np.nan
        # Subtract birth year from season calendar year
        return float(season_year - dob_dt.year)
    except Exception:
        pass
    return np.nan

