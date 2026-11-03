import shutil
import subprocess
import sys
from pathlib import Path

pointgroups_dir = Path(__file__).resolve().parent
standardized_dir = pointgroups_dir / "sno"
subdirs = ["geometries", "perturbed_geometries"]


def run_molorient(input_dir, output_dir, molorient):
    """
    Runs the molorient command (SNO orientation, 6 significant figures) on every
    molecule in input_dir. molorient writes <stem>_standardized.xyz next to
    each input; that file is moved into output_dir.
    Returns the number of molecules standardized.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = sorted(input_dir.glob("*.xyz"))
    for path in paths:
        subprocess.run([molorient, "--sno", "--precision", "6", str(path)], check=True)
        out_name = f"{path.stem}_standardized{path.suffix}"
        shutil.move(str(input_dir / out_name), str(output_dir / out_name))
        print(path.name, flush=True)

    return len(paths)


if __name__ == "__main__":
    molorient = shutil.which("molorient")
    if molorient is None:
        sys.exit("molorient command not found; activate the environment it is installed in.")

    for subdir in subdirs:
        count = run_molorient(pointgroups_dir / subdir, standardized_dir / f"{subdir}_standardized", molorient)
        print(f"Standardized {count} molecules in {subdir}.")
