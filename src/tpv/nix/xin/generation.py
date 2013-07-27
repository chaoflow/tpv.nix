import os
import tpv.cli

from plumbum import FG
from plumbum.cmd import nix_env


class Generation(tpv.cli.Command):
    """Manage generations of a profile
    """
    profile = tpv.cli.SwitchAttr(
        ['-p', '--profile'], str,
        help="Name of profile within " + os.environ['NIX_USER_PROFILE_DIR'],
    )

    @property
    def profile_path(self):
        return os.path.sep.join([os.environ['NIX_USER_PROFILE_DIR'],
                                 self.profile])

    def __call__(self):
        cmd = nix_env
        if self.profile:
            cmd = cmd[['-p', self.profile]]
        cmd['--list-generations'] & FG


class Remove(tpv.cli.Command):
    """Remove generations
    """
    profile = tpv.cli.SwitchAttr(
        ['-p', '--profile'], str,
        help="Name of profile within " + os.environ['NIX_USER_PROFILE_DIR'],
    )

    @property
    def profile_path(self):
        return os.path.sep.join([os.environ['NIX_USER_PROFILE_DIR'],
                                 self.profile])

    def __call__(self, *generations):
        cmd = nix_env
        if self.profile:
            cmd = cmd[['-p', self.profile]]
        nix_env[['--delete-generations'] + list(generations)] & FG
