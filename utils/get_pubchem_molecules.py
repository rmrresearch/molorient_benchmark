import random
import pubchempy as pcp


def search_pubchem():
    """
    Randomly selects a compound from the PubChem database using
    PubChemPy. Returns a list of Atom objects and the CID used.
    """
    for _ in range(1000):
        rand_int = random.randint(1, 119000000)
        try:
            c = pcp.Compound.from_cid(rand_int, record_type="3d")
        except (pcp.BadRequestError, pcp.NotFoundError, pcp.PubChemHTTPError) as e:
            print(type(e).__name__)
            continue

        atoms_output = c.to_dict(properties=["atoms"])

        return atoms_output, rand_int

    raise RuntimeError("search_pubchem: no valid compound found after 1000 attempts.")