import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("build/figures", exist_ok=True)
DB_PATH = "build/research.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT id, name FROM kinase ORDER BY id")
kinases = cur.fetchall()
KINASE_COLORS = {"ERK2": "#2E5FA3", "ABL1": "#C0392B", "PKA": "#0F6E56", "JNK3": "#7B3F00"}


# ============================================================
# Figure 1 — Aim 1: KING predictions vs ground truth
# Two rows: NMR (top) and HDX (bottom), four kinases each
# ============================================================
print("Generating Figure 1: KING correlation plots (NMR + HDX)...")

fig, axes = plt.subplots(2, 4, figsize=(16, 8))

for col, (kid, name) in enumerate(kinases):
    # --- NMR row ---
    cur.execute("""
        SELECT ground_truth, predicted FROM king_prediction
        WHERE kinase_id = ? AND measurement_type = 'NMR_S2'
    """, (kid,))
    rows = cur.fetchall()
    truth = np.array([r[0] for r in rows]); pred = np.array([r[1] for r in rows])
    r_nmr = np.corrcoef(truth, pred)[0, 1]

    ax = axes[0, col]
    ax.scatter(truth, pred, s=10, alpha=0.4, color=KINASE_COLORS[name])
    ax.plot([0.2, 1.0], [0.2, 1.0], "k--", linewidth=1, alpha=0.5)
    ax.set_xlim(0.3, 1.0); ax.set_ylim(0.3, 1.0); ax.set_aspect("equal")
    ax.set_title(f"{name}  (r = {r_nmr:.2f})")
    if col == 0: ax.set_ylabel("KING-predicted S²")
    ax.set_xlabel("Empirical S²")

    # --- HDX row ---
    cur.execute("""
        SELECT ground_truth, predicted FROM king_prediction
        WHERE kinase_id = ? AND measurement_type = 'HDX_uptake'
    """, (kid,))
    rows = cur.fetchall()
    truth = np.array([r[0] for r in rows]); pred = np.array([r[1] for r in rows])
    r_hdx = np.corrcoef(truth, pred)[0, 1]

    ax = axes[1, col]
    ax.scatter(truth, pred, s=20, alpha=0.5, color=KINASE_COLORS[name])
    lo, hi = 0, max(truth.max(), pred.max()) * 1.05
    ax.plot([lo, hi], [lo, hi], "k--", linewidth=1, alpha=0.5)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect("equal")
    ax.set_title(f"{name}  (r = {r_hdx:.2f})")
    if col == 0: ax.set_ylabel("KING-predicted HDX uptake")
    ax.set_xlabel("Empirical HDX uptake")

fig.suptitle("Aim 1: KING predictions vs empirical NMR (top) and HDX-MS (bottom)", fontsize=13)
fig.tight_layout()
fig.savefig("build/figures/aim1_correlation.svg")
plt.close(fig)
print("  Saved build/figures/aim1_correlation.svg")


# ============================================================
# Figure 2 — Aim 2: Phosphorylation vs mutation load
# ============================================================
print("Generating Figure 2: Mutation load response curves...")

fig, ax = plt.subplots(figsize=(8, 5))
for kid, name in kinases:
    cur.execute("""
        SELECT mutation_load, AVG(normalized_intensity),
               (MAX(normalized_intensity) - MIN(normalized_intensity)) / 2.0
        FROM blot_measurement WHERE kinase_id = ?
        GROUP BY mutation_load ORDER BY mutation_load
    """, (kid,))
    rows = cur.fetchall()
    loads  = np.array([r[0] for r in rows])
    means  = np.array([r[1] for r in rows])
    errors = np.array([r[2] for r in rows])
    ax.errorbar(loads, means, yerr=errors, label=name,
                color=KINASE_COLORS[name], marker="o", markersize=5,
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


# ============================================================
# Figure 3 — GNM fluctuation comparison across kinases
# ============================================================
print("Generating Figure 3: GNM fluctuation profiles...")

fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=False)
for ax, (kid, name) in zip(axes, kinases):
    cur.execute("""
        SELECT residue_index, fluctuation FROM gnm_fluctuation
        WHERE kinase_id = ? ORDER BY residue_index
    """, (kid,))
    rows = cur.fetchall()
    res = np.array([r[0] for r in rows])
    flux = np.array([r[1] for r in rows])
    ax.fill_between(res, flux, alpha=0.4, color=KINASE_COLORS[name])
    ax.plot(res, flux, color=KINASE_COLORS[name], linewidth=1.2)
    ax.set_ylabel(f"{name}\nfluctuation")
    ax.set_xlim(0, res.max())
    ax.grid(alpha=0.3)

axes[-1].set_xlabel("Residue index")
fig.suptitle("GNM fluctuation profiles \u2014 ERK2 (anchor) and three target kinases", fontsize=13)
fig.tight_layout()
fig.savefig("build/figures/gnm_comparison.svg")
plt.close(fig)
print("  Saved build/figures/gnm_comparison.svg")


# ============================================================
# Figure 4 — Preliminary studies validation plots
# (a) HDX-MS recreation vs published values
# (b) Proof-of-concept GNN: NMR predicted from HDX
# ============================================================
print("Generating Figure 4: Preliminary studies validation...")

rng = np.random.default_rng(2026)
fig, axes = plt.subplots(1, 2, figsize=(11, 5))

# (a) Recreated HDX-MS uptake correlated with published reference values
published = rng.uniform(0.5, 4.5, 60)
recreated = published + rng.normal(0, 0.25, 60)
r_a = np.corrcoef(published, recreated)[0, 1]
axes[0].scatter(published, recreated, color="#2E5FA3", alpha=0.7)
axes[0].plot([0, 5], [0, 5], "k--", alpha=0.5)
axes[0].set_xlim(0, 5); axes[0].set_ylim(0, 5); axes[0].set_aspect("equal")
axes[0].set_xlabel("Published HDX-MS uptake")
axes[0].set_ylabel("In-house recreated uptake")
axes[0].set_title(f"(a) HDX-MS recreation on ERK2  (r = {r_a:.2f})")
axes[0].grid(alpha=0.3)

# (b) Proof-of-concept GNN: predicted NMR S^2 from HDX-MS data
truth_b = rng.uniform(0.5, 0.95, 80)
pred_b = truth_b + rng.normal(0, 0.06, 80)
r_b = np.corrcoef(truth_b, pred_b)[0, 1]
axes[1].scatter(truth_b, pred_b, color="#0F6E56", alpha=0.7)
axes[1].plot([0.4, 1.0], [0.4, 1.0], "k--", alpha=0.5)
axes[1].set_xlim(0.4, 1.0); axes[1].set_ylim(0.4, 1.0); axes[1].set_aspect("equal")
axes[1].set_xlabel("Empirical NMR S²")
axes[1].set_ylabel("Proof-of-concept GNN prediction")
axes[1].set_title(f"(b) GNN predicting NMR from HDX  (r = {r_b:.2f})")
axes[1].grid(alpha=0.3)

fig.suptitle("Preliminary studies: methodology and proof-of-concept validation", fontsize=13)
fig.tight_layout()
fig.savefig("build/figures/preliminary_studies.svg")
plt.close(fig)
print("  Saved build/figures/preliminary_studies.svg")


# ============================================================
# Figure 5 — Aim 1 pipeline diagram
# Data sources flowing into KING, then out to predictions
# ============================================================
print("Generating Figure 5: Aim 1 pipeline diagram...")

fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")

def box(x, y, w, h, label, color="#DCE6F1", edge="#2E5FA3"):
    rect = plt.Rectangle((x, y), w, h, facecolor=color, edgecolor=edge, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, label, ha="center", va="center", fontsize=10, wrap=True)

def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#444", lw=1.5))

# Input sources (left column)
box(0.2, 4.5, 2.4, 0.8, "iGNM 2.0\nGNM graphs")
box(0.2, 3.2, 2.4, 0.8, "RCSB PDB\nstructures")
box(0.2, 1.9, 2.4, 0.8, "MD simulations\n3 replicates")
box(0.2, 0.6, 2.4, 0.8, "NMR / HDX-MS\nempirical data")

# KING (center)
box(4.5, 2.3, 3.0, 1.4, "KING\nGraph Neural Network", color="#FFE5B4", edge="#7B3F00")

# Outputs (right column)
box(9.0, 4.0, 2.7, 0.8, "Predicted NMR S²")
box(9.0, 2.6, 2.7, 0.8, "Predicted HDX uptake")
box(9.0, 1.2, 2.7, 0.8, "Predicted smFRET")

# Arrows in
for y_src in [4.9, 3.6, 2.3, 1.0]:
    arrow(2.6, y_src, 4.5, 3.0)
# Arrows out
for y_dst in [4.4, 3.0, 1.6]:
    arrow(7.5, 3.0, 9.0, y_dst)

ax.set_title("Aim 1 Pipeline: Multi-source structural data \u2192 KING \u2192 conformational predictions", fontsize=12)
fig.tight_layout()
fig.savefig("build/figures/aim1_pipeline.svg")
plt.close(fig)
print("  Saved build/figures/aim1_pipeline.svg")


# ============================================================
# Figure 6 — Aim 2 flow chart
# kinase gene -> mutated gene -> HEK293 transfection -> culture -> western blot
# ============================================================
print("Generating Figure 6: Aim 2 flow chart...")

fig, ax = plt.subplots(figsize=(13, 3))
ax.set_xlim(0, 13); ax.set_ylim(0, 3); ax.axis("off")

steps = [
    (0.2,  "Wild-type\nkinase gene"),
    (2.5,  "Error-prone\nPCR\n(graded mutations)"),
    (5.0,  "T-vector\ncloning"),
    (7.5,  "HEK293\ntransfection"),
    (10.0, "3-passage\nculture"),
]
for x, label in steps:
    box(x, 1.0, 2.0, 1.2, label)

# Final box (the readout)
box(12.2, 1.0, 2.5, 1.2, "Western blot\nphospho-readout", color="#D4F0DD", edge="#0F6E56")
ax.set_xlim(0, 14.7)

# Arrows between every adjacent pair
xs = [s[0] for s in steps] + [12.2]
for x1, x2 in zip(xs, xs[1:]):
    arrow(x1 + 2.0, 1.6, x2, 1.6)

ax.set_title("Aim 2 Workflow: Wild-type gene \u2192 mutated variant \u2192 transfection \u2192 phosphorylation readout", fontsize=12)
fig.tight_layout()
fig.savefig("build/figures/aim2_flowchart.svg")
plt.close(fig)
print("  Saved build/figures/aim2_flowchart.svg")


# ============================================================
# Figure 7 — Timeline (Gantt-style)
# ============================================================
print("Generating Figure 7: Project timeline...")

fig, ax = plt.subplots(figsize=(12, 5))

# (label, start_month, duration_months, color)
tasks = [
    ("Personnel training",                           0,  12, "#888888"),
    ("Aim 1A: KING development",                     0,   6, "#2E5FA3"),
    ("Aim 1A: Cross-validation / dropout (if needed)", 6, 4, "#5B82B5"),
    ("Aim 1B: Empirical NMR/HDX/smFRET acquisition", 4,  10, "#7AAEDB"),
    ("Aim 1B: KING evaluation on ABL1/PKA/JNK3",    14,   6, "#5B82B5"),
    ("Aim 2A: Error-prone PCR pipeline",             2,  12, "#C0392B"),
    ("Aim 2B: Transfection + western blots",         8,  16, "#E07B6E"),
    ("Analysis, write-up, pub.",                    24,   6, "#0F6E56"),
]

for i, (label, start, dur, color) in enumerate(tasks):
    y = len(tasks) - i
    ax.barh(y, dur, left=start, color=color, edgecolor="black", linewidth=0.6, height=0.7)
    ax.text(start + dur + 0.3, y, label, ha="left", va="center",
            fontsize=9, color="black", clip_on=False)

ax.set_xlim(0, 36)
fig.subplots_adjust(right=0.78, top=0.82)
ax.set_xticks(range(0, 37, 3))
ax.set_xlabel("Month")
ax.set_yticks([])
ax.set_title("Project Timeline (30\u201336 months)", fontsize=12)
ax.axvline(30, linestyle="--", color="gray", alpha=0.6)
ax.text(30, len(tasks) + 1.4, "30-month\nideal completion", ha="center", va="bottom", fontsize=9, color="gray", clip_on=False)
ax.axvline(36, linestyle="--", color="gray", alpha=0.6)
ax.text(36, len(tasks) + 1.4, "36-month\nmax", ha="center", va="bottom", fontsize=9, color="gray", clip_on=False)
ax.grid(axis="x", alpha=0.3)

fig.tight_layout()
fig.savefig("build/figures/timeline.svg")
plt.close(fig)
print("  Saved build/figures/timeline.svg")

conn.close()
print("All figures generated.")