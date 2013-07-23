import requests


URL_BASE = 'http://hydra.nixos.org/'


class Node(object):
    def get_json(self, rel=''):
        r = requests.get(URL_BASE + rel,
                        headers={'Accept': 'application/json'})
        return r.json()


class Hydra(Node):
    def keys(self):
        return [x['name']
                for x in self.get_json()]

    def __getitem__(self, key):
        return Project(key)


class Project(Node):
    def __init__(self, name):
        self.name = name

    def keys(self):
        return self.get_json('project/' + self.name).keys()

    def __getitem__(self, key):
        if key == 'jobsets':
            return Jobsets(self.name)
        else:
            return self.get_json('project/' + self.name)[key]


class Jobsets(Node):
    def __init__(self, project):
        self.project = project

    def keys(self):
        return [x['name']
                for x in self.get_json('project/' + self.project)["jobsets"]]

    def __getitem__(self, key):
        return Jobset(self.project, key)


class Jobset(Node):
    def __init__(self, project, name):
        self.project = project
        self.name = name

    def keys(self):
        return self.get_json('jobset/' + self.project + '/' + self.name).keys()

    def __getitem__(self, key):
        return self.get_json('jobset/' + self.project + '/' + self.name)[key]



class Evaluation(Node):
    def __getitem__(self, key):
        pass
