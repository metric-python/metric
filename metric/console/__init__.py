import os
from shutil import copytree
from metric.src.path import createDirectory, createPackage
from metric.src.cabin import Cabin


def init(project):
    cabin = Cabin()

    if isinstance(project, str):
        if project != '.':
            createDirectory(os.path.join(os.getcwd(), project))

        # build package
        createPackage(os.path.join(os.getcwd(), project, 'apps'))
        createPackage(os.path.join(os.getcwd(), project, 'apps', 'resources'))

        scripts = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../scripts')
        project = os.path.join(os.getcwd(), project, 'scripts')

        # copy directory to project path
        copytree(scripts, project)
        cabin.info(f'Copied: {project}')
