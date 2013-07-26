import requests
from itertools import chain

from metachao import aspect

URL_BASE = 'http://hydra.nixos.org'


class hydra_json_get(aspect.Aspect):
    def get(self):
        url = self.get_url()
        if not url:
            return dict()
        else:
            accept_header = {'Accept': 'application/json'}
            return requests.get(URL_BASE + self.get_url(),
                                headers=accept_header).json()


class cache_get(aspect.Aspect):
    cache = aspect.aspectkw(cache=None)

    @aspect.plumb
    def get(_next, self):
        if not self.cache:
            if self.cache is None:
                self.cache = dict()
            self.cache.update(_next())
        return self.cache


def list_to_dict(value, key="name"):
    if isinstance(value, list):
        value = {r[key]: r for r in value}
    return value


class traverse_get(aspect.Aspect):
    traverse = aspect.aspectkw(traverse=())

    @aspect.plumb
    def get(_next, self):
        node = _next()
        if isinstance(self.traverse, str):
            self.traverse = (self.traverse,)
        for component in self.traverse:
            node = node[component]

        return list_to_dict(node)


class apply_map_spec(aspect.Aspect):
    children = aspect.aspectkw(children={})
    url_pattern = aspect.aspectkw(url_pattern=None)
    parameters = aspect.aspectkw(parameters={})
    param = aspect.aspectkw(param=None)

    @aspect.plumb
    def __getitem__(_next, self, key):
        children = self.children

        if key in children:
            return HydraNode(parameters=self.parameters, **children[key])
        elif "*" in children:
            parameters = merge_dicts(self.parameters,
                                     {children["*"]["param"]: key})
            return HydraNode(parameters=parameters, **children["*"])
        else:
            return self.get()[key]

    @aspect.plumb
    def keys(_next, self):
        return merge_dicts(self.children, self.get()).keys()

    def get_url(self):
        return self.url_pattern.format(**self.parameters) \
            if self.url_pattern else None


def merge_dicts(*dicts):
    return dict(chain(*(d.iteritems() for d in dicts)))

hydra_node = aspect.compose(
    cache_get,
    traverse_get,
    hydra_json_get,
    apply_map_spec
)


class Node(object):
    def keys(self):
        raise AttributeError

    def __getitem__(self, key):
        raise KeyError


HydraNode = hydra_node(Node)


def unroll_spec(spec):
    tree = dict(children={})

    for path, meta in spec.iteritems():
        components = filter(None, path[1:].split('/'))
        keywords = list(meta.pop("parameter_keywords", ()))

        node = tree
        for comp in components:
            children = node["children"]
            if comp not in children:
                children[comp] = dict(children={})
            node = children[comp]

            if comp == "*":
                node["param"] = keywords.pop(0)

        if "refer" in meta:
            meta = spec[meta["refer"]]

        node.update(meta)
        # node['path'] = path

    return tree


mapping_spec = \
{ "/projects/": dict(url_pattern="/"),
  "/projects/*": dict(parameter_keywords=("project",),
                      url_pattern="/project/{project}"),
  "/jobsets/*/": dict(parameter_keywords=("project",),
                      url_pattern="/project/{project}", traverse="jobsets"),
  "/jobsets/*/*": dict(parameter_keywords=("project", "jobset"),
                       url_pattern="/jobset/{project}/{jobset}"),
  "/views/*/": dict(parameter_keywords=("project",),
                    url_pattern="/project/{project}",
                    traverse="views"),
  "/views/*/*": dict(parameter_keywords=("project", "view"),
                     url_pattern="/views/{project}/{view}"),
  "/projects/*/jobsets/": dict(refer="/jobsets/*/",
                               parameter_keywords=("project",)),
  "/projects/*/views/": dict(refer="/views/*/",
                             parameter_keywords=("project",))
}


Hydra = hydra_node(Node, **unroll_spec(mapping_spec))
