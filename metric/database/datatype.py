# TODO Write comment and documentation properly here
# TODO: Create more data type Date, Decimal, and Enum

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Text, Date
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


# **PRIMARY KEY ID**
def primary_key_id(auto=False):
    """
    ## Primary key id (Datatype)

    [ID]
        primarry_key_id adalah fungsi tipe data yang bertujuan untuk mendefinisikan kolom sebagai primary key dengan
        auto_increment.
    [EN]
        primary_key_id is a data type function that supposed to define the column as the primary key with auto_increment

    :param auto: the automatic column definition, for migration purpose
    :return: Column primary_key_id
    """
    if not auto:
        return Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    else:
        return Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)


# **FOREIGN KEY ID**
def foreign_key_id(name=None, key='', **kwargs):
    if name is None:
        if 'onupdate' or 'ondelete' in kwargs:
            return Column(Integer, ForeignKey(key, **kwargs))
        else:
            return Column(Integer, ForeignKey(key))
    else:
        if 'onupdate' or 'ondelete' in kwargs:
            return Column(name, Integer, ForeignKey(key, **kwargs))
        else:
            return Column(name, Integer, ForeignKey(key))


# **CHARACTER**
def character(name=None, length=191, **kwargs):
    d = {'nullable': False, 'default': 0}
    if 'null' or 'unique' or 'default' in kwargs:
        if 'null' in kwargs:
            kwargs['nullable'] = kwargs['null']
            del kwargs['null']

        d = kwargs

    if name is None:
        return Column(String(length), **d)
    else:
        return Column(name, String(length), **d)


# **TEXT**
def text(name=None, **kwargs):
    if name is None:
        return Column(Text(), **kwargs)
    else:
        return Column(name, Text(), **kwargs)


# **NUMBER**
def number(name=None):
    d = {'nullable': False, 'default': 0}
    if name is None:
        return Column(Integer, **d)
    else:
        return Column(name, Integer, **d)


# **BOOLEAN**
def boolean(name=None):
    dialect_type = mysql.TINYINT

    d = {'nullable': False, 'default': 0}
    if name is None:
        return Column(dialect_type, **d)
    else:
        return Column(name, dialect_type, **d)


# **DATE**
def date(name=None):
    if name is not None:
        return Column(name, Date)
    else:
        return Column(Date)


# **CREATED AT**
def created_at(auto=False):
    if not auto:
        return Column(DateTime, default=func.now(), nullable=False)
    else:
        return Column('created_at', DateTime, default=func.now(), nullable=False)


# **UPDATED AT**
def updated_at(auto=False):
    if not auto:
        return Column(DateTime, onupdate=func.now(), default=func.now(), nullable=False)
    else:
        return Column('updated_at', DateTime, onupdate=func.now(), default=func.now(), nullable=False)


# **RELATIONS**
def relations(to, **kwargs):
    return relationship(to, **kwargs)
