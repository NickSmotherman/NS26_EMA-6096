import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("build/figures", exist_ok=True)
DB_PATH = "build/research.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()


# =====================================================
# Figure 1 — Aim 1: KING predictions vs ground truth
# One scatter plot per kinase, side by side
# =====================================================
print("Generating Figure 1: KING correlation plots...")

cur.execute("SELECT id, name FROM kinase ORDER BY id")
kinases = cur.fetchall()

fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharey=True)

for ax, (kid, name) in zip(axes, kinases):
    cur.execute("""
        SELECT ground_truth, predicted
        FROM king_prediction
        WHERE kinase_id = ? AND measurement_type = 'NMR_S2'
    """, (kid,))
    rows = cur.fetchall()
    truth = np.array([r[0] for r in rows])
    pred  = np.array([r[1] for r in rows])

    # Pearson correlation
    r = np.corrcoef(truth, pred)[0, 1]

    ax.scatter(truth, pred, s=10, alpha=0.4, color="#2E5FA3")
    ax.plot([0.2, 1.0], [0.2, 1.0], "k--", linewidth=1, alpha=0.5)  # y=x line
    ax.set_xlim(0.3, 1.0)
    ax.set_ylim(0.3, 1.0)
    ax.set_xlabel("Empirical S²")
    ax.set_title(f"{name}  (r = {r:.2f})")
    ax.set_aspect("equal")

axes[0].set_ylabel("KING-predicted S²")
fig.suptitle("Aim 1: KING predictions vs empirical NMR order parameters", fontsize=13)
fig.tight_layout()
fig.savefig("build/figures/aim1_correlation.svg")
plt.close(fig)
print("  Saved build/figures/aim1_correlation.svg")


# =================================================
# Figure 2 — Aim 2: Phosphorylation vs mutation load
# One curve per kinase, all on the same axes
# =================================================
print("Generating Figure 2: Mutation load response curves...")

fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#2E5FA3", "#C0392B", "#0F6E56", "#7B3F00"]

for (kid, name), color in zip(kinases, colors):
    cur.execute("""
        SELECT mutation_load, AVG(normalized_intensity), 
               (MAX(normalized_intensity) - MIN(normalized_intensity)) / 2.0
        FROM blot_measurement
        WHERE kinase_id = ?
        GROUP BY mutation_load
        ORDER BY mutation_load
    """, (kid,))
    rows = cur.fetchall()
    loads  = np.array([r[0] for r in rows])
    means  = np.array([r[1] for r in rows])
    errors = np.array([r[2] for r in rows])

    ax.errorbar(loads, means, yerr=errors, label=name,
                color=color, marker="o", markersize=5,
                linewidth=1.5, capsize=3, alpha=0.85)

ax.axhline(0.1, linestyle="--", color="gray", alpha=0.6, linewidth=1)
ax.text(24, 0.115, "10% threshold", ha="right", va="bottom", fontsize=9, color="gray")

ax.set_xlabel("Mutation load (point mutations)")
ax.set_ylabel("Normalized phosphorylation intensity")
ax.set_title("Aim 2: Phosphorylation response to increasing mutation load")
ax.legend(title="Kinase", loc="upper right")
ax.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("build/figures/aim2_mutation_curve.svg")
plt.close(fig)
print("  Saved build/figures/aim2_mutation_curve.svg")


conn.close()
print("All figures generated.")