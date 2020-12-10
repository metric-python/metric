import os
from mako.template import Template
from metric import ROOTPATH
from metric.src.path import createFile
from metric.src.path import createPackage


def __manager(t, name):
    if t == 'resources':
        path = ['apps', 'resources']
    elif t == 'models':
        path = ['apps', 'models']
    else:
        path = []

    if '/' in name:
        path.extend(name.split('/')[:-1])
        name = name.split('/')[-1]
        createPackage(os.path.join(*path))

    template = Template(filename=os.path.join(ROOTPATH, 'scripts', f'{t}.mako'))
    createFile(os.path.join('apps', t, f'{name.lower()}.py'), template.render(name=name))


def resource(name):
    """
    Resource
    ---
    this function is serve as resource generate file and package directory
    """
    __manager('resources', name)
