from __future__ import absolute_import

import unittest

from ..hydra import Hydra, \
    HydraNode, Projects, Project, \
    ProjectJobsets, Jobsets, Jobset, \
    ProjectViews, Views, View


class TestRequest(unittest.TestCase):
    # def test_hydra_keys(self):
    #     hy = Hydra()
    #     self.assertTrue(set(('nixos', 'nixpkgs')).issubset(hy.keys()))

    def test_hydra_getitem(self):
        hy = Hydra()
        self.assertTrue(isinstance(hy['projects'], Projects))
        self.assertTrue(isinstance(hy['jobsets'], Jobsets))
        self.assertTrue(isinstance(hy['views'], Views))

    def test_hydra_iter(self):
        hy = Hydra()
        self.assertEqual(set(hy), set(('projects', 'jobsets', 'views')))

    def test_projects_getitem(self):
        hy = Hydra()
        nixos = hy['projects']['nixos']

        self.assertTrue(isinstance(nixos, HydraNode))
        self.assertTrue(isinstance(nixos, Project))

    def test_projects_iter(self):
        hy = Hydra()
        projs = hy['projects']

        self.assertTrue('nixos' in projs)
        self.assertTrue(set(('nixos', 'nixpkgs')).issubset(set(projs)))
        self.assertTrue(set(('nixos', 'nixpkgs')).issubset(set(projs.keys())))
        self.assertTrue(isinstance(projs.itervalues()[0], Project))

    def test_project_getitem(self):
        hy = Hydra()
        nixos = hy['projects']['nixos']

        # Jobsets and Views sub factories
        self.assertTrue(set(("jobsets", "views")).issubset(set(nixos)))
        self.assertTrue(isinstance(nixos["jobsets"], ProjectJobsets))

    def test_jobset_getitem(self):
        hy = Hydra()
        jobsets = hy['jobsets']
        trunk = jobsets['nixos']['trunk']

        self.assertTrue(isinstance(trunk, HydraNode))
        self.assertEqual(trunk["project"], "nixos")

    # def test_hydra_keys(self):
    #     hy = Hydra()
    #     self.assertEqual(set(hy.keys()), set(("projects", "views", "jobsets")))

    # def test_project_keys(self):
    #     hy = Hydra()
    #     nixos = hy['projects']['nixos']

    #     self.assertTrue(set(("owner", "name", "jobsets", "description"))
    #                     .issubset(nixos.keys()))

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
