"""
nba_prep - Evaluation & Business Decision ROI
This module implements functions to compute statistical validation metrics (AUPRC, AUROC)
and translate predictive model probabilities into actionable financial ROI models.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score, precision_recall_curve

def calculate_model_metrics(y_true, y_pred):
    """
    Computes key classification and ranking metrics (AUPRC, AUROC, and base rate)
    for model evaluation, and locates the decision threshold that maximizes the F1-score.
    
    Parameters:
        y_true (array-like): Ground truth binary labels (1 = longevity, 0 = bust).
        y_pred (array-like): Continuous predicted success probabilities.
        
    Returns:
        dict: Collection of evaluation metrics containing:
              - 'auprc': Area Under the Precision-Recall Curve (target metric)
              - 'auroc': Area Under the Receiver Operating Characteristic
              - 'base_rate': Proportion of positive labels in the true dataset
              - 'optimal_threshold': Probability threshold that maximizes F1-score
              - 'max_f1': The maximum F1-score achieved at the optimal threshold
    """
    try:
        y_true_arr = np.array(y_true, dtype=float)
        y_pred_arr = np.array(y_pred, dtype=float)
        
        auprc = float(average_precision_score(y_true_arr, y_pred_arr))
        auroc = float(roc_auc_score(y_true_arr, y_pred_arr))
        base_rate = float(np.mean(y_true_arr))
        
        # Calculate optimal threshold balancing precision and recall (F1 score max)
        precisions, recalls, thresholds = precision_recall_curve(y_true_arr, y_pred_arr)
        f1_scores = np.zeros_like(thresholds)
        for i in range(len(thresholds)):
            p = precisions[i]
            r = recalls[i]
            if p + r > 0:
                f1_scores[i] = 2.0 * p * r / (p + r)
        
        opt_idx = np.argmax(f1_scores) if len(f1_scores) > 0 else 0
        optimal_threshold = float(thresholds[opt_idx]) if len(thresholds) > 0 else 0.5
        max_f1 = float(f1_scores[opt_idx]) if len(f1_scores) > 0 else 0.0
        
        return {
            "auprc": auprc,
            "auroc": auroc,
            "base_rate": base_rate,
            "optimal_threshold": optimal_threshold,
            "max_f1": max_f1
        }
    except Exception as e:
        return {"error": str(e)}

def estimate_draft_roi(y_true, y_pred, threshold, rookie_contract_cost=5000000):
    """
    Estimates the financial ROI and scouting cost-savings for an NBA front office 
    using the model's predictions to filter draft prospects.
    
    Parameters:
      - y_true (array-like): Ground truth career longevity label (1 = success, 0 = bust).
      - y_pred (array-like): Model predicted success probability.
      - threshold (float): Decision probability threshold above which a player is drafted.
      - rookie_contract_cost (int/float): Cost of a guaranteed rookie contract (default: $5,000,000).
      
    Returns:
      - dict: Collection of business ROI metrics containing:
              - 'total_prospects': Total prospects screened
              - 'total_drafted': Number of players predicted above the threshold
              - 'draft_successes': Successful players selected (True Positives)
              - 'draft_busts': Wasted contract selections (False Positives)
              - 'scouting_success_rate_pct': Success rate among players selected
              - 'base_success_rate_pct': Base success rate in the overall pool
              - 'relative_improvement_factor': Yield improvement factor (e.g. 2.5x)
              - 'wasted_salary_cap_dollars': Wasted contract cap space on busts
              - 'scouting_travel_saved_pct': Percentage of player pool filtered out
    """
    try:
        y_true_arr = np.array(y_true, dtype=bool)
        y_pred_arr = np.array(y_pred, dtype=float)
        
        # Players drafted are those equal to or greater than the decision threshold
        drafted = y_pred_arr >= threshold
        
        total_prospects = len(y_true_arr)
        total_drafted = int(np.sum(drafted))
        
        if total_drafted == 0:
            return {"message": "No prospects drafted at this threshold."}
            
        successes = int(np.sum(y_true_arr & drafted))
        busts = int(np.sum((~y_true_arr) & drafted))
        
        success_rate = float(successes / total_drafted)
        base_success_rate = float(np.mean(y_true_arr))
        
        # Financial impact: money spent on busts (False Positives)
        wasted_salary_cap = busts * rookie_contract_cost
        
        # Scouting efficiency: percentage of player pool filtered out (skipped scouting/travel)
        skipped_scouting_pct = float((total_prospects - total_drafted) / total_prospects)
        
        return {
            "total_prospects": total_prospects,
            "total_drafted": total_drafted,
            "draft_successes": successes,
            "draft_busts": busts,
            "scouting_success_rate_pct": success_rate * 100,
            "base_success_rate_pct": base_success_rate * 100,
            "relative_improvement_factor": float(success_rate / base_success_rate) if base_success_rate > 0 else 0,
            "wasted_salary_cap_dollars": wasted_salary_cap,
            "scouting_travel_saved_pct": skipped_scouting_pct * 100
        }
    except Exception as e:
        return {"error": str(e)}

