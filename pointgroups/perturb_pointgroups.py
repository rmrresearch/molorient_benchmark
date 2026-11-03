import argparse
import random
import sys
from decimal import getcontext, localcontext
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.random_perturbation import random_translation, random_rotation
from pubchem.perturb_pubchem_molecules import read_xyz

input_dir = Path(__file__).resolve().parent / "geometries"
output_dir = Path(__file__).resolve().parent / "perturbed_geometries"


def perturb_molecules(input_dir, output_dir, seed=None, digits=20):
    """
    Rotates (about the origin) then translates every .xyz molecule in input_dir
    by its own random rotation and translation, writing each to output_dir
    under the same file name. Rotation angles and translations are redrawn
    if they repeat an earlier molecule's, so every molecule's are unique.
    Coordinates are written to `digits` significant figures, with the math done
    20 digits beyond that.
    """
    if seed is not None:
        random.seed(seed)
    orig_prec = getcontext().prec
    getcontext().prec = digits + 20
    output_dir.mkdir(exist_ok=True)

    paths = sorted(input_dir.glob("*.xyz"))
    seen_angles, seen_translations = set(), set()
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

        lines = [str(len(elements)), comment]
        with localcontext() as ctx:
            ctx.prec = digits
            for element, coord in zip(elements, moved):
                lines.append(f"{element} " + " ".join(format(+c, "f") for c in coord))
        (output_dir / path.name).write_text("\n".join(lines) + "\n")

        print(path.name, flush=True)

    getcontext().prec = orig_prec
    assert len(seen_angles) == len(paths)
    assert len(seen_translations) == len(paths)
    print(f"Perturbed {len(paths)} molecules, all rotations and translations unique.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--digits", type=int, default=20,
                        help="significant figures written for perturbed coordinates")
    args = parser.parse_args()

    perturb_molecules(input_dir, output_dir, args.seed, args.digits)
