import argparse
import csv
import random
import sys
from decimal import Decimal, getcontext
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.helpers import round_coord
from utils.random_perturbation import random_translation, random_rotation

input_dir = Path(__file__).resolve().parent / "unstandardized_pubchem" / "pubchem_molecules"
output_dir = Path(__file__).resolve().parent / "unstandardized_pubchem" / "perturbed_pubchem"


def read_xyz(path):
    """
    Reads an XYZ file written by call_get_pubchem.py.
    Returns (comment_line, elements, coords) with coords as Decimal [x, y, z].
    """
    lines = path.read_text().splitlines()
    n_atoms = int(lines[0])
    elements, coords = [], []
    for line in lines[2:2 + n_atoms]:
        element, x, y, z = line.split()
        elements.append(element)
        coords.append([Decimal(x), Decimal(y), Decimal(z)])
    return lines[1], elements, coords


def perturb_molecules(input_dir, output_dir, seed=None):
    """
    Rotates (about the origin) then translates every molecule in input_dir
    by its own random rotation and translation, writing each to output_dir
    under the same file name. Rotation angles and translations are redrawn
    if they repeat an earlier molecule's, so every molecule's are unique.
    The parameters are recorded in output_dir/perturbations.csv.
    """
    if seed is not None:
        random.seed(seed)
    # Guard digits during the math (as in molorient's orient_system); rounded to prec on output.
    getcontext().prec += 9
    output_dir.mkdir(exist_ok=True)

    paths = sorted(input_dir.glob("*.txt"), key=lambda p: int(p.stem))
    seen_angles, seen_translations = set(), set()
    rows = []
    for path in paths:
        comment, elements, coords = read_xyz(path)

        rotated, angles = random_rotation(coords)
        while tuple(angles) in seen_angles:
            rotated, angles = random_rotation(coords)
        seen_angles.add(tuple(angles))

        moved, translation = random_translation(rotated)
        while tuple(translation) in seen_translations:
            moved, translation = random_translation(rotated)
        seen_translations.add(tuple(translation))

        getcontext().prec -= 9
        lines = [str(len(elements)), comment]
        for element, (x, y, z) in zip(elements, moved):
            lines.append(f"{element} {round_coord(x)} {round_coord(y)} {round_coord(z)}")
        getcontext().prec += 9
        (output_dir / path.name).write_text("\n".join(lines) + "\n")

        cid = comment.split()[-1]
        rows.append([path.name, cid, *angles, *translation])
        print(f"{path.name} (CID {cid})", flush=True)

    with open(output_dir / "perturbations.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "cid", "yaw", "pitch", "roll", "tx", "ty", "tz"])
        writer.writerows(rows)

    getcontext().prec -= 9
    assert len(seen_angles) == len(paths)
    assert len(seen_translations) == len(paths)
    print(f"Perturbed {len(paths)} molecules, all rotations and translations unique.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    getcontext().prec = 6
    perturb_molecules(input_dir, output_dir, args.seed)
