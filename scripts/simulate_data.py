


import os
import csv
import random
import math

random.seed(42)  # deterministic output

os.makedirs("data/simulated", exist_ok=True)

KINASES = ["ERK2", "ABL1", "PKA", "JNK3"]
PROTEIN_LENGTHS = {"ERK2": 360, "ABL1": 280, "PKA": 350, "JNK3": 400}


# ---------- NMR measurements ----------
# S^2 order parameter per residue, plus T1 and T2 relaxation times
# Real S^2 values typically range 0.6 - 0.95 for rigid regions, lower for loops

with open("data/simulated/nmr_measurements.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["kinase", "replicate", "residue_index", "order_parameter_s2", "t1_ms", "t2_ms"])
    for kinase in KINASES:
        for rep in range(1, 5):  # quadruplicate
            for residue in range(1, PROTEIN_LENGTHS[kinase] + 1):
                s2 = max(0.3, min(0.95, random.gauss(0.82, 0.08)))
                t1 = random.gauss(800, 60)
                t2 = random.gauss(60, 8)
                w.writerow([kinase, rep, residue, round(s2, 3), round(t1, 1), round(t2, 1)])


# ---------- HDX-MS measurements ----------
# Deuterium uptake per peptide across multiple timepoints
# We'll fake ~30 peptides per kinase across the protein

TIMEPOINTS = [10, 30, 60, 300, 1800]  # seconds
with open("data/simulated/hdx_measurements.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["kinase", "replicate", "peptide_id", "start_residue", "end_residue", "timepoint_s", "deuterium_uptake"])
    for kinase in KINASES:
        n_peptides = 30
        for rep in range(1, 5):
            for pep_id in range(1, n_peptides + 1):
                start = random.randint(1, PROTEIN_LENGTHS[kinase] - 10)
                end = start + random.randint(5, 9)
                # Each peptide has a baseline uptake rate
                base = random.uniform(0.5, 4.5)
                for t in TIMEPOINTS:
                    # Exponential uptake model
                    uptake = base * (1 - math.exp(-t / 600)) + random.gauss(0, 0.1)
                    w.writerow([kinase, rep, pep_id, start, end, t, round(max(0, uptake), 3)])


# ---------- KING predictions ----------
# For each empirical measurement, KING produces a slightly noisy prediction
# Pearson r ~0.85 expected (consistent with grant's stated >0.75 target)

with open("data/simulated/king_predictions.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["kinase", "measurement_type", "residue_or_peptide_id", "ground_truth", "predicted"])
    # NMR predictions
    for kinase in KINASES:
        for residue in range(1, PROTEIN_LENGTHS[kinase] + 1):
            truth = max(0.3, min(0.95, random.gauss(0.82, 0.08)))
            # KING prediction: truth + small noise
            pred = truth + random.gauss(0, 0.07)
            pred = max(0.2, min(1.0, pred))
            w.writerow([kinase, "NMR_S2", residue, round(truth, 3), round(pred, 3)])
    # HDX predictions (one value per peptide, averaged across timepoints)
    for kinase in KINASES:
        for pep_id in range(1, 31):
            truth = random.uniform(0.5, 4.5)
            pred = truth + random.gauss(0, 0.4)
            w.writerow([kinase, "HDX_uptake", pep_id, round(truth, 3), round(max(0, pred), 3)])


# ---------- Western blot measurements ----------
# Phosphorylation intensity vs mutation load - exponential decay
# Each kinase has its own threshold (similar but not identical)

KINASE_THRESHOLDS = {"ERK2": 12, "ABL1": 11, "PKA": 13, "JNK3": 12}
with open("data/simulated/blot_measurements.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["kinase", "mutation_load", "replicate", "pixel_intensity", "normalized_intensity"])
    for kinase in KINASES:
        threshold = KINASE_THRESHOLDS[kinase]
        for mut_load in range(0, 25):
            for rep in range(1, 5):
                # Exponential decay centered on the threshold
                decay = math.exp(-((mut_load / threshold) ** 2.5))
                raw_intensity = decay * 1000 + random.gauss(0, 25)
                normalized = decay + random.gauss(0, 0.025)
                w.writerow([kinase, mut_load, rep, round(max(0, raw_intensity), 1), round(max(0, normalized), 4)])

# ---------- GNM fluctuation profiles ----------
# Per-residue mean-squared fluctuations from a Gaussian Network Model
# Real GNM values are typically 0.1 - 5.0 with peaks at flexible loops

with open("data/simulated/gnm_fluctuations.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["kinase", "residue_index", "fluctuation"])
    for kinase in KINASES:
        length = PROTEIN_LENGTHS[kinase]
        # Build a realistic profile: low everywhere, peaks at a few loop regions
        loop_centers = [int(length * frac) for frac in [0.15, 0.45, 0.7, 0.9]]
        for residue in range(1, length + 1):
            base = 0.4 + random.gauss(0, 0.1)
            # Add Gaussian peaks at loop regions
            for center in loop_centers:
                base += 2.5 * math.exp(-((residue - center) ** 2) / (2 * 15 ** 2))
            base = max(0.1, base + random.gauss(0, 0.15))
            w.writerow([kinase, residue, round(base, 4)])

print("Simulated data written to data/simulated/")