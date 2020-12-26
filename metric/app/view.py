import os
from jinja2 import FileSystemLoader
from jinja2 import Environment

from metric.src import ROOTPATH


class View:
    _path_view = os.path.join(ROOTPATH, 'app', 'view')

    def _loader(self, template_file):
        return Environment(loader=FileSystemLoader(searchpath=self._path_view))

    def render(self, file, **kwargs):
        file = file.split('.')
        file[-1] = f'{file[-1]}.html'
        loader = self._loader(file).get_template(os.path.join(*file))
        return loader.render(**kwargs)
