from metric.db.schemas import Model
from metric.db.query import Query
from metric.db.datatype import *
from metric.app.auth import Auth


class Users(Model, Query, Auth):
    """
    ____Model for Users, Generated when Init____
    """

    __tablename__ = 'users'

    # ____column data form models____
    id = primary_key_id()
    created_at = created_at()
    updated_at = updated_at()

    name = character()
    username = character(unique=True)
    email = character(unique=True)
    password = character()
    is_active = boolean()

    @staticmethod
    def hidden():
        """
        ____The column record you wanted to hide____

        @return: list of column to hide
        """
        return ['password']
