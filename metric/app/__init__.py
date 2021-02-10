import os
from flask import Flask
from flask_jwt_extended import JWTManager

from metric.src import ROOTPATH


APP = Flask(__name__, static_url_path=os.path.join(ROOTPATH, 'public'))
APP.config['JWT_SECRET_KEY'] = 'JWT-SECRET-KEY'
APP.config['SECRET_KEY'] = 'SECRET_KEY'

JWT = JWTManager(APP)

APP_PATH = os.path.dirname(os.path.abspath(__file__))
