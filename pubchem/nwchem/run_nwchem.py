import argparse
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.nwchem import write_nwchem_input, parse_nwchem_output, read_xyz_strings

pubchem_dir = Path(__file__).resolve().parent.parent
unstandardized_dir = pubchem_dir / "unstandardized_pubchem"
output_dir = Path(__file__).resolve().parent / "nwchem_output"
subdirs = ["pubchem_molecules", "perturbed_pubchem"]


def run_one(path, out_dir, nwchem):
    """
    Writes <CID>.nw to out_dir and runs NWChem on it in a throwaway scratch
    directory, saving the output as <CID>.out. Returns True if NWChem exited
    cleanly and printed its oriented geometry.
    """
    comment, elements, coords = read_xyz_strings(path)
    input_path = out_dir / f"{path.stem}.nw"
    write_nwchem_input(path.stem, comment, elements, coords, input_path)
    with tempfile.TemporaryDirectory() as scratch:
        result = subprocess.run([nwchem, str(input_path.resolve())], cwd=scratch,
                                capture_output=True, text=True)
    (out_dir / f"{path.stem}.out").write_text(result.stdout)
    return result.returncode == 0 and parse_nwchem_output(result.stdout) is not None


def run_nwchem(input_dir, out_dir, nwchem, workers=4):
    """
    Runs NWChem (geometry-only input) on every molecule in input_dir, writing
    <CID>.nw and <CID>.out to out_dir.
    Returns (number run, list of failed file names).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = sorted((p for p in input_dir.glob("*.txt") if p.stem.isdigit()),
                   key=lambda p: int(p.stem))
    failed = []
    with ThreadPoolExecutor(workers) as pool:
        for path, ok in zip(paths, pool.map(lambda p: run_one(p, out_dir, nwchem), paths)):
            if not ok:
                failed.append(path.name)
            print(path.name if ok else f"FAILED {path.name}", flush=True)

    return len(paths) - len(failed), failed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    nwchem = shutil.which("nwchem")
    if nwchem is None:
        sys.exit("nwchem command not found.")

    for subdir in subdirs:
        count, failed = run_nwchem(unstandardized_dir / subdir, output_dir / subdir, nwchem, args.workers)
        print(f"Ran NWChem on {count} molecules in {subdir}; {len(failed)} failed {failed}.")
