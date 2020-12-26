import os
from mako.template import Template
from alembic.command import revision, upgrade, downgrade

from metric import ROOTPATH
from metric.src.path import createFile
from metric.src.path import createPackage
from metric.src import saltKey
from metric.src import iniConfig
from metric.src.cabin import Cabin


CABIN = Cabin()


def __template(t, **kwargs):
    """
    a function to generate template from mako file as resource, model and many more
    """
    if t == 'resources':
        path = ['app', 'resource']
    elif t == 'models':
        path = ['db', 'model']
    elif t == 'plantations':
        path = ['db', 'field']
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

            if not os.path.exists(os.path.join(*path)):
                createPackage(os.path.join(*path))

        render_var = kwargs
        render_var['name'] = name

        path.append(f'{name.lower()}.py')
        template = Template(filename=os.path.join(ROOTPATH, f'{t}.py.mako'))
        createFile(os.path.join(*path), template.render(**render_var))


def resource(name):
    """
    To generate a resource file

    :@param name: this parameter to define your name/path of the resource
    """
    __template('resources', name=name)


def model(name, table_name):
    """
    To generate a model file

    :@param name: this parameter is define your name/path of the model

    :@param table_name: parameter to define your table name of the model
    """
    __template('models', name=name, tablename=table_name)


def plantation(name):
    """
    To generate a plantation file

    :@param name: this parameter is define your name/path of the plantation
    """
    __template('plantations', name=name)


def migration(message):
    """ Function will create a new revision migration from alembic

    :@param message: a parameter to describe your migration name and message.
    """
    return revision(iniConfig(os.getcwd()), message=message)


def up_version(target='head', sql_mode=False):
    """ Upgrade version of migration available

    :@param target: parameter target of version migration

    :@param sql_mode: a toggle to show sql_mode, some kind like verbose on/off
    """
    CABIN.info('Upgrade migration!')
    return upgrade(iniConfig(os.getcwd()), target, sql=sql_mode)


def down_version(target='head', sql_mode=False):
    CABIN.info('Downgrade migration!')
    return downgrade(iniConfig(os.getcwd()), target, sql=sql_mode)


def up_plantation(name):
    from importlib import util

    spec = util.spec_from_file_location(name, os.path.join(os.getcwd(), 'db', 'field', f'{name}.py'))
    mod = util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    plant_class = getattr(mod, name.capitalize())()
    return plant_class.run()


def configReset(path=os.getcwd()):
    """
    reset the configuration system
    """
    app_key = saltKey()
    app_config = iniConfig(path).file_config

    # alembic configuration
    app_config.set('alembic', 'version_locations', '%(here)s/db/version')
    app_config.set('alembic', 'output_encoding', 'utf-8')

    # application configuration
    app_config.add_section('app')
    app_config.set('app', 'key', app_key)
    app_config.set('app', 'name', 'Metric')
    app_config.set('app', 'logs', '%(here)s/logs')

    # auth configuration
    app_config.add_section('auth')
    app_config.set('auth', 'expiry_time', '180')

    # uWSGI configuration
    app_config.add_section('uwsgi')
    app_config.set('uwsgi', 'module', 'app.wsgi')

    with open(os.path.join(path, 'config.ini'), 'w') as f:
        app_config.write(f)
        f.close()
