import shutil
import subprocess
import sys
from pathlib import Path

pubchem_dir = Path(__file__).resolve().parent.parent
unstandardized_dir = pubchem_dir / "unstandardized_pubchem"
standardized_dir = Path(__file__).resolve().parent / "nwchem_standardized_pubchem"
subdirs = ["pubchem_molecules", "perturbed_pubchem"]


def run_molorient_nwchem(input_dir, output_dir, molorient):
    """
    Runs the molorient command (NWChem orientation, default precision) on every
    molecule in input_dir. molorient writes <stem>_standardized.txt next to
    each input; that file is moved into output_dir.
    Returns (number standardized, list of failed file names). A molecule molorient
    fails on is skipped, not fatal.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = sorted((p for p in input_dir.glob("*.txt") if p.stem.isdigit()),
                   key=lambda p: int(p.stem))
    failed = []
    for path in paths:
        result = subprocess.run([molorient, "--nwchem", str(path)], capture_output=True, text=True)
        out_name = f"{path.stem}_standardized{path.suffix}"
        if result.returncode != 0:
            failed.append(path.name)
            print(f"FAILED {path.name}", flush=True)
            continue
        shutil.move(str(input_dir / out_name), str(output_dir / out_name))
        print(path.name, flush=True)

    return len(paths) - len(failed), failed


if __name__ == "__main__":
    molorient = shutil.which("molorient")
    if molorient is None:
        sys.exit("molorient command not found; activate the environment it is installed in.")

    for subdir in subdirs:
        count, failed = run_molorient_nwchem(unstandardized_dir / subdir, standardized_dir / subdir, molorient)
        print(f"Standardized {count} molecules in {subdir}; {len(failed)} failed {failed}.")
