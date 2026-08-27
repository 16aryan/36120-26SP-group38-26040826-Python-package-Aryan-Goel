import pandas as pd
from nba_prep.features import calculate_cumulative_features

# ==============================================================================
# TEST SUITE: CUMULATIVE CAREER FEATURES
# ==============================================================================
# This suite verifies that historical player-level stats are aggregated correctly
# over successive collegiate seasons (using 'pid' and 'year' grouping).

def test_calculate_cumulative_features():
    """
    Validate career cumulative metrics, peak indicators, and seasonal progression deltas.
    Uses a mock DataFrame representing a multi-season history for two separate players (pid 1 and 2).
    """
    # Arrange: Setup mock player data.
    # Player 1 has 2 seasons (2020 & 2021). Player 2 has 1 season (2020).
    df = pd.DataFrame({
        'pid': [1, 1, 2],
        'year': [2020, 2021, 2020],
        'GP': [10, 20, 5],
        'pts': [100, 250, 30],
        'ast': [10, 20, 5],
        'stl': [5, 10, 2],
        'blk': [2, 4, 1],
        'treb': [30, 60, 10],
        'stops': [15, 25, 6],
        'bpm': [2.5, 4.0, 1.0],
        'porpag': [1.5, 2.5, 0.5],
        'dporpag': [1.0, 2.0, 0.5],
        'usg': [20.0, 25.0, 15.0],
        'Min_per': [40.0, 60.0, 30.0]
    })
    
    # Act: Process cumulative features
    res = calculate_cumulative_features(df)
    
    # Assert: Verify season counters, cumulative sums, peak values, and delta features.
    assert res.loc[0, 'career_season_num'] == 1  # Player 1 first season
    assert res.loc[1, 'career_season_num'] == 2  # Player 1 second season
    assert res.loc[1, 'cum_GP'] == 30            # Cumulative GP: 10 + 20
    assert res.loc[1, 'cum_pts'] == 350          # Cumulative points: 100 + 250
    assert res.loc[1, 'cum_mean_bpm'] == 3.25    # Mean Box Plus-Minus: (2.5 + 4.0)/2
    assert res.loc[1, 'max_pts_to_date'] == 250  # Max points achieved up to this season
    assert res.loc[1, 'max_ast_to_date'] == 20   # Max assists achieved up to this season
    assert res.loc[1, 'cum_mean_usg'] == 22.5    # Mean usage rate: (20.0 + 25.0)/2
    assert res.loc[1, 'max_min_per_to_date'] == 60.0 # Max playing minutes % up to this season
    assert res.loc[1, 'pts_progression'] == 150  # Progression delta: 250 - 100

