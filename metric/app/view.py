import os
from jinja2 import FileSystemLoader
from jinja2 import Environment

from metric.src import ROOTPATH


class View:
    path_views = os.path.join(ROOTPATH, 'apps', 'views')

    def _loader(self, template_file):
        print(self.path_views)
        return Environment(loader=FileSystemLoader(searchpath=self.path_views))

    def render(self, file, **kwargs):
        file = file.split('.')
        file[-1] = f'{file[-1]}.html'
        loader = self._loader(file).get_template(os.path.join(*file))
        return loader.render(**kwargs)
