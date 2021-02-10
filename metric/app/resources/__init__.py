import os

from flask import send_from_directory
from metric.app import ROOTPATH
from metric.app.resource import Resource


class Public(Resource):
    def get(self, d, f):
        """
        ____This resource get will only get the public with 1 depth path only____

        @param d: directory public you wanted to access
        @param f: the file you wanted to accessed
        @return: the file from directory
        """
        return send_from_directory(os.path.join(ROOTPATH, 'public', d), f)
