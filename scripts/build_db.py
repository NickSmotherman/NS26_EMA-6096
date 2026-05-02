
import sqlite3
import csv
import os

os.makedirs("build", exist_ok=True)
DB_PATH = "build/research.db"

# Remove old database if it exists, so we start fresh every build
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()


# ---------- Create the schema ----------
print("Creating schema...")

cur.executescript("""
CREATE TABLE kinase (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,
    pdb_id       TEXT NOT NULL,
    aa_length    INTEGER
);

CREATE TABLE blind_assignment (
    id           INTEGER PRIMARY KEY,
    kinase_id    INTEGER NOT NULL,
    blind_code   TEXT NOT NULL,
    FOREIGN KEY (kinase_id) REFERENCES kinase(id)
);

CREATE TABLE nmr_measurement (
    id                  INTEGER PRIMARY KEY,
    kinase_id           INTEGER NOT NULL,
    replicate           INTEGER NOT NULL,
    residue_index       INTEGER NOT NULL,
    order_parameter_s2  REAL,
    t1_ms               REAL,
    t2_ms               REAL,
    FOREIGN KEY (kinase_id) REFERENCES kinase(id)
);

CREATE TABLE hdx_measurement (
    id                INTEGER PRIMARY KEY,
    kinase_id         INTEGER NOT NULL,
    replicate         INTEGER NOT NULL,
    peptide_id        INTEGER NOT NULL,
    start_residue     INTEGER,
    end_residue       INTEGER,
    timepoint_s       REAL,
    deuterium_uptake  REAL,
    FOREIGN KEY (kinase_id) REFERENCES kinase(id)
);

CREATE TABLE king_model (
    id                    INTEGER PRIMARY KEY,
    training_date         TEXT,
    validation_pearson_r  REAL,
    github_commit         TEXT
);

CREATE TABLE king_prediction (
    id                INTEGER PRIMARY KEY,
    model_id          INTEGER NOT NULL,
    kinase_id         INTEGER NOT NULL,
    measurement_type  TEXT NOT NULL,
    item_id           INTEGER,
    ground_truth      REAL,
    predicted         REAL,
    FOREIGN KEY (model_id) REFERENCES king_model(id),
    FOREIGN KEY (kinase_id) REFERENCES kinase(id)
);

CREATE TABLE blot_measurement (
    id                    INTEGER PRIMARY KEY,
    kinase_id             INTEGER NOT NULL,
    mutation_load         INTEGER NOT NULL,
    replicate             INTEGER NOT NULL,
    pixel_intensity       REAL,
    normalized_intensity  REAL,
    FOREIGN KEY (kinase_id) REFERENCES kinase(id)
);
""")


# ---------- Populate kinase table from PDB metadata ----------
print("Loading kinases...")

KINASES = [
    ("ERK2", "4ERK"),
    ("ABL1", "1IEP"),
    ("PKA",  "1ATP"),
    ("JNK3", "1JNK"),
]

PROTEIN_LENGTHS = {"ERK2": 360, "ABL1": 280, "PKA": 350, "JNK3": 400}

for name, pdb_id in KINASES:
    cur.execute(
        "INSERT INTO kinase (name, pdb_id, aa_length) VALUES (?, ?, ?)",
        (name, pdb_id, PROTEIN_LENGTHS[name])
    )

# Build a name -> id lookup so we can use it everywhere below
cur.execute("SELECT id, name FROM kinase")
kinase_id = {name: kid for kid, name in cur.fetchall()}


# ---------- Blind assignment ----------
print("Assigning blind codes...")
blind_codes = ["A", "B", "C", "D"]
for (name, _), code in zip(KINASES, blind_codes):
    cur.execute(
        "INSERT INTO blind_assignment (kinase_id, blind_code) VALUES (?, ?)",
        (kinase_id[name], code)
    )


# ---------- KING model ----------
print("Registering KING model version...")
cur.execute(
    "INSERT INTO king_model (training_date, validation_pearson_r, github_commit) VALUES (?, ?, ?)",
    ("2026-05-01", 0.853, "simulated_v1")
)
model_id = cur.lastrowid


# ---------- Helper to load a CSV into a table ----------
def load_csv(path, table, columns, transform=None):
    """Load a CSV into a SQLite table.
    columns: list of column names in the table, in the same order as the CSV columns
             (after applying transform).
    transform: optional function that takes a CSV row dict and returns a tuple of values.
    """
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            if transform:
                rows.append(transform(row))
            else:
                rows.append(tuple(row[c] for c in columns))
    placeholders = ",".join(["?"] * len(columns))
    col_list = ",".join(columns)
    cur.executemany(
        f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})",
        rows
    )
    print(f"  {table}: {len(rows)} rows")


# ---------- NMR ----------
print("Loading NMR measurements...")
load_csv(
    "data/simulated/nmr_measurements.csv",
    "nmr_measurement",
    ["kinase_id", "replicate", "residue_index", "order_parameter_s2", "t1_ms", "t2_ms"],
    transform=lambda r: (
        kinase_id[r["kinase"]], int(r["replicate"]), int(r["residue_index"]),
        float(r["order_parameter_s2"]), float(r["t1_ms"]), float(r["t2_ms"])
    )
)


# ---------- HDX ----------
print("Loading HDX measurements...")
load_csv(
    "data/simulated/hdx_measurements.csv",
    "hdx_measurement",
    ["kinase_id", "replicate", "peptide_id", "start_residue", "end_residue", "timepoint_s", "deuterium_uptake"],
    transform=lambda r: (
        kinase_id[r["kinase"]], int(r["replicate"]), int(r["peptide_id"]),
        int(r["start_residue"]), int(r["end_residue"]),
        float(r["timepoint_s"]), float(r["deuterium_uptake"])
    )
)


# ---------- KING predictions ----------
print("Loading KING predictions...")
load_csv(
    "data/simulated/king_predictions.csv",
    "king_prediction",
    ["model_id", "kinase_id", "measurement_type", "item_id", "ground_truth", "predicted"],
    transform=lambda r: (
        model_id, kinase_id[r["kinase"]], r["measurement_type"],
        int(r["residue_or_peptide_id"]), float(r["ground_truth"]), float(r["predicted"])
    )
)


# ---------- Blot measurements ----------
print("Loading blot measurements...")
load_csv(
    "data/simulated/blot_measurements.csv",
    "blot_measurement",
    ["kinase_id", "mutation_load", "replicate", "pixel_intensity", "normalized_intensity"],
    transform=lambda r: (
        kinase_id[r["kinase"]], int(r["mutation_load"]), int(r["replicate"]),
        float(r["pixel_intensity"]), float(r["normalized_intensity"])
    )
)


# ---------- Done ----------
conn.commit()
conn.close()
print(f"Database written to {DB_PATH}")