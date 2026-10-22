import shutil
import subprocess
import sys
from pathlib import Path

pubchem_dir = Path(__file__).resolve().parent
unstandardized_dir = pubchem_dir / "unstandardized_pubchem"
standardized_dir = pubchem_dir / "sno" / "sno_standardized_pubchem"
subdirs = ["pubchem_molecules", "perturbed_pubchem"]


def run_molorient(input_dir, output_dir, molorient):
    """
    Runs the molorient command (SNO orientation, default precision) on every
    molecule in input_dir. molorient writes <stem>_standardized.txt next to
    each input; that file is moved into output_dir.
    Returns the number of molecules standardized.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = sorted((p for p in input_dir.glob("*.txt") if p.stem.isdigit()),
                   key=lambda p: int(p.stem))
    for path in paths:
        subprocess.run([molorient, "--sno", str(path)], check=True)
        out_name = f"{path.stem}_standardized{path.suffix}"
        shutil.move(str(input_dir / out_name), str(output_dir / out_name))
        print(path.name, flush=True)

    return len(paths)


if __name__ == "__main__":
    molorient = shutil.which("molorient")
    if molorient is None:
        sys.exit("molorient command not found; activate the environment it is installed in.")

    for subdir in subdirs:
        count = run_molorient(unstandardized_dir / subdir, standardized_dir / subdir, molorient)
        print(f"Standardized {count} molecules in {subdir}.")
