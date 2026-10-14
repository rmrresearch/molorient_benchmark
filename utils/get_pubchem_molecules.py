import random
import pubchempy as pcp


def search_pubchem(n_molecules=1000):
    """
    Randomly selects compounds from the PubChem database using
    PubChemPy until n_molecules have been retrieved without error.
    Returns a list of (atoms, CID) tuples.
    """
    molecules = []
    seen_cids = set()
    while len(molecules) < n_molecules:
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
        molecules.append((atoms_output, rand_int))

    return molecules
