from math import ceil
from alembic.util.exc import CommandError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from metric.src import iniConfig
from metric.src.cabin import Cabin
from metric.src.path import auto

Model = declarative_base()


def session(connection=False):
    '''
    session(conection=bool(True/False))
    ---
    ____fungsi ini digunakan untuk system melakukan koneksi sesi ke database dengan menggunakan
    sesi yang ada pada fungsi sqlalchemy, dan konfigurasi .ini menggunakan alembic konfigurasi.
    parameter connection berfungsi sebagai penanda dari sesi koneksi dalam boolean, jika "True"
    maka koneksi akan digunakan untuk membuat engine, jika tidak koneksi digunakan untuk mengikat
    sesi pada database____
    ---
    '''
    config = iniConfig()
    try:
        url = config.get_main_option('sqlalchemy.url')
    except CommandError as e:
        raise e
    else:
        if not connection:
            session_ng = sessionmaker(bind=create_engine(url), expire_on_commit=False)
            return session_ng()
        else:
            return create_engine(url).begin()


class ORM:
    def __init__(self):
        """
        ____ORM class is the ORM class wizard to gather and summon all the models registered and
        send it to the attribute class____
        """
        self.model = lambda: None
        for k, v in auto('dbs', 'models', 'dbs/models').items():
            setattr(self.model, v.__name__, v)

    def pagination(self, model, page=0, limit=10, *args):
        """

        @param model:
        @param page:
        @param limit:
        @param args:
        """
        result = lambda: None
        record_count = model.count()
        record_pagination = '<ul class="uk-pagination">'

        for i in range(1, ceil(record_count / limit) + 1):
            record_pagination += '<li class="uk-active">' if i - 1 == page else '<li>'
            record_pagination += f'<a href="?page={i}">{i}</a></li>'

        record_pagination += '</ul>'
        record_data = model.select(*args) if args else model.select()

        setattr(result, 'total', record_count)
        setattr(result, 'page', record_pagination)
        setattr(result, 'data', record_data)

        result.data = result.data.grab(page, limit).all()
        return result
