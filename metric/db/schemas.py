import os
from sqlalchemy.ext.declarative import declarative_base

from metric.src import ROOTPATH
from metric.src.path import auto


Model = declarative_base()


class Schemas:
    def __init__(self):
        """
        ____Schemas is used to gather all the models registered in package models,
        and set it as attribute variable for class it self____
        """
        self.model = lambda : None
        for k, v in auto('dbs', 'models', 'dbs/models').items():
            setattr(self.model, v.__name__, v)
