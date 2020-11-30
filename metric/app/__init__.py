import os
from flask import Flask

PROJECTPATH = os.path.dirname(os.path.abspath(__name__))

APP = Flask(__name__)
APP.config['JWT_SECRET_KEY'] = 'JWT-SECRET-KEY'


