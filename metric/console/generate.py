import os
from mako.template import Template
from metric import ROOTPATH

from metric.src.path import createFile
from metric.src.path import createPackage
from metric.src import saltKey
from metric.src import iniConfig


def __manager(t, name):
    if t == 'resources':
        path = ['apps', 'resources']
    elif t == 'models':
        path = ['db', 'models']
    else:
        path = []

    if '/' in name:
        path.extend(name.split('/')[:-1])
        name = name.split('/')[-1]
        createPackage(os.path.join(*path))

    template = Template(filename=os.path.join(ROOTPATH, f'{t}.py.mako'))
    createFile(os.path.join('apps', t, f'{name.lower()}.py'), template.render(name=name))


def resource(name):
    """
    Resource
    ---
    this function is serve as resource generate file and package directory
    """
    __manager('resources', name)


def configReset(path=os.getcwd()):
    """
    reset the configuration system
    """
    app_key = saltKey()
    app_config = iniConfig(path).file_config

    app_config.set('alembic', 'version_locations', '%(here)s/db/models/versions')
    app_config.set('alembic', 'output_encoding', 'utf-8')

    app_config.add_section('app')
    app_config.set('app', 'key', app_key)
    app_config.set('app', 'name', 'Metric')

    with open(os.path.join(path, 'config.ini'), 'w') as f:
        app_config.write(f)
        f.close()
