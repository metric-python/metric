import os
from abc import ABC, abstractmethod

from metric.src import iniConfig
from metric.src.path import auto
from metric.app import APP
from metric.app.routes import resource as rsc
from metric.app.routes import route
from metric.app.helper import hashString

ROOTPATH = os.path.dirname(os.path.abspath(__name__))


class Metric(ABC):
    app = APP
    config = iniConfig(ROOTPATH)

    def __init__(self):
        from metric.app.resources import Public

        self.app.config['SECRET_KEY'] = hashString(self.config.get_section_option('app', 'name'))
        rsc(Public, '/public')

    @staticmethod
    def resource():
        """
        ____This function is used to automatically generate resources by crawling through the directory and read
        them as app resources, except init and index____
        """
        for k, v in auto('apps', 'resources', 'apps/resource').items():
            url = k.replace('apps.resources', '').split('.')[:-1]
            url = os.path.join(*url) if len(url) > 1 else ''

            rsc(v, f'/{url}')

    @abstractmethod
    def run(self):
        pass

    @staticmethod
    def admin():
        """
        ____This function is used to invoke built-in administrator system by metric____
        """
        from metric.app.resources.admin.users import Users

        register_resources = {
            'users': Users
        }

        register_routes = {
            'GET': {
                'users.get_create_or_edit_form': ['users/form/<string:_action>', Users().get_create_or_edit_form],
                'users.get_detail': ['users/detail/<int:_id>', Users().get_detail]
            },
        }

        for k, v in register_resources.items():
            rsc(v, '/admin')

        for k, v in register_routes.items():
            for sub_k, sub_v in v.items():
                route(sub_v[1], url=f'/admin/{sub_v[0]}', endpoint=sub_k, method=k)
