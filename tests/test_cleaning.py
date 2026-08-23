import pytest
import numpy as np
from nba_prep.cleaning import clean_height, clean_year, calculate_age

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
