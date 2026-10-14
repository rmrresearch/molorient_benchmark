import unittest
from unittest.mock import MagicMock, patch
from utils.get_pubchem_molecules import search_pubchem


class TestSearchPubchem(unittest.TestCase):
    @patch("utils.get_pubchem_molecules.pcp.Compound.from_cid")
    def test_generate_1000_molecules(self, mock_from_cid):
        compound = MagicMock()
        compound.to_dict.return_value = {"atoms": []}
        mock_from_cid.return_value = compound

        molecules = search_pubchem()

        self.assertEqual(len(molecules), 1000)


if __name__ == "__main__":
    unittest.main()
