import pytest
import numpy as np
from nba_prep.evaluation import calculate_model_metrics, estimate_draft_roi

def test_calculate_model_metrics():
    y_true = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0] # Base rate: 20%
    y_pred = [0.9, 0.1, 0.8, 0.2, 0.15, 0.05, 0.1, 0.0, 0.05, 0.1]
    
    metrics = calculate_model_metrics(y_true, y_pred)
    
    assert "auprc" in metrics
    assert "auroc" in metrics
    assert metrics["base_rate"] == 0.2
    assert metrics["auroc"] > 0.5
    assert metrics["optimal_threshold"] > 0.0

def test_estimate_draft_roi():
    y_true = [1, 0, 1, 0, 1, 0, 0, 0, 0, 0] # 3 successes, 7 busts
    y_pred = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    
    # Threshold at 0.5: drafted = [0.9, 0.8, 0.7, 0.6, 0.5] (first 5 players)
    # y_true for first 5 = [1, 0, 1, 0, 1] -> 3 successes, 2 busts
    roi = estimate_draft_roi(y_true, y_pred, threshold=0.5, rookie_contract_cost=5000000)
    
    assert roi["total_drafted"] == 5
    assert roi["draft_successes"] == 3
    assert roi["draft_busts"] == 2
    assert roi["scouting_success_rate_pct"] == 60.0 # 3 successes out of 5 drafted
    assert roi["base_success_rate_pct"] == 30.0 # 3 successes out of 10 prospects
    assert roi["relative_improvement_factor"] == 2.0 # 60% vs 30%
    assert roi["wasted_salary_cap_dollars"] == 10000000 # 2 busts * $5,000,000
    assert roi["scouting_travel_saved_pct"] == 50.0 # 5 skipped out of 10 prospects

    # Threshold at 1.5 (none drafted)
    empty_roi = estimate_draft_roi(y_true, y_pred, threshold=1.5)
    assert "message" in empty_roi
