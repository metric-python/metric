from flask import Flask
from flask_jwt_extended import JWTManager


APP = Flask(__name__)
APP.config['JWT_SECRET_KEY'] = 'JWT-SECRET-KEY'
APP.config['SECRET_KEY'] = 'SECRET_KEY'

JWT = JWTManager(APP)
