import numpy as np

def calculate_ast_tov_ratio(ast, tov):
    """
    Calculates Assist-to-Turnover ratio, handling zero turnovers cleanly.
    """
    try:
        ast = np.array(ast, dtype=float)
        tov = np.array(tov, dtype=float)
        # For zero turnovers, divide by 1e-5 (or return a very high ratio)
        return np.where(tov == 0, ast / 1e-5, ast / tov)
    except Exception:
        return np.nan

def calculate_true_shooting_percentage(pts, fga, fta):
    """
    Calculates True Shooting Percentage: PTS / (2 * (FGA + 0.44 * FTA)).
    """
    try:
        pts = np.array(pts, dtype=float)
        fga = np.array(fga, dtype=float)
        fta = np.array(fta, dtype=float)
        denom = 2.0 * (fga + 0.44 * fta)
        return np.where(denom == 0, 0.0, pts / denom)
    except Exception:
        return np.nan

def calculate_defensive_impact(stl, blk, dreb):
    """
    A heuristic defensive score combining steals, blocks, and defensive rebounds.
    Formula: steals * 1.5 + blocks * 1.5 + defensive rebounds * 1.0.
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
    """
    try:
        pts = np.array(pts, dtype=float)
        min_per = np.array(min_per, dtype=float)
        return np.where(min_per == 0, 0.0, pts / min_per)
    except Exception:
        return np.nan
