import pandas as pd
from nba_prep.features import calculate_cumulative_features

def test_calculate_cumulative_features():
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
    res = calculate_cumulative_features(df)
    assert res.loc[0, 'career_season_num'] == 1
    assert res.loc[1, 'career_season_num'] == 2
    assert res.loc[1, 'cum_GP'] == 30
    assert res.loc[1, 'cum_pts'] == 350
    assert res.loc[1, 'cum_mean_bpm'] == 3.25
    assert res.loc[1, 'max_pts_to_date'] == 250
    assert res.loc[1, 'max_ast_to_date'] == 20
    assert res.loc[1, 'cum_mean_usg'] == 22.5
    assert res.loc[1, 'max_min_per_to_date'] == 60.0
    assert res.loc[1, 'pts_progression'] == 150
