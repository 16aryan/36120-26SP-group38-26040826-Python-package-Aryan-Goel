"""
nba_prep - Feature Engineering Utilities
This module calculates advanced basketball metrics, cumulative seasonal stats,
and recruiting/conference strength indices for NBA prospect evaluation.
"""

import numpy as np
import pandas as pd

def calculate_ast_tov_ratio(ast, tov):
    """
    Calculates Assist-to-Turnover ratio, handling zero turnovers cleanly.
    
    Parameters:
        ast (array-like): Assist count(s).
        tov (array-like): Turnover count(s).
        
    Returns:
        array/float: Assist-to-Turnover ratio, protected with an epsilon factor for zero turnovers.
    """
    try:
        ast = np.array(ast, dtype=float)
        tov = np.array(tov, dtype=float)
        safe_tov = np.where(tov == 0, 1e-5, tov)
        return np.where(tov == 0, ast / 1e-5, ast / safe_tov)
    except Exception:
        return np.nan

def calculate_true_shooting_percentage(pts, fga, fta):
    """
    Calculates True Shooting Percentage (TS%): PTS / (2 * (FGA + 0.44 * FTA)).
    TS% measures a player's shooting efficiency by taking 2FGs, 3FGs, and FTs into account.
    
    Parameters:
        pts (array-like): Points scored.
        fga (array-like): Field goal attempts.
        fta (array-like): Free throw attempts.
        
    Returns:
        array/float: True shooting percentage, or 0.0 if there are no attempts.
    """
    try:
        pts = np.array(pts, dtype=float)
        fga = np.array(fga, dtype=float)
        fta = np.array(fta, dtype=float)
        denom = 2.0 * (fga + 0.44 * fta)
        safe_denom = np.where(denom == 0, 1.0, denom)
        return np.where(denom == 0, 0.0, pts / safe_denom)
    except Exception:
        return np.nan

def calculate_defensive_impact(stl, blk, dreb):
    """
    Calculates a heuristic Defensive Impact score.
    Formula: steals * 1.5 + blocks * 1.5 + defensive rebounds * 1.0.
    
    Parameters:
        stl (array-like): Steal count(s).
        blk (array-like): Block count(s).
        dreb (array-like): Defensive rebound count(s).
        
    Returns:
        array/float: Defensive impact score, with missing values (NaNs) imputed to 0.0.
    """
    try:
        stl = np.array(stl, dtype=float)
        blk = np.array(blk, dtype=float)
        dreb = np.array(dreb, dtype=float)
        # Handle potential NaNs by replacing with 0 inside calculation
        stl = np.nan_to_num(stl, nan=0.0)
        blk = np.nan_to_num(blk, nan=0.0)
        dreb = np.nan_to_num(dreb, nan=0.0)
        return stl * 1.5 + blk * 1.5 + dreb * 1.0
    except Exception:
        return np.nan

def calculate_scoring_efficiency(pts, min_per):
    """
    Calculates scoring rate relative to playing time percentage.
    Formula: points / minutes_percentage.
    
    Parameters:
        pts (array-like): Points scored.
        min_per (array-like): Percentage of total game minutes played.
        
    Returns:
        array/float: Scoring efficiency score, or 0.0 if playing time is zero.
    """
    try:
        pts = np.array(pts, dtype=float)
        min_per = np.array(min_per, dtype=float)
        safe_min = np.where(min_per == 0, 1.0, min_per)
        return np.where(min_per == 0, 0.0, pts / safe_min)
    except Exception:
        return np.nan

def calculate_cumulative_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes cumulative stats, progression, and running metrics for players (grouped by pid).
    Assumes df has already been sorted by pid and year.
    
    Parameters:
        df (pd.DataFrame): Sorted player dataset.
        
    Returns:
        pd.DataFrame: Computed cumulative feature columns.
    """
    res = pd.DataFrame(index=df.index)
    
    # Calculate season index (1st season, 2nd season, etc.)
    res['career_season_num'] = df.groupby('pid').cumcount() + 1
    
    # Cumulative stats
    res['cum_GP'] = df.groupby('pid')['GP'].cumsum()
    res['cum_pts'] = df.groupby('pid')['pts'].cumsum()
    res['cum_ast'] = df.groupby('pid')['ast'].cumsum()
    res['cum_stl'] = df.groupby('pid')['stl'].cumsum()
    res['cum_blk'] = df.groupby('pid')['blk'].cumsum()
    res['cum_treb'] = df.groupby('pid')['treb'].cumsum()
    res['cum_stops'] = df.groupby('pid')['stops'].cumsum()
    
    # Cumulative means (mean per season up to current)
    res['cum_mean_bpm'] = df.groupby('pid')['bpm'].cumsum() / res['career_season_num']
    res['cum_mean_porpag'] = df.groupby('pid')['porpag'].cumsum() / res['career_season_num']
    res['cum_mean_dporpag'] = df.groupby('pid')['dporpag'].cumsum() / res['career_season_num']
    res['cum_mean_pts'] = df.groupby('pid')['pts'].cumsum() / res['career_season_num']
    res['cum_mean_ast'] = df.groupby('pid')['ast'].cumsum() / res['career_season_num']
    res['cum_mean_treb'] = df.groupby('pid')['treb'].cumsum() / res['career_season_num']
    res['cum_mean_stl'] = df.groupby('pid')['stl'].cumsum() / res['career_season_num']
    res['cum_mean_blk'] = df.groupby('pid')['blk'].cumsum() / res['career_season_num']
    res['cum_mean_usg'] = df.groupby('pid')['usg'].cumsum() / res['career_season_num']
    res['cum_mean_min_per'] = df.groupby('pid')['Min_per'].cumsum() / res['career_season_num']
    
    # Running maximums (capture player's single-season peaks up to current)
    res['max_bpm_to_date'] = df.groupby('pid')['bpm'].cummax()
    res['max_porpag_to_date'] = df.groupby('pid')['porpag'].cummax()
    res['max_dporpag_to_date'] = df.groupby('pid')['dporpag'].cummax()
    res['max_pts_to_date'] = df.groupby('pid')['pts'].cummax()
    res['max_ast_to_date'] = df.groupby('pid')['ast'].cummax()
    res['max_treb_to_date'] = df.groupby('pid')['treb'].cummax()
    res['max_stl_to_date'] = df.groupby('pid')['stl'].cummax()
    res['max_blk_to_date'] = df.groupby('pid')['blk'].cummax()
    res['max_usg_to_date'] = df.groupby('pid')['usg'].cummax()
    res['max_min_per_to_date'] = df.groupby('pid')['Min_per'].cummax()
    
    # Year-over-year progression (difference from previous season to capture development velocity)
    res['bpm_progression'] = df.groupby('pid')['bpm'].diff().fillna(0.0)
    res['pts_progression'] = df.groupby('pid')['pts'].diff().fillna(0.0)
    res['porpag_progression'] = df.groupby('pid')['porpag'].diff().fillna(0.0)
    
    return res

def calculate_advanced_recruit_and_conference_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes recruiting rank indicators, major conference flags, and per-minute statistics.
    
    Parameters:
        df (pd.DataFrame): Dataset containing recruit rank, conf, and playing time metrics.
        
    Returns:
        pd.DataFrame: Computed recruit and conference indicators.
    """
    res = pd.DataFrame(index=df.index)
    
    # Recruiting rank cleaning
    res['has_rec_rank'] = df['Rec Rank'].notna().astype(float)
    res['rec_rank_filled'] = df['Rec Rank'].fillna(150.0)  # Fill missing recruiting ranks with a default baseline (150th)
    
    # High-major power conferences flag loaded from external configurations if available
    import os
    external_path = os.path.join("data", "external", "major_conferences.csv")
    if os.path.exists(external_path):
        try:
            ext_df = pd.read_csv(external_path)
            major_confs = set(ext_df[ext_df["is_power_conference"] == 1]["conf"].dropna().unique())
        except Exception:
            major_confs = {'ACC', 'SEC', 'B10', 'B12', 'BE', 'P10', 'P12'}
    else:
        # Standard fallback power conferences
        major_confs = {'ACC', 'SEC', 'B10', 'B12', 'BE', 'P10', 'P12'}
        
    res['is_major_conf'] = df['conf'].isin(major_confs).astype(float)
    
    # Per-minute features (with zero-minute safety epsilon to prevent NaN/Inf)
    mp_safe = np.where(df['mp'] == 0, 1e-5, df['mp'])
    res['pts_per_min'] = df['pts'] / mp_safe
    res['ast_per_min'] = df['ast'] / mp_safe
    res['stl_per_min'] = df['stl'] / mp_safe
    res['blk_per_min'] = df['blk'] / mp_safe
    res['treb_per_min'] = df['treb'] / mp_safe
    
    return res



