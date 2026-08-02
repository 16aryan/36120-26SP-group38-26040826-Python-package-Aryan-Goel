import pytest
import numpy as np
from nba_prep.cleaning import clean_height, clean_year, calculate_age
from nba_prep.features import (
    calculate_ast_tov_ratio,
    calculate_true_shooting_percentage,
    calculate_defensive_impact,
    calculate_scoring_efficiency,
)

def test_clean_height():
    assert clean_height("6-7") == 79.0
    assert clean_height("6-2") == 74.0
    assert np.isnan(clean_height(None))
    assert np.isnan(clean_height("invalid"))
    assert np.isnan(clean_height(6.7))

def test_clean_year():
    assert clean_year("Fr") == 1
    assert clean_year("So") == 2
    assert clean_year("Jr") == 3
    assert clean_year("Sr") == 4
    assert clean_year(" 2.0 ") == 2
    assert np.isnan(clean_year("invalid"))
    assert np.isnan(clean_year(None))
    assert np.isnan(clean_year(0.0))

def test_calculate_age():
    assert calculate_age(2020, "1997-10-15") == 23.0
    assert np.isnan(calculate_age(2020, None))
    assert np.isnan(calculate_age(None, "1997-10-15"))
    assert np.isnan(calculate_age(2020, "invalid-date"))

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
