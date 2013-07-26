from __future__ import absolute_import

import unittest

from ..hydra import Hydra, Node

from metachao import aspect

class TestRequest(unittest.TestCase):
    # def test_hydra_keys(self):
    #     hy = Hydra()
    #     self.assertTrue(set(('nixos', 'nixpkgs')).issubset(hy.keys()))

    def test_hydra_getitem(self):
        hy = Hydra()
        projects = hy['projects']
        self.assertTrue(isinstance(projects, Node))

    def test_project_getitem(self):
        hy = Hydra()
        nixos = hy['projects']['nixos']

        self.assertTrue(isinstance(nixos, Node))
        self.assertEqual(nixos["name"], "nixos")

    def test_jobset_getitem(self):
        hy = Hydra()
        jobsets = hy['jobsets']
        trunk = jobsets['nixos']['trunk']

        self.assertTrue(isinstance(trunk, Node))
        self.assertEqual(trunk["project"], "nixos")

    def test_hydra_keys(self):
        hy = Hydra()
        self.assertEqual(set(hy.keys()), set(("projects", "views", "jobsets")))

    def test_project_keys(self):
        hy = Hydra()
        nixos = hy['projects']['nixos']

        self.assertTrue(set(("owner", "name", "jobsets", "description"))
                        .issubset(nixos.keys()))

    # def test_project_getitem(self):
    #     hy = Hydra()
    #     nixos = hy['nixos']

    #     self.assertEqual(nixos["name"], "nixos")

    #     # self.assertTrue(isinstance(nixos["jobsets"], Jobsets))
    #     self.assertTrue("trunk" in nixos["jobsets"].keys())

    # def test_jobset_keys(self):
    #     hy = Hydra()
    #     trunk = hy['nixos']['jobsets']['trunk']

    #     self.assertTrue(set(("project", "errormsg", "name")).issubset(trunk.keys()))

    # def test_jobset_getitem(self):
    #     hy = Hydra()
    #     trunk = hy['nixos']['jobsets']['trunk']

    #     # self.assertTrue(isinstance(trunk, Jobset))
    #     self.assertEqual(trunk["project"], "nixos")
