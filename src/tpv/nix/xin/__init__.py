"""xin - prototypical unified cli for nix
"""

import os
import plumbum.commands
import tpv.cli
import tpv.pkg_resources

from plumbum import FG
from plumbum.cmd import grep
from plumbum.cmd import nix_env


class Install(tpv.cli.Command):
    """Install packages into your profile
    """
    profile = tpv.cli.SwitchAttr(
        ['-p', '--profile'], str, default="profile",
        help="Name of profile within " + os.environ['NIX_USER_PROFILE_DIR'],
    )

    @property
    def profile_path(self):
        return os.path.sep.join([os.environ['NIX_USER_PROFILE_DIR'],
                                 self.profile])

    def __call__(self, *packages):
        nix_env[['-p', self.profile_path, '-i'] + list(packages)] & FG


class Remove(tpv.cli.Command):
    """Remove packages from your profile
    """
    profile = tpv.cli.SwitchAttr(
        ['-p', '--profile'], str, default="profile",
        help="Name of profile within " + os.environ['NIX_USER_PROFILE_DIR'],
    )

    @property
    def profile_path(self):
        return os.path.sep.join([os.environ['NIX_USER_PROFILE_DIR'],
                                 self.profile])

    def __call__(self, *packages):
        nix_env[['-p', self.profile_path, '-e'] + list(packages)] & FG


class Search(tpv.cli.Command):
    """Search packages

    By default all available packages are searched. To search for
    installed packages, check the switches below. The querystr is
    passed to grep.

    """
    @property
    def profile_path(self):
        return os.path.sep.join([os.environ['NIX_USER_PROFILE_DIR'],
                                 self.profile])

    installed = tpv.cli.Flag(
        ['-i', '--installed'],
        help="Search packages installed in your profile")

    profile = tpv.cli.SwitchAttr(
        ['-p', '--profile'], str,
        help="Search packages installed in profile within " +
        os.environ['NIX_USER_PROFILE_DIR'], )

    def __call__(self, querystr='.*'):
        query = nix_env['--query', '--description']
        if self.profile:
            query = query[['--profile', self.profile_path]]
            self.installed = True

        if self.installed:
            query = query['--installed']
        else:
            query = query['--available']
        try:
            (query['*'] | grep[querystr]) & FG
        except plumbum.commands.ProcessExecutionError:
            # if query returns no lines, grep returns exit code 1,
            # resulting in a plumbum exception
            pass


class Xin(tpv.cli.Command):
    """Prototypical unified nix command line.

    Come join the discussion!
    """
    VERSION = 0

    def __call__(self):
        self.help()

tpv.pkg_resources.load_entry_points("tpv.nix.xin.commands", Xin)

app = Xin.run
