import requests
from itertools import chain

from metachao import aspect

URL_BASE = 'http://hydra.nixos.org'


class cacheGet(aspect.Aspect):
    cache = aspect.aspectkw(cache=None)

    @aspect.plumb
    def get(_next, self):
        if not self.cache:
            if self.cache is None:
                self.cache = dict()
            self.cache.update(_next())
        return self.cache


def listToDict(value, key="name"):
    if isinstance(value, list):
        value = {r[key]: r for r in value}
    return value


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


def unroll_spec(spec):
    tree = dict(name='', children={})

    for path, meta in spec.iteritems():
        components = filter(None, path[1:].split('/'))
        parameters = list(meta.get("parameters", ()))
        node = tree
        for comp in components:
            children = node["children"]
            if comp not in children:
                children[comp] = dict(name=comp,
                                      children={})
            node = children[comp]

            if comp == "*":
                node["param"] = parameters.pop(0)

        node.update(meta)
        node['path'] = path

    return tree

mapping_spec = \
{ "/projects/": dict(url_pattern="/"),
  "/projects/*": dict(parameters=("project",),
                      url_pattern="/project/{project}"),
  "/jobsets/*/": dict(parameters=("project",),
                      url_pattern="/project/{project}", traverse="jobsets"),
  "/jobsets/*/*": dict(parameters=("project", "jobset"),
                       url_pattern="/jobset/{project}/{jobset}"),
  "/views/*/": dict(parameters=("project",),
                    url_pattern="/project/{project}",
                    path="views"),
  "/views/*/*": dict(parameters=("project", "view"),
                     url_pattern="/views/{project}/{view}"),
  # "/projects/*/jobsets/": dict(refer="/jobsets/*/"),
  # "/projects/*/views/": dict(refer="/views/*/")
}


class Node(object):
    def __init__(self, spec, parameters={}):
        self.spec = spec
        self.parameters = parameters

    def keys(self):
        if  "url_pattern" not in self.spec:
            return self.spec["children"].keys()
        elif self.spec["url_pattern"]:
            node = self.get()
            traverse = self.spec.get("traverse", ())
            if isinstance(traverse, str):
                traverse = (traverse,)
            for component in traverse:
                node = node[component]

            return listToDict(node).keys()
        else:
            raise AttributeError

    def __getitem__(self, key):
        children = self.spec["children"]

        if key in children:
            return Node(children[key], self.parameters)
        elif "*" in children:
            return Node(children["*"],
                        dict(chain(((children["*"]["param"], key),),
                                   self.parameters.iteritems())))

        elif self.spec["url_pattern"]:
            return self.get()[key]
        else:
            raise KeyError

    def get_url(self):
        return self.spec["url_pattern"].format(**self.parameters)

    def get(self):
        accept_header = {'Accept': 'application/json'}
        return requests.get(URL_BASE + self.get_url(),
                            headers=accept_header).json()


class Hydra(Node):
    def __init__(self):
        super(Hydra, self).__init__(unroll_spec(mapping_spec))
