from __future__ import absolute_import

import unittest

from ..hydra import Hydra, Project, Jobset, Jobsets

class TestRequest(unittest.TestCase):
    def test_hydra_keys(self):
        h = Hydra()
        self.assertTrue(set(('nixos', 'nixpkgs')).issubset(h.keys()))

    def test_hydra_getitem(self):
        h = Hydra()
        nixos = h['nixos']
        self.assertTrue(isinstance(nixos, Project))

    def test_project_keys(self):
        h = Hydra()
        nixos = h['nixos']

        self.assertTrue(set(("owner", "name", "jobsets", "description"))
                        .issubset(nixos.keys()))

    def test_project_getitem(self):
        h = Hydra()
        nixos = h['nixos']

        self.assertEqual(nixos["name"], "nixos")

        self.assertTrue(isinstance(nixos["jobsets"], Jobsets))
        self.assertTrue("trunk" in nixos["jobsets"].keys())

    def test_jobset_keys(self):
        h = Hydra()
        trunk = h['nixos']['jobsets']['trunk']

        self.assertTrue(set(("project", "errormsg", "name")).issubset(trunk.keys()))

    def test_jobset_getitem(self):
        h = Hydra()
        trunk = h['nixos']['jobsets']['trunk']

        self.assertTrue(isinstance(trunk, Jobset))
        self.assertEqual(trunk["project"], "nixos")
