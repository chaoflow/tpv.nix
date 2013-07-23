import requests

from metachao import aspect

URL_BASE = 'http://hydra.nixos.org/'


class Node(object):
    def __init__(self, *args):
        self.args = args

    def get_json(self):
        r = requests.get(URL_BASE + self.get_url(),
                         headers={'Accept': 'application/json'})
        return r.json()

    def __getitem__(self, key):
        return self.get_json()[key]

    def keys(self):
        return self.get_json().keys()


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
    item = aspect.aspectkw(item=None)

    def keys(self):
        items = self.get_json()
        if self.item:
            items = items[self.item]

        return [x['name']
                for x in items]

    def __getitem__(self, key):
        return self.mapping(key, *self.args)


Jobset = mapTreeNode(url_pattern="jobset/{1}/{0}",
                     mapping=dict())(Node)

Jobsets = mapTreeCollection(item="jobsets",
                            url_pattern="project/{0}",
                            mapping=Jobset)(Node)

Project = mapTreeNode(url_pattern="project/{0}",
                      mapping=dict(jobsets=Jobsets))(Node)

Hydra = mapTreeCollection(url_pattern="",
                          mapping=Project)(Node)
