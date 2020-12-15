import os
from abc import ABC, abstractmethod

from metric.src.path import auto
from metric.app.routes import resource as rsc
from metric.app import APP

ROOTPATH = os.path.dirname(os.path.abspath(__name__))


class Metric(ABC):
    app = APP

    @staticmethod
    def resource():
        # iterate the dictionary auto path resources as items key and value, then breakdown as resource,
        # except index and init.
        for k, v in auto('app', 'resource', 'app/resource').items():
            url = k.replace('app.resource', '')
            url = url.split('.')[:-1]
            url = os.path.join(*url) if len(url) > 1 else ''

            rsc(v, url)

    @abstractmethod
    def run(self):
        pass
