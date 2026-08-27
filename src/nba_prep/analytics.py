"""
nba_prep - Prospect Analytics & Scouting
This module provides functions to categorize prospects into qualitative draft tiers
and generate textual scouting reports summarizing their collegiate box score profiles.
"""

import numpy as np
import pandas as pd

def categorize_prospect(probability):
    """
    Categorizes the predicted probability of NBA career longevity (>= 3 seasons)
    into actionable tiers for front-office decision makers.
    
    Parameters:
        probability (float/str): Predicted probability score between 0.0 and 1.0.
        
    Returns:
        str: Actionable scouting tier description.
    """
    try:
        p = float(probability)
        if not (0.0 <= p <= 1.0):
            return "Invalid Probability"
        
        # Classify into scout-friendly ranges
        if p >= 0.75:
            return "Tier 1: Franchise Core (Elite)"
        elif p >= 0.45:
            return "Tier 2: Rotation Contributor (Moderate)"
        elif p >= 0.15:
            return "Tier 3: G-League / Development Project (Low-Moderate)"
        else:
            return "Tier 4: High Risk / Undrafted Profile (Very Low)"
    except Exception:
        return "Unknown Tier"

def generate_scouting_report(player_name, bpm, true_shooting, defensive_impact, rec_rank=None):
    """
    Generates a concise textual scouting report card summarizing a prospect's collegiate profile.
    
    Parameters:
        player_name (str): Name of the prospect player.
        bpm (float): Box Plus-Minus (bpm) overall impact score.
        true_shooting (float): True Shooting percentage (ts%).
        defensive_impact (float): Calculated Defensive Impact score.
        rec_rank (float, optional): High school recruiting rank (1-150+).
        
    Returns:
        str: Formatted scouting report summary card.
    """
    try:
        report = []
        report.append(f"=== Scouting Profile Summary: {player_name} ===")
        
        # 1. On-court overall impact (BPM)
        bpm_val = float(bpm) if bpm is not None else 0.0
        if bpm_val >= 8.0:
            report.append("- On-Court Impact: Elite collegiate contributor. Dominates game-flow.")
        elif bpm_val >= 3.0:
            report.append("- On-Court Impact: Solid positive contributor. Standard rotation-level output.")
        else:
            report.append("- On-Court Impact: Below-average impact. May struggle with speed/intensity at professional level.")
            
        # 2. Scoring efficiency (True Shooting)
        ts_val = float(true_shooting) if true_shooting is not None else 0.0
        if ts_val >= 0.60:
            report.append("- Scoring Efficiency: Exceptionally efficient. Outstanding shooting selections.")
        elif ts_val >= 0.50:
            report.append("- Scoring Efficiency: Average efficiency. Capable secondary scoring option.")
        else:
            report.append("- Scoring Efficiency: Highly inefficient scorer. Needs structural offensive adjustment.")
            
        # 3. Defensive presence (Defensive Impact Score)
        def_val = float(defensive_impact) if defensive_impact is not None else 0.0
        if def_val >= 10.0:
            report.append("- Defensive Presence: Heavy defensive impact. Strong rebounder, rim protector, or disruptor.")
        elif def_val >= 4.0:
            report.append("- Defensive Presence: Moderate defensive activity. Solid team defender.")
        else:
            report.append("- Defensive Presence: Minimal defensive statistical footprint. Potential defensive liability.")
            
        # 4. Recruiting Pedigree
        if rec_rank is not None:
            rank_val = float(rec_rank)
            if rank_val <= 25.0:
                report.append("- Pedigree: Five-star high school recruit with elite pedigree.")
            elif rank_val <= 100.0:
                report.append("- Pedigree: Four-star prospect with solid high school pedigree.")
            else:
                report.append("- Pedigree: Mid-major or unranked prospect. Career path relies heavily on development.")
        
        return "\n".join(report)
    except Exception as e:
        return f"Error generating scouting report: {str(e)}"

