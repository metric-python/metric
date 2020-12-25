from abc import ABC, abstractmethod
from metric.db.schemas import Schemas


class Plantation(ABC, Schemas):
    """"
    This class is purposely to planting the value for the database initiate or etc.

    - planting: is a abstract method that you must be set for the plantation

    - run: is function to run plantation
    """
    @abstractmethod
    def planting(self):
        """
        Abstract method for plantation
        """
        pass

    def run(self):
        """
        Function for running plantation to the field
        """
        self.planting()
