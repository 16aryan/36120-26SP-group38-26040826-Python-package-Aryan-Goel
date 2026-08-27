from nba_prep import (
    clean_height, 
    categorize_prospect, 
    generate_scouting_report, 
    calculate_model_metrics, 
    estimate_draft_roi
)

print("--- Verifying Python Package: nba_prep (v0.3.1) ---")

# 1. Clean height data
height_inches = clean_height("6-7")
print(f"Height '6-7' cleaned to: {height_inches} inches (Expected: 79.0)")

# 2. Categorize a prospect's probability score
tier = categorize_prospect(0.82)
print(f"Prospect probability 0.82 classified as: '{tier}'")

# 3. Generate a scouting report card
report = generate_scouting_report(
    "Aryan Goel", 
    bpm=9.2, 
    true_shooting=0.61, 
    defensive_impact=11.0, 
    rec_rank=15.0
)
print("\nGenerated Scouting Report Card:")
print(report)

# 4. Run Model Evaluation Metrics
print("\n--- Simulated Model Evaluation (Experiments 1, 2, 3) ---")
y_true = [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]  # Ground truth: 3 successes, 7 busts
y_pred = [0.92, 0.78, 0.85, 0.40, 0.12, 0.65, 0.31, 0.05, 0.18, 0.09]  # Model probabilities

metrics = calculate_model_metrics(y_true, y_pred)
print(f"Model AUPRC Score: {metrics['auprc']:.4f}")
print(f"Model AUROC Score: {metrics['auroc']:.4f}")
print(f"Optimal Decision Threshold (Max F1): {metrics['optimal_threshold']:.4f}")

# 5. Estimate Draft ROI
print("\n--- Scouting & Financial ROI Estimation ---")
roi = estimate_draft_roi(y_true, y_pred, threshold=0.50, rookie_contract_cost=5000000)

print(f"Total Prospects Screened: {roi['total_prospects']}")
print(f"Prospects Drafted above threshold: {roi['total_drafted']}")
print(f"Successful Picks: {roi['draft_successes']} | Wasted Picks (Busts): {roi['draft_busts']}")
print(f"Draft Success Rate: {roi['scouting_success_rate_pct']:.1f}%")
print(f"Relative Scouting Yield Improvement: {roi['relative_improvement_factor']:.2f}x")
print(f"Wasted Salary Cap Dollars: ${roi['wasted_salary_cap_dollars']:,}")
print(f"Scouting Travel & Video Analysis Hours Saved: {roi['scouting_travel_saved_pct']:.1f}%")
