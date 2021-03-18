import os
from abc import ABC, abstractmethod

from metric.src.path import auto
from metric.app.route import Route


class Metric(ABC, Route):
    def __init__(self):
        super(Metric, self).__init__()

    def resources(self):
        for k, v in auto('apps', 'resources', 'apps/resource').items():
            url = k.replace('apps.resources', '').split('.')[:-1]
            url = os.path.join(*url) if len(url) > 1 else ''

            self.resource(v, f'/{url}')

    @abstractmethod
    def run(self):
        pass
