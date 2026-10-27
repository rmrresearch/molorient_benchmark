import pytest
from pathlib import Path

from utils.nwchem import parse_nwchem_output

nwchem_dir = Path(__file__).resolve().parent.parent / "pubchem" / "nwchem"
standardized_dir = nwchem_dir / "nwchem_standardized_pubchem"
output_dir = nwchem_dir / "nwchem_output"
subdirs = ["pubchem_molecules", "perturbed_pubchem"]

# molorient writes 6 decimals; NWChem prints 8 decimals.
tol = 1e-6


def read_standardized(path):
    lines = path.read_text().splitlines()
    rows = [line.split() for line in lines[2:2 + int(lines[0])]]
    return [r[0] for r in rows], [[float(v) for v in r[1:4]] for r in rows]


def sign_deviation(molorient, nwchem):
    """
    Largest atom deviation after giving each axis the one sign (+1 or -1,
    chosen by the sign of the axis' dot product) that best aligns it.
    """
    worst = 0.0
    for k in range(3):
        m = [c[k] for c in molorient]
        n = [c[k] for c in nwchem]
        s = 1 if sum(a * b for a, b in zip(m, n)) >= 0 else -1
        worst = max(worst, max(abs(a - s * b) for a, b in zip(m, n)))
    return worst


@pytest.mark.skipif(
    not any((standardized_dir / s).glob("*_standardized.txt") for s in subdirs if (standardized_dir / s).is_dir())
    or not any((output_dir / s).glob("*.out") for s in subdirs if (output_dir / s).is_dir()),
    reason="NWChem comparison datasets not present "
           "(run pubchem/nwchem/run_molorient_nwchem.py and pubchem/nwchem/run_nwchem.py)",
)
@pytest.mark.parametrize("subdir", subdirs)
def test_molorient_matches_nwchem_up_to_sign(subdir):
    outputs = sorted((output_dir / subdir).glob("*.out"), key=lambda p: int(p.stem))
    assert outputs, f"no NWChem outputs found in {output_dir / subdir}"
    problems = []
    for out in outputs:
        mol_path = standardized_dir / subdir / f"{out.stem}_standardized.txt"
        parsed = parse_nwchem_output(out.read_text())
        if parsed is None:
            problems.append(f"{out.stem}: no NWChem geometry")
        elif not mol_path.exists():
            problems.append(f"{out.stem}: no molorient output")
        else:
            nw_elements, nw_coords = parsed
            mo_elements, mo_coords = read_standardized(mol_path)
            if mo_elements != nw_elements:
                problems.append(f"{out.stem}: elements differ")
            else:
                dev = sign_deviation(mo_coords, nw_coords)
                if dev > tol:
                    problems.append(f"{out.stem}: max deviation {dev:.2e}")
    assert not problems, f"{len(problems)} molecules differ: {problems}"
