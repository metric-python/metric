import os
from sqlalchemy.ext.declarative import declarative_base
from abc import ABCMeta

from metric.src import ROOTPATH
from metric.src.path import auto


class Schemas:
    path_model = os.path.join(ROOTPATH, 'dbs', 'models')

    def __init__(self):
        self.model = lambda: None
        self.__gathering()

    def __gathering(self):
        for k, v in auto('db', 'models', 'db/models').items():
            setattr(self.model, v.__name__, v)


class Model(declarative_base(), metaclass=ABCMeta):
    pass
