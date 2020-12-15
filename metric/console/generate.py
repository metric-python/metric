import os
from mako.template import Template
from alembic.command import revision, upgrade

from metric import ROOTPATH
from metric.src.path import createFile
from metric.src.path import createPackage
from metric.src import saltKey
from metric.src import iniConfig


def __template(t, **kwargs):
    """
    a function to generate template from mako file as resource, model and many more
    """
    if t == 'resources':
        path = ['app', 'resource']
    elif t == 'models':
        path = ['db', 'model']
    else:
        path = []

    # by default there's name key in kwargs variable parameter of this function
    try:
        name = kwargs['name']
    except KeyError as err:
        raise KeyError.with_traceback(err.__traceback__)
    else:
        if '/' in name:
            split_name = name.split('/')
            path.extend(split_name[:-1])
            name = split_name[-1]

            createPackage(os.path.join(*path))

        path.append(f'{name.lower()}.py')
        template = Template(filename=os.path.join(ROOTPATH, f'{t}.py.mako'))
        createFile(os.path.join(*path), template.render(**kwargs))


def resource(name):
    """
    Resource
    ---
    this function is serve as resource generate file and package directory
    """
    __template('resources', name=name)


def model(name, tablename):
    __template('models', name=name, tablename=tablename)


def configReset(path=os.getcwd()):
    """
    reset the configuration system
    """
    app_key = saltKey()
    app_config = iniConfig(path).file_config

    app_config.set('alembic', 'version_locations', '%(here)s/db/version')
    app_config.set('alembic', 'output_encoding', 'utf-8')

    app_config.add_section('app')
    app_config.set('app', 'key', app_key)
    app_config.set('app', 'name', 'Metric')

    with open(os.path.join(path, 'config.ini'), 'w') as f:
        app_config.write(f)
        f.close()


def migration(message, path=os.getcwd()):
    return revision(iniConfig(path), message=message)


def up_version(path=os.getcwd(), sql_mode=False):
    return upgrade(iniConfig(path), 'head', sql=sql_mode)
