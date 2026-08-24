import pytest
from nba_prep.analytics import categorize_prospect, generate_scouting_report

def test_categorize_prospect():
    assert categorize_prospect(0.8) == "Tier 1: Franchise Core (Elite)"
    assert categorize_prospect(0.5) == "Tier 2: Rotation Contributor (Moderate)"
    assert categorize_prospect(0.2) == "Tier 3: G-League / Development Project (Low-Moderate)"
    assert categorize_prospect(0.05) == "Tier 4: High Risk / Undrafted Profile (Very Low)"
    assert categorize_prospect(1.5) == "Invalid Probability"
    assert categorize_prospect("not-a-probability") == "Unknown Tier"

def test_generate_scouting_report():
    # Elite player report test
    report_elite = generate_scouting_report("LeBron James", 10.5, 0.62, 12.0, rec_rank=5.0)
    assert "LeBron James" in report_elite
    assert "Elite collegiate contributor" in report_elite
    assert "Exceptionally efficient" in report_elite
    assert "Heavy defensive impact" in report_elite
    assert "Five-star high school recruit" in report_elite

    # Below average player report test
    report_fringe = generate_scouting_report("Bench Player", 1.0, 0.45, 2.0, rec_rank=150.0)
    assert "Bench Player" in report_fringe
    assert "Below-average impact" in report_fringe
    assert "Highly inefficient scorer" in report_fringe
    assert "Minimal defensive statistical footprint" in report_fringe
    assert "Mid-major or unranked prospect" in report_fringe
