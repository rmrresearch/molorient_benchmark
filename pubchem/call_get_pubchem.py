import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.get_pubchem_molecules import iter_pubchem

output_dir = Path(__file__).resolve().parent / "pubchem_molecules"


def write_molecules(molecules, output_dir):
    """
    Writes each (atoms, CID) tuple to output_dir as 0.txt, 1.txt, ...
    in XYZ format, with the CID on the comment line.
    """
    for i, (atoms_output, cid) in enumerate(molecules):
        atoms = atoms_output["atoms"]
        lines = [str(len(atoms)), f"CID {cid}"]
        for atom in atoms:
            lines.append(f"{atom['element']} {atom['x']} {atom['y']} {atom['z']}")
        (output_dir / f"{i}.txt").write_text("\n".join(lines) + "\n")
        print(f"{i}.txt (CID {cid})", flush=True)


if __name__ == "__main__":
    write_molecules(iter_pubchem(), output_dir)
