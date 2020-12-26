import os
from flask import send_from_directory

from metric.src import ROOTPATH
from metric.app import APP
from metric.app.resource import Resource


class Public(Resource):
    def getCss(self, path_file):
        return send_from_directory(os.path.join(ROOTPATH, 'public', 'css'), path_file)

    def getJs(self, path_file):
        return send_from_directory(os.path.join(ROOTPATH, 'public', 'js'), path_file)

    def getFont(self, path_file):
        return send_from_directory(os.path.join(ROOTPATH, 'public', 'font'), path_file)

    def getImg(self, path_file):
        return send_from_directory(os.path.join(ROOTPATH, 'public', 'img'), path_file)

    def home(self):
        return self.render('home')
