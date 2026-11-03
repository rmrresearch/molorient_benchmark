import re

from pointgroups.sno.compare_standardized import compare_dirs, raw_dir, perturbed_dir


def test_perturbed_standardize_same_as_raw():
    missing, mismatched, total = compare_dirs(raw_dir, perturbed_dir)
    assert total > 0, f"no standardized files found in {raw_dir}"
    assert not missing, f"files present in only one directory: {missing}"
    assert not mismatched, f"{len(mismatched)} files differ: {mismatched}"


def test_no_negative_zero():
    negative_zero = re.compile(r"(?<![\d.])-0\.0+(?![\d.])")
    flagged = sorted(
        f"{d.name}/{p.name}"
        for d in (raw_dir, perturbed_dir)
        for p in d.glob("*_standardized.xyz")
        if negative_zero.search(p.read_text())
    )
    assert not flagged, f"{len(flagged)} files contain -0 coordinates: {flagged}"
