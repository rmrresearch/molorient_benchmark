import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.get_pubchem_molecules import iter_pubchem

output_dir = Path(__file__).resolve().parent / "unstandardized_pubchem" / "pubchem_molecules"


def write_molecules(molecules, output_dir):
    """
    Writes each (atoms, CID) tuple to output_dir as <CID>.txt
    in XYZ format, with the CID on the comment line.
    Creates output_dir (and its parents) if it does not exist.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    for atoms_output, cid in molecules:
        atoms = atoms_output["atoms"]
        lines = [str(len(atoms)), f"CID {cid}"]
        for atom in atoms:
            lines.append(f"{atom['element']} {atom['x']} {atom['y']} {atom['z']}")
        (output_dir / f"{cid}.txt").write_text("\n".join(lines) + "\n")
        print(f"{cid}.txt", flush=True)


if __name__ == "__main__":
    write_molecules(iter_pubchem(), output_dir)
