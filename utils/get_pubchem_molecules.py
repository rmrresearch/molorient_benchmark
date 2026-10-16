import random
import pubchempy as pcp


def iter_pubchem(n_molecules=1000):
    """
    Randomly selects compounds from the PubChem database using
    PubChemPy, yielding (atoms, CID) tuples one at a time until
    n_molecules have been retrieved without error.
    """
    n_found = 0
    seen_cids = set()
    while n_found < n_molecules:
        rand_int = random.randint(1, 119000000)
        if rand_int in seen_cids:
            continue
        seen_cids.add(rand_int)
        try:
            c = pcp.Compound.from_cid(rand_int, record_type="3d")
        except (pcp.BadRequestError, pcp.NotFoundError, pcp.PubChemHTTPError) as e:
            print(type(e).__name__)
            continue

        atoms_output = c.to_dict(properties=["atoms"])
        n_found += 1
        yield atoms_output, rand_int


def search_pubchem(n_molecules=1000):
    """
    Same as iter_pubchem, but returns a list of (atoms, CID) tuples.
    """
    return list(iter_pubchem(n_molecules))
