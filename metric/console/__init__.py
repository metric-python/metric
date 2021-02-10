import os
import glob
from shutil import copy
from distutils.dir_util import copy_tree
from alembic.command import init

from metric.src.path import createDirectory, createPackage
from metric.src.cabin import Cabin
from metric.src import iniConfig
from metric.console.generate import configReset, migration


CABIN = Cabin()


class Installer:
    project = False

    def initialize(self, project_name):
        """
        ____This function is serve as initialize installer, and run through interface command line____

        @param project_name: string, name for your project either name or just . for current directory
        """
        if project_name != '.':
            createDirectory(os.path.join(os.getcwd(), project_name))
        self.project = os.path.join(os.getcwd(), project_name)

        init(iniConfig(self.project), self.project)

        self._buildDirectory()
        self._fileToManage()

        configReset(self.project)

    def _buildDirectory(self):
        """
        ____Function supposed to build directory, manage directory and package____
        """
        package_to_be_build = {
            'apps': ['resources', 'middlewares', 'handlers'],
            'dbs':  ['models']
        }

        directory_to_be_build = {
            'apps': ['views'],
            'dbs':  ['versions', 'fields'],
            'public': ['css', 'js', 'img'],
            '.': ['scripts']
        }

        directory_to_be_remove = ['versions']

        # ____directory to be remove____
        [os.rmdir(os.path.join(self.project, i)) for i in directory_to_be_remove]
        CABIN.info('removing unnecessary directories')

        # ____build the package needed____
        for k, v in package_to_be_build.items():
            createPackage(os.path.join(self.project, k))

            # ____build sub package____
            for i in v:
                createPackage(os.path.join(self.project, k, i))
        CABIN.info('building packages')

        # ____build the directory to sub____
        for k, v in directory_to_be_build.items():
            for i in v:
                createDirectory(os.path.join(self.project, k, i))
        CABIN.info('building directories')

    def _fileToManage(self):
        """
        ____Installer function to manage the file____
        """

        # ____remove unnecessary files____
        file_to_be_removed = ['script.py.mako']
        [os.remove(os.path.join(self.project, i)) for i in file_to_be_removed]
        CABIN.info('removing unnecessary files')

        # ____copy scripts files to project____
        scripts = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../scripts")
        [copy(file, os.path.join(self.project, 'scripts')) for file in glob.glob(os.path.join(scripts, "*.mako"))]
        CABIN.info('copy file scripts')

        copy_tree(os.path.join(scripts, "setup"), self.project)
        for file in glob.glob(os.path.join(os.path.join(scripts, "setup"), "*.py")):
            copy(file, self.project)
        CABIN.info('copy setup files')

        # ____move necessary file____
        os.rename(os.path.join(self.project, 'env.py'), os.path.join(self.project, 'scripts', 'env.py'))
        CABIN.info('move env to scripts')


def initStart(project):
    installer = Installer()
    return installer.initialize(project)
