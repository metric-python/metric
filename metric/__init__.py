import os
from abc import ABC, abstractmethod
from metric.src.path import auto

ROOTPATH = os.path.dirname(os.path.abspath(__name__))


class Metric(ABC):
    def __init__(self):
        pass

    def resource(self):
        # iterate the dictionary auto path resources as items key and value, then breakdown as resource, except index
        for k, v in auto('apps', 'resources', 'apps/resources').items():
            segment, uri = k.split('.'), k.replace('.', '/')

            if segment[-1] == 'index':
                segment[-1] = ''
                uri = '.'.join(segment).replace('.', '/')

            uri = uri.replace('apps/resources/', '')
            print(uri)

    @abstractmethod
    def run(self):
        pass
