import datetime
import os

from mako.template import Template as _makoTemplate

from metric.src import ROOTPATH
from metric.src.package import Package


class TemplateTypeError(ValueError):
    def __init__(self, message, errors='Invalid template type!'):
        super().__init__(message)
        self.errors = errors

    def __str__(self):
        return self.errors


class TemplateMakeError(ValueError):
    def __init__(self, message, errors='Template create error!'):
        super().__init__(message)
        self.errors = errors

    def __str__(self):
        return self.errors


class Template:
    template_type = None
    template_variable = None

    def __init__(self, **kwargs):
        """
        ## Template

        [ID]
            Kelas yang di gunakan untuk mempersiapkan, dan membuat suatu file atau package beradsarkan dari template
            yang telah di sediakan

        @param kwargs: dict variable template
        """
        self.template_variable = kwargs

    def _manager(self):
        """
        ## [PRIVATE] Manager

        [ID]
            Fungsi yang di private untuk mengatur tipe template yang akan di buat.
        """
        if self.template_type is not None:
            if self.template_type == 'resource':
                self.path = ['apps', 'resources']
            elif self.template_type == 'model':
                self.path = ['models']
        else:
            raise TemplateTypeError('Available template type is resource, model and field only')

    def make(self, name):
        """
        ## Make

        [ID]
            Fungsi untuk membuat file template berdasakan dari script yang telah di sediakan oleh framework.

        @param name: file name
        """
        scripts_path = os.path.join(ROOTPATH, 'scripts')
        self._manager()

        if isinstance(name, str) and name != '':
            if '.' in name:
                split_name = name.split('.')
                self.path.extend(split_name[:-1])
                name = split_name[-1]

            template_path_join = os.path.join(*self.path)

            if not os.path.exists(template_path_join):
                Package.make_package(template_path_join)

            variable = self.template_variable
            variable['name'], variable['time'] = (name, datetime.datetime.now())

            self.path.append(f'{name.lower()}.py')
            Package.make_file(
                os.path.join(*self.path),
                _makoTemplate(
                    filename=os.path.join(scripts_path, f'{self.template_type}.py.mako')
                )
            )
        else:
            raise TemplateMakeError('Make sure the file name is string and filled!')
