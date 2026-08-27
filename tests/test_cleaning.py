import pytest
import numpy as np
from nba_prep.cleaning import clean_height, clean_year, calculate_age

# ==============================================================================
# TEST SUITE: DATA CLEANING UTILITIES
# ==============================================================================
# This suite verifies input cleaning functions which resolve dirty raw datasets,
# such as parsing height strings, standardizing college year codes, and
# computing age based on birth dates and season years.

def test_clean_height():
    """
    Test conversion of height strings (feet-inches) to numeric inches.
    Ensures standard formats (e.g., '6-7') are correctly parsed, and
    verifies that missing/null values and malformed strings safely return NaN.
    """
    # Standard format checks
    assert clean_height("6-7") == 79.0
    assert clean_height("6-2") == 74.0
    # Null and error-prone inputs return NaN
    assert np.isnan(clean_height(None))
    assert np.isnan(clean_height("invalid"))
    assert np.isnan(clean_height(6.7))

def test_clean_year():
    """
    Test standardizing college class years into numerical season codes.
    Maps string representations ('Fr', 'So', 'Jr', 'Sr') to academic sequence levels (1-4).
    Verifies float values are coerced, and invalid states return NaN.
    """
    # Standard class mapping
    assert clean_year("Fr") == 1
    assert clean_year("So") == 2
    assert clean_year("Jr") == 3
    assert clean_year("Sr") == 4
    # String-float conversion check (whitespace trimmed)
    assert clean_year(" 2.0 ") == 2
    # Invalid inputs return NaN
    assert np.isnan(clean_year("invalid"))
    assert np.isnan(clean_year(None))
    assert np.isnan(clean_year(0.0))

def test_calculate_age():
    """
    Test computation of collegiate athlete age from DOB (YYYY-MM-DD) and season year.
    Verifies typical ages are correct, and checks handling of empty/malformed inputs.
    """
    # Standard calculation: 2020 - 1997 = 23 years old
    assert calculate_age(2020, "1997-10-15") == 23.0
    # Invalid combinations return NaN
    assert np.isnan(calculate_age(2020, None))
    assert np.isnan(calculate_age(None, "1997-10-15"))
    assert np.isnan(calculate_age(2020, "invalid-date"))

