import pytest
import numpy as np
import pandas as pd
from nba_prep.features import (
    calculate_ast_tov_ratio,
    calculate_true_shooting_percentage,
    calculate_defensive_impact,
    calculate_scoring_efficiency,
    calculate_advanced_recruit_and_conference_features,
)

# ==============================================================================
# TEST SUITE: ADVANCED BASKETBALL FEATURE CALCULATIONS
# ==============================================================================
# This suite verifies that custom statistical metrics are computed accurately,
# including handling edge-cases like division-by-zero or missing values.

def test_calculate_ast_tov_ratio():
    """
    Test Assist-to-Turnover Ratio.
    Verifies regular division, and validates safety guard against division by zero (using epsilon).
    """
    assert calculate_ast_tov_ratio(10, 2) == pytest.approx(5.0)
    assert calculate_ast_tov_ratio(10, 0) == pytest.approx(1000000.0)  # default epsilon 1e-5 used as denominator

def test_calculate_true_shooting_percentage():
    """
    Test True Shooting Percentage (TS%).
    Calculates standard efficiency: PTS / (2 * (FGA + 0.44 * FTA)).
    """
    # Formula: 20 / (2 * (10 + 0.44 * 5)) = 20 / (2 * 12.2) = 20 / 24.4
    assert calculate_true_shooting_percentage(20, 10, 5) == pytest.approx(20.0 / 24.4)

def test_calculate_defensive_impact():
    """
    Test custom weighted Defensive Impact Score.
    Weights: stl * 1.5 + blk * 1.5 + dreb * 1.0.
    """
    # Formula: 2*1.5 + 3*1.5 + 4*1.0 = 3 + 4.5 + 4 = 11.5
    assert calculate_defensive_impact(2, 3, 4) == 11.5

def test_calculate_scoring_efficiency():
    """
    Test Scoring Efficiency relative to minute percentage allocation.
    Formula: pts / min_per.
    """
    # Formula: 15 / 50 = 0.30
    assert calculate_scoring_efficiency(15, 50) == pytest.approx(0.3)

def test_calculate_advanced_recruit_and_conference_features():
    """
    Test advanced features involving high-school recruiting rank and conference status.
    Verifies:
      - Fill missing recruiting rank with a default (150.0).
      - Binary index flag 'has_rec_rank' creation.
      - Power/major conference detection from list of strings.
      - Points-per-minute rate generation.
    """
    df = pd.DataFrame({
        'Rec Rank': [10.0, np.nan],
        'conf': ['ACC', 'WAC'],
        'mp': [30.0, 0.0],
        'pts': [15.0, 0.0],
        'ast': [3.0, 0.0],
        'stl': [1.5, 0.0],
        'blk': [0.6, 0.0],
        'treb': [6.0, 0.0]
    })
    res = calculate_advanced_recruit_and_conference_features(df)
    
    # Assert Recruiting Rank attributes
    assert res.loc[0, 'has_rec_rank'] == 1.0
    assert res.loc[1, 'has_rec_rank'] == 0.0
    assert res.loc[1, 'rec_rank_filled'] == 150.0  # NaN filled with default 150
    
    # Assert Conference Classification (ACC is a major conf, WAC is mid-major)
    assert res.loc[0, 'is_major_conf'] == 1.0
    assert res.loc[1, 'is_major_conf'] == 0.0
    
    # Assert production rate features (15 pts / 30 mins = 0.5 pts/min)
    assert res.loc[0, 'pts_per_min'] == 0.5

