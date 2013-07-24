import requests

from metachao import aspect

URL_BASE = 'http://hydra.nixos.org/'


class cacheGet(aspect.Aspect):
    cache = aspect.aspectkw(cache=None)

    @aspect.plumb
    def get(_next, self):
        if not self.cache:
            if self.cache is None:
                self.cache = dict()
            self.cache.update(_next())
        return self.cache


def listToDict(dict, key="name"):
    if isinstance(dict, list):
        dict = {r[key]: r for r in dict}
    return dict


class traverseGet(aspect.Aspect):
    path = aspect.aspectkw(path=())

    @aspect.plumb
    def get(_next, self):
        node = _next()
        if isinstance(self.path, str):
            self.path = (self.path,)
        for component in self.path:
            node = node[component]

        return listToDict(node)


class Node(object):
    def __init__(self, *args):
        self.args = args

    def get(self):
        accept_header = {'Accept': 'application/json'}
        return requests.get(URL_BASE + self.get_url(),
                            headers=accept_header).json()

    def __getitem__(self, key):
        return self.get()[key]

    def keys(self):
        return self.get().keys()


@cacheGet
@traverseGet
class mapTree(aspect.Aspect):
    url_pattern = aspect.aspectkw(url_pattern="")
    mapping = aspect.aspectkw(mapping=None)

    def get_url(self):
        return self.url_pattern.format(*self.args)

    @aspect.plumb
    def __getitem__(_next, self, key):
        if not isinstance(self.mapping, dict):
            return self.mapping(key, *self.args)
        elif key in self.mapping:
            return self.mapping[key](*self.args)
        else:
            return _next(key)

Jobset  = mapTree(Node,
                  url_pattern="jobset/{1}/{0}",
                  mapping=dict())

Jobsets = mapTree(Node,
                  path="jobsets",
                  url_pattern="project/{0}",
                  mapping=Jobset)

Project = mapTree(Node,
                  url_pattern="project/{0}",
                  mapping=dict(jobsets=Jobsets))

Hydra   = mapTree(Node,
                  url_pattern="",
                  mapping=Project)
