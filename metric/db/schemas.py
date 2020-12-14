import os

from metric.src import ROOTPATH
from metric.src.cabin import Cabin
from metric.src.path import auto


class Schemas:
    """
    ORM
    ---
    ____class ini adalah class parent yang disisipkan kedalam class lain atau bisa juga dengan cara
    di panggil seperti biasa, tapi class ini sebenarnya adalah class yang menampung object model
    yang telah di buat di dalam applikasi.____
    ---
    """
    cabin = Cabin()
    path_model = os.path.join(ROOTPATH, 'db', 'models')

    def __init__(self):
        self.model = lambda: None
        self.__gathering()

    def __gathering(self):
        for k, v in auto('db', 'models', 'db/models').items():
            setattr(self.model, v.__name__, v)
