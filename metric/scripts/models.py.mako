from metric.db.schemas import Model
from metric.db.query import Query
from metric.db.datatype import *


class ${name}(Model, Query):
    """
    model ${name} for ${tablename}
    """
    __tablename__ = '${tablename}'

    # column data form models
    id = primary_key_id()
    created_at = created_at()
    updated_at = updated_at()
