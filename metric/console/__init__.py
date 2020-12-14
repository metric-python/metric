import os
import glob
from shutil import copy
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

        # build package
        for k, v in {'apps': ['resources'], 'dbs': ['models']}.items():
            createPackage(os.path.join(project, k))
            for i in v:
                createPackage(os.path.join(project, k, i))

        scripts = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../scripts')
        for file in glob.glob(os.path.join(scripts, "*.mako")):
            copy(file, project)

        # copy directory to project path
        cabin.info(f'Copied: {project}')

        # reset config
        configReset(project)

