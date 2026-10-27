def write_nwchem_input(cid, comment, elements, coords, path):
    """
    Writes a geometry-only NWChem input (no task) so NWChem prints its oriented
    geometry and exits without running an SCF. noautoz skips internal-coordinate
    generation, which errors on some molecules and does not affect the orientation.
    coords are [x, y, z] strings, written verbatim.
    """
    lines = [f"start {cid}", f'title "{comment}"', "geometry units angstroms noautoz"]
    for element, xyz in zip(elements, coords):
        lines.append(f"{element} " + " ".join(xyz))
    lines.append("end")
    path.write_text("\n".join(lines) + "\n")


def parse_nwchem_output(text):
    """
    Parses the last "Output coordinates in angstroms" table of an NWChem output.
    Returns (elements, coords) with coords as float [x, y, z], or None if absent.
    """
    i = text.rfind("Output coordinates in angstroms")
    if i < 0:
        return None
    elements, coords = [], []
    for line in text[i:].splitlines()[4:]:
        t = line.split()
        if len(t) < 6 or not t[0].isdigit():
            break
        elements.append(t[1])
        coords.append([float(v) for v in t[3:6]])
    return elements, coords


def read_xyz_strings(path):
    """
    Reads an XYZ file written by call_get_pubchem.py.
    Returns (comment_line, elements, coords) with coords as [x, y, z] strings.
    """
    lines = path.read_text().splitlines()
    n_atoms = int(lines[0])
    elements, coords = [], []
    for line in lines[2:2 + n_atoms]:
        element, x, y, z = line.split()
        elements.append(element)
        coords.append([x, y, z])
    return lines[1], elements, coords
