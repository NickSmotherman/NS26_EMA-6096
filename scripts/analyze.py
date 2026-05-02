import sqlite3
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, ttest_ind
from scipy.optimize import curve_fit
import os

os.makedirs("build", exist_ok=True)
DB_PATH = "build/research.db"
conn = sqlite3.connect(DB_PATH)


# ============================================================
# Aim 1 Analysis — KING accuracy per kinase
# ============================================================
print("=" * 60)
print("AIM 1: KING prediction accuracy per kinase")
print("=" * 60)

raw_predictions = pd.read_sql_query("""
    SELECT k.name AS kinase, p.measurement_type, p.ground_truth, p.predicted
    FROM king_prediction p
    JOIN kinase k ON k.id = p.kinase_id
""", conn)

# Compute per-kinase statistics
aim1_results = []
for kinase, group in raw_predictions.groupby("kinase"):
    truth = group["ground_truth"].values
    pred = group["predicted"].values

    pearson_r, pearson_p = pearsonr(truth, pred)
    spearman_r, spearman_p = spearmanr(truth, pred)
    mae = np.mean(np.abs(truth - pred))

    aim1_results.append({
        "kinase":      kinase,
        "n_points":    len(truth),
        "pearson_r":   round(pearson_r, 4),
        "pearson_p":   pearson_p,
        "spearman_r":  round(spearman_r, 4),
        "spearman_p":  spearman_p,
        "mean_abs_err": round(mae, 4),
    })

aim1_df = pd.DataFrame(aim1_results)
print("\nAim 1 results dataframe:")
print(aim1_df.to_string(index=False))
aim1_df.to_csv("build/aim1_analysis.csv", index=False)
print("\nSaved to build/aim1_analysis.csv")


# ============================================================
# Aim 2 Analysis — Mutation threshold per kinase + cross-kinase t-tests
# ============================================================
print("\n" + "=" * 60)
print("AIM 2: Mutation tolerance threshold per kinase")
print("=" * 60)

raw_blots = pd.read_sql_query("""
    SELECT k.name AS kinase, b.mutation_load, b.normalized_intensity
    FROM blot_measurement b
    JOIN kinase k ON k.id = b.kinase_id
""", conn)

# Exponential decay model for fitting
def decay_model(x, threshold, steepness):
    return np.exp(-((x / threshold) ** steepness))

# Fit each kinase's curve and find its threshold
aim2_results = {}
for kinase, group in raw_blots.groupby("kinase"):
    means = group.groupby("mutation_load")["normalized_intensity"].mean().reset_index()
    x = means["mutation_load"].values
    y = means["normalized_intensity"].values

    popt, _ = curve_fit(decay_model, x, y, p0=[12, 2.5], maxfev=5000)
    threshold, steepness = popt

    # R-squared
    y_pred = decay_model(x, *popt)
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # The point of maximum derivative (steepest functional loss)
    x_fine = np.linspace(0, 25, 500)
    y_fine = decay_model(x_fine, *popt)
    derivative = np.gradient(y_fine, x_fine)
    max_deriv_load = x_fine[np.argmin(derivative)]  # most negative = steepest drop

    aim2_results[kinase] = {
        "threshold_param":      round(threshold, 3),
        "steepness_param":      round(steepness, 3),
        "max_derivative_load":  round(max_deriv_load, 2),
        "r_squared":            round(r_squared, 4),
        "raw_individual_loads": group[group["mutation_load"] == round(max_deriv_load)]["normalized_intensity"].values
    }

# Cross-kinase t-tests: are these thresholds statistically similar?
# Compare each kinase's intensity values at its own threshold load against ERK2's
print("\nCross-kinase t-tests (at each kinase's own max-derivative load, vs ERK2):")
erk2_values = aim2_results["ERK2"]["raw_individual_loads"]

ttest_rows = []
for kinase, res in aim2_results.items():
    if kinase == "ERK2":
        t_stat, p_val = (np.nan, np.nan)
    else:
        t_stat, p_val = ttest_ind(erk2_values, res["raw_individual_loads"])
    ttest_rows.append({
        "kinase":              kinase,
        "max_derivative_load": res["max_derivative_load"],
        "r_squared":           res["r_squared"],
        "t_stat_vs_ERK2":      round(t_stat, 3) if not np.isnan(t_stat) else None,
        "p_value_vs_ERK2":     p_val if not np.isnan(p_val) else None,
        "similar_to_ERK2":     (p_val > 0.05) if not np.isnan(p_val) else None,
    })

aim2_df = pd.DataFrame(ttest_rows)
print("\nAim 2 results dataframe:")
print(aim2_df.to_string(index=False))
aim2_df.to_csv("build/aim2_analysis.csv", index=False)
print("\nSaved to build/aim2_analysis.csv")


# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
print(f"  build/aim1_analysis.csv  - {len(aim1_df)} rows")
print(f"  build/aim2_analysis.csv  - {len(aim2_df)} rows")

conn.close()