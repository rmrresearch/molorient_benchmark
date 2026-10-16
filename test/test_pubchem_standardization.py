import pytest
from pathlib import Path

standardized_dir = Path(__file__).resolve().parent.parent / "pubchem" / "sno" / "standardized_pubchem"
raw_dir = standardized_dir / "pubchem_molecules"
perturbed_dir = standardized_dir / "perturbed_pubchem"


@pytest.mark.skipif(
    not any(raw_dir.glob("*_standardized.txt")) or not perturbed_dir.is_dir(),
    reason="standardized PubChem datasets not present "
           "(run pubchem/run_molorient.py or untar pubchem/sno/tarred_standardized/)",
)
def test_perturbed_standardize_same_as_raw():
    raw = {p.name: p for p in raw_dir.glob("*_standardized.txt")}
    perturbed = {p.name: p for p in perturbed_dir.glob("*_standardized.txt")}
    assert raw, f"no standardized files found in {raw_dir}"
    assert raw.keys() == perturbed.keys()
    mismatched = sorted((name for name in raw if raw[name].read_text() != perturbed[name].read_text()),
                        key=lambda name: int(name.split("_")[0]))
    assert not mismatched, f"{len(mismatched)} files differ: {mismatched}"
