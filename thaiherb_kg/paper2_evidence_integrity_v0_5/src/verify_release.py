from __future__ import annotations
import csv
import hashlib
import json
import sys
from pathlib import Path

def rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def verify(root: Path):
    manifest = json.loads((root / "SHA256_MANIFEST.json").read_text(encoding="utf-8"))
    mismatches = []
    for item in manifest["files"]:
        path = root / item["path"]
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            mismatches.append(item["path"])
    assert not mismatches, f"Bad checksum(s): {mismatches}"
    chem = rows(root / "P2_CHEM_EVIDENCE_100.csv")
    compound = rows(root / "P2_COMPOUND_CANONICAL_MAP.csv")
    cross = rows(root / "P2_171_TO_174_CROSSWALK.csv")
    materials = rows(root / "P2_MATERIAL_CONTEXT_CROSSWALK.csv")
    assert len(chem) == 100 and len(compound) == 83
    assert all(x["disposition"] == "NOT_VERIFIED" for x in chem)
    assert len(cross) == 74 and sum(int(x["v3_present"]) for x in cross) == 71
    assert len(materials) == 200
    print(f"PASS {len(manifest['files'])} SHA files; 100 claims; 83 compounds; 71-to-74 crosswalk")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python verify_release.py EXTRACTED_P2_RELEASE_DIRECTORY")
    verify(Path(sys.argv[1]))
