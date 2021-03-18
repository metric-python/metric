import base64
import os

from alembic.config import Config
from bcrypt import gensalt
from bcrypt import hashpw
from flask import Flask
from flask_jwt_extended import JWTManager

ROOTPATH   = os.path.dirname(os.path.abspath(__name__))
APPPATH    = os.path.join(ROOTPATH, 'apps')
PUBLICPATH = os.path.join(ROOTPATH, 'public')

FLASK = Flask(__name__, static_url_path=os.path.join(ROOTPATH, 'public'))
JWT   = JWTManager(FLASK)


class Base:
    app = FLASK

    @staticmethod
    def base_configuration(path=ROOTPATH):
        return Config(os.path.join(path, 'config.ini'))

    @staticmethod
    def base_key_salted():
        key = gensalt(12)
        return base64.b64encode(key).decode('utf-8')

    @classmethod
    def hasher(cls, data, base_64_encode=False):
        """
        Convert data into hash string or convert it as base64 as well
        """
        salt_key = cls.base_configuration().get_section_option('app', 'key')
        salt_key = base64.b64decode(salt_key)
        result = hashpw(data.encode('utf-8'), salt_key)
        return base64.b64encode(result) if base_64_encode else result
