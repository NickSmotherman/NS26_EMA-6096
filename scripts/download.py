
import requests
import os
import json

os.makedirs("data/pdb", exist_ok=True)

KINASES = {
    "ERK2": "4ERK",
    "ABL1": "1IEP",
    "PKA":  "1ATP",
    "JNK3": "1JNK"
}

for name, pdb_id in KINASES.items():
    print(f"Downloading {name} ({pdb_id})...")

    # Downloads the structure file
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    r = requests.get(url)
    with open(f"data/pdb/{pdb_id}.pdb", "w") as f:
        f.write(r.text)

    # Downloads metadata via the PDB API
    api_url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    r = requests.get(api_url)
    with open(f"data/pdb/{pdb_id}_meta.json", "w") as f:
        json.dump(r.json(), f, indent=2)

    print(f"  Saved {pdb_id}.pdb and {pdb_id}_meta.json")

print("Download complete.")