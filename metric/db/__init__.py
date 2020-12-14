from alembic.util.exc import CommandError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from metric.src import iniConfig
from metric.src.cabin import Cabin


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
