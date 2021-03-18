import os
from metric.app.resource import Resource
from metric.admin import ADMINSTRUCTUREPATH


class Login(Resource):
    def __init__(self):
        super(Login, self).__init__()

    def get(self):
        pass
