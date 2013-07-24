import requests

from metachao import aspect

URL_BASE = 'http://hydra.nixos.org/'


class listToDictGet(aspect.Aspect):
    key = aspect.aspectkw(key="name")

    @aspect.plumb
    def get(_next, self):
        res = _next()
        if isinstance(res, list):
            res = {r[self.key]: r
                   for r in res}
        return res


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
class mapTreeBase(aspect.Aspect):
    url_pattern = aspect.aspectkw(url_pattern="")
    mapping = aspect.aspectkw(mapping=None)

    def get_url(self):
        return self.url_pattern.format(*self.args)


class mapTreeNode(mapTreeBase):
    @aspect.plumb
    def __getitem__(_next, self, key):
        if key in self.mapping:
            return self.mapping[key](*self.args)
        else:
            return _next(key)


class mapTreeCollection(mapTreeBase):
    def keys(self):
        return self.get().keys()

    def __getitem__(self, key):
        return self.mapping(key, *self.args)


Jobset = mapTreeNode(Node,
                     url_pattern="jobset/{1}/{0}",
                     mapping=dict())

Jobsets = mapTreeCollection(Node,
                            path="jobsets",
                            url_pattern="project/{0}",
                            mapping=Jobset)

Project = mapTreeNode(Node,
                      url_pattern="project/{0}",
                      mapping=dict(jobsets=Jobsets))

Hydra = mapTreeCollection(Node,
                          url_pattern="",
                          mapping=Project)
