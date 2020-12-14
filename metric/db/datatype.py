# ____import sqlalchemy objects____
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Text, Date
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


def primary_key_id(auto=False):
    """
    ____type data for id with primary key____
    """
    if not auto:
        return Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    else:
        return Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)


def foreign_key_id(name=None, key='', **kwargs):
    """
    ____type data for id with targeted foreign key____
    """
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


def character(name=None, length=191, **kwargs):
    """
    ____type data for character or string, required parameter length and other attributes____
    """
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


def text(name=None, **kwargs):
    """
    ____type data for text character____
    """
    if name is None:
        return Column(Text(), **kwargs)
    else:
        return Column(name, Text(), **kwargs)


def number(name=None):
    """
    ____type data for number or integer with parameter____
    """
    d = {'nullable': False, 'default': 0}
    if name is None:
        return Column(Integer, **d)
    else:
        return Column(name, Integer, **d)


def boolean(name=None):
    """
    ____an custom type data for boolean it's based on every server dialect____
    """
    dialect_type = mysql.TINYINT

    d = {'nullable': False, 'default': 0}
    if name is None:
        return Column(dialect_type, **d)
    else:
        return Column(name, dialect_type, **d)


def date():
    """
    ____this is data type for date column____
    """
    return Column(Date)


def created_at(auto=False):
    """
    ____this type data is special only for created_at, which mean it's store value datetime when
    first record____
    """
    if not auto:
        return Column(DateTime, default=func.now(), nullable=False)
    else:
        return Column('created_at', DateTime, default=func.now(), nullable=False)


def updated_at(auto=False):
    """
    ____this type data is special only for updated_at, which mean it's store value when the record
    is updated or modified____
    """
    if not auto:
        return Column(DateTime, onupdate=func.now(), default=func.now(), nullable=False)
    else:
        return Column('updated_at', DateTime, onupdate=func.now(), default=func.now(), nullable=False)


def relations(to, **kwargs):
    """
    ____this is not type data column however it's a information about the relationship schema
    between tables____
    """
    return relationship(to, **kwargs)
