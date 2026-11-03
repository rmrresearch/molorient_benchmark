import sys
from pathlib import Path

sno_dir = Path(__file__).resolve().parent
raw_dir = sno_dir / "geometries_standardized"
perturbed_dir = sno_dir / "perturbed_geometries_standardized"


def compare_dirs(raw_dir, perturbed_dir):
    """
    Compares every *_standardized.xyz file in raw_dir against the file of the
    same name in perturbed_dir, byte for byte.
    Returns (missing, mismatched, total): file names present in only one
    directory, file names whose bytes differ, and the number of names seen.
    """
    raw = {p.name: p for p in raw_dir.glob("*_standardized.xyz")}
    perturbed = {p.name: p for p in perturbed_dir.glob("*_standardized.xyz")}
    missing = sorted(raw.keys() ^ perturbed.keys())
    mismatched = sorted(name for name in raw.keys() & perturbed.keys()
                        if raw[name].read_bytes() != perturbed[name].read_bytes())
    return missing, mismatched, len(raw.keys() | perturbed.keys())


if __name__ == "__main__":
    missing, mismatched, total = compare_dirs(raw_dir, perturbed_dir)
    for name in missing:
        print(f"only in one directory: {name}")
    for name in mismatched:
        print(f"differs: {name}")
    print(f"{total - len(missing) - len(mismatched)}/{total} byte identical.")
    sys.exit(1 if missing or mismatched or total == 0 else 0)
