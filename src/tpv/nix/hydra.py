import requests
from itertools import chain

from metachao import aspect
from metachao.classtree import Base, OrderedDict

URL_BASE = 'http://hydra.nixos.org'


def merge_dicts(*dicts):
    return dict(chain(*(d.iteritems() for d in dicts)))


class hydra_json_get(aspect.Aspect):
    def get(self, url):
        if not url:
            return dict()
        else:
            accept_header = {'Accept': 'application/json'}
            return requests.get(URL_BASE + url,
                                headers=accept_header).json()


def list_to_dict(value, key="name"):
    if isinstance(value, list):
        value = {r[key]: r for r in value}
    return value


class traverse_get(aspect.Aspect):
    traverse = aspect.config(traverse=())

    @aspect.plumb
    def get(_next, self, url):
        node = _next(url)
        for component in self.traverse:
            node = node[component]

        return list_to_dict(node)


class attributes(aspect.Aspect):
    url_pattern = aspect.config(None)
    __attributes__ = None

    @aspect.plumb
    def __getitem__(_next, self, key):
        try:
            return _next(key)
        except KeyError:
            pass

        return self.attributes[key]

    @property
    def attributes(self):
        if self.__attributes__ is None:
            url = self.url_pattern.format(**self.parameters)
            self.__attributes__ = self.get(url)

        return self.__attributes__


class iterable_factory(aspect.Aspect):
    url_pattern = aspect.config(None)
    __factory_children__ = None

    @aspect.plumb
    def __iter__(_next, self):
        return chain(_next(), iter(self.factory_children))

    @property
    def factory_children(self):
        if self.__factory_children__ is None:
            url = self.url_pattern.format(**self.parameters)
            self.__factory_children__ = self.get(url)

        return self.__factory_children__


class factory(aspect.Aspect):
    factory_parameter = aspect.config(None)
    factory_class = aspect.config(None)

    @aspect.plumb
    def __getitem__(_next, self, key):
        try:
            return _next(key)
        except KeyError:
            pass

        parameters = merge_dicts({self.factory_parameter: key},
                                 self.parameters)
        node = self.factory_class(**parameters)
        self[key] = node
        return node


hydra_factory = aspect.compose(iterable_factory,
                               traverse_get,
                               factory)


class instantiate_with_parameters_upon_traversal(aspect.Aspect):
    """Instantiate class trees of dictionary-like nodes upon traversal"""

    @aspect.plumb
    def __init__(_next, self, **parameters):
        _next()
        self.parameters = parameters

    @aspect.plumb
    def __getitem__(_next, self, key):
        try:
            return _next(key)
        except KeyError:
            pass

        node = self.__class__[key](**self.parameters)
        self[key] = node
        return node


@hydra_json_get
@instantiate_with_parameters_upon_traversal
class HydraNode(Base, OrderedDict):
    pass


## Structure Definitions

# Views branch

@attributes(url_pattern="/view/{project}/{view}")
class View(HydraNode):
    pass


@hydra_factory(url_pattern="/project/{project}",
               traverse=("views",),
               factory_class=View,
               factory_parameter="view")
class ProjectViews(HydraNode):
    pass


@hydra_factory(url_pattern="/",
               factory_class=ProjectViews,
               factory_parameter="project")
class Views(HydraNode):
    pass


# Jobsets branch

@attributes(url_pattern="/jobset/{project}/{jobset}")
class Jobset(HydraNode):
    pass


@hydra_factory(url_pattern="/project/{project}",
               traverse=("jobsets",),
               factory_class=Jobset,
               factory_parameter="jobset")
class ProjectJobsets(HydraNode):
    pass


@hydra_factory(url_pattern="/",
               factory_class=ProjectJobsets,
               factory_parameter="project")
class Jobsets(HydraNode):
    pass


# Projects branch

@attributes(url_pattern="/project/{project}")
class Project(HydraNode):
    pass

Project['jobsets'] = ProjectJobsets
Project['views'] = ProjectViews


@hydra_factory(url_pattern="/",
               factory_class=Project,
               factory_parameter="project")
class Projects(HydraNode):
    pass


class Hydra(HydraNode):
    pass

Hydra['jobsets'] = Jobsets
Hydra['projects'] = Projects
Hydra['views'] = Views
