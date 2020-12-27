import os
import glob
from shutil import copy
from distutils.dir_util import copy_tree
from alembic.command import init

from metric.src.path import createDirectory, createPackage
from metric.src.cabin import Cabin
from metric.src import iniConfig
from metric.console.generate import configReset


def initStart(project):
    cabin = Cabin()

    if isinstance(project, str):
        if project != '.':
            createDirectory(os.path.join(os.getcwd(), project))

        project = os.path.join(os.getcwd(), project)

        init(iniConfig(project), project)
        cabin.info('Building configuration')
        build_package = {
            'app': ['resource', 'bridge', 'handler'],
            'db': ['model']
        }

        # build package
        for k, v in build_package.items():
            createPackage(os.path.join(project, k))
            for i in v:
                createPackage(os.path.join(project, k, i))

        # build directory
        dir_to_build = {
            'app': ['view'],
            'db': ['version', 'field'],
            'public': ['css', 'js', 'img']
        }
        for k, v in dir_to_build.items():
            for i in v:
                createDirectory(os.path.join(project, k, i))

        # remove unnecessary file and directory
        file_to_remove = [
            'script.py.mako'
        ]
        for i in file_to_remove:
            os.remove(os.path.join(project, i))

        dir_to_remove = [
            'versions'
        ]
        for i in dir_to_remove:
            os.rmdir(os.path.join(project, i))

        # scripts copy
        scripts = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../scripts')
        for file in glob.glob(os.path.join(scripts, "*.mako")):
            copy(file, project)

        # setup copy
        setups = os.path.join(scripts, 'setup')
        copy_tree(setups, project)
        for file in glob.glob(os.path.join(setups, "*.py")):
            copy(file, project)

        # copy directory to project path
        cabin.info(f'Copied: {project}')

        # reset config
        configReset(project)
