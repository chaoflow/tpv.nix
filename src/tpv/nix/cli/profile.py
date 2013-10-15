import os
import re
import tpv.cli

from plumbum import FG
from plumbum.cmd import rm


class _Profile(dict):
    pass


class MyProfiles(object):
    container = os.environ['NIX_USER_PROFILE_DIR']

    def __iter__(self):
        for x in sorted(os.listdir(self.container)):
            if x.endswith('-link'):
                continue
            path = os.path.sep.join([self.container, x])
            if not os.path.islink(path):
                continue
            yield x

    def __contains__(self, key):
        # you can provide a name within container or an absolute path
        if key.startswith('/'):
            if key.startswith(self.container):
                key = key[len(self.container)+1:]
            else:
                return False
        for x in self:
            if key == x:
                return True
        return False

    def __delitem__(self, name):
        if not name in self:
            raise KeyError(name)
        rm[os.path.sep.join([self.container, name])] & FG
        for x in os.listdir(self.container):
            if re.match(name + "-\d+-link", x):
                path = os.path.sep.join([self.container, x])
                rm[path] & FG

    def __getitem__(self, name):
        if not name in self:
            raise KeyError(name)
        path = os.path.sep.join([self.container, name])
        return _Profile(name=name, path=path)

    def itervalues(self):
        for name in self:
            yield self[name]

    def values(self):
        return [x for x in self.itervalues()]


MODEL = dict(
    myprofiles=MyProfiles(),
)


class Profile(tpv.cli.Command):
    """Manage nix profiles
    """
    def __call__(self):
        for key in MODEL['myprofiles']:
            print(key)


class Remove(tpv.cli.Command):
    """Remove a profile with all its generations
    """
    @tpv.cli.completion(profiles=tpv.cli.DictDynamicCompletion(dicttree=MODEL))
    def __call__(self, *profiles):
        user_profile_path = os.readlink(os.environ['HOME'] + '/.nix-profile')
        for profile in (MODEL['myprofiles'][x] for x in profiles):
            if profile['path'] == user_profile_path:
                raise KeyError('I will not let you delete your user profile.')

        for profile in profiles:
            del MODEL['myprofiles'][profile]
