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

def test_calculate_ast_tov_ratio():
    assert calculate_ast_tov_ratio(10, 2) == pytest.approx(5.0)
    assert calculate_ast_tov_ratio(10, 0) == pytest.approx(1000000.0)  # default epsilon 1e-5

def test_calculate_true_shooting_percentage():
    # PTS=20, FGA=10, FTA=5
    # true_shooting = 20 / (2 * (10 + 0.44 * 5)) = 20 / (2 * 12.2) = 20 / 24.4
    assert calculate_true_shooting_percentage(20, 10, 5) == pytest.approx(20.0 / 24.4)

def test_calculate_defensive_impact():
    # stl=2, blk=3, dreb=4
    # impact = 2*1.5 + 3*1.5 + 4*1.0 = 3 + 4.5 + 4 = 11.5
    assert calculate_defensive_impact(2, 3, 4) == 11.5

def test_calculate_scoring_efficiency():
    # pts=15, min_per=50
    assert calculate_scoring_efficiency(15, 50) == pytest.approx(0.3)

def test_calculate_advanced_recruit_and_conference_features():
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
    assert res.loc[0, 'has_rec_rank'] == 1.0
    assert res.loc[1, 'has_rec_rank'] == 0.0
    assert res.loc[1, 'rec_rank_filled'] == 150.0
    assert res.loc[0, 'is_major_conf'] == 1.0
    assert res.loc[1, 'is_major_conf'] == 0.0
    assert res.loc[0, 'pts_per_min'] == 0.5
