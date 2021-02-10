""" ____MODEL {$name}, CREATED AT: {$timestamp}_____ """

from metric.db.schemas import Model
from metric.db.query import Query
from metric.db.datatype import *


class ${name}(Model, Query):
    """
    ____Model ${name} for ${tablename} table___
    """
    __tablename__ = '${tablename}'

    # ___column data form models___
    id = primary_key_id()
    created_at = created_at()
    updated_at = updated_at()

    @staticmethod
    def hidden():
        return []
