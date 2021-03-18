import os

from flask import url_for

from metric.db import ORM
from metric.db.errors import NoneTypeValue
from metric.app import APP_PATH
from metric.app.resource import Resource
from metric.app.helper import hashString
from metric.app.view import View


class Users(Resource, ORM, View):
    """
    ____API for resource users____
    """
    def __init__(self):
        super(Users, self).__init__()
        self.path_views = os.path.join(APP_PATH, 'views')

    def get(self):
        """
        ____This is API for get users record____

        @return: view render html
        """
        page = 0
        limit = 10

        try:
            if 'page' in self.requests.args:
                page = int(self.requests.args['page']) - 1

            if 'limit' in self.requests.args:
                limit = int(self.requests.args['limit'])
        except AttributeError:
            pass

        pagination = self.pagination(self.model.Users(), page, limit)
        return self.render('users.users', pagination=pagination.page, data=pagination.data)

    def get_create_or_edit_form(self, _action):
        """
        ____View GET to show form either is create or edit____

        @param _action: the action parameter type
        @return: view render html
        """
        if _action == 'create':
            return self.render('form', method='post', url=url_for('users.post'))

        elif _action == 'edit':
            try:
                data = self.model.Users()
                data = data.select().filter('id', self.requests.args['id'])

                return self.render('users.form', data=data.first(object()), method='put', url=url_for('users.post'))

            except NoneTypeValue:
                # ____return 404 because the data return is error____
                return {}

    def get_detail(self, _id):
        """
        ____View the detail information about a record of the users____

        @param _id: the ID user
        @return: view render html
        """
        try:
            data = self.model.Users()
            data = data.select().filter('id', _id)

            return self.render('users.detail', data=data.first(object()))

        except NoneTypeValue:
            # ____return 404 because the data return is error____
            return {}
        pass

    def post(self):
        """
        ____This is API to add new user record____

        @return: dictionary data
        """
        validation = self.validation(
            False,
            name='required',
            email='required, email',
            username='required',
            password='required',
        )

        # ____if errors in validation then just return____
        if 'errors' in validation:
            return validation

        # ____changing request password to hash string with helper metric____
        requests = self.requests.json
        requests['password'] = hashString(requests['password'])

        user = self.model.Users()
        user.add(**requests)
        return self.redirecting()

    def delete(self, id):
        """
        ____This is API to delete a user record____

        @param id: user id to deleted
        @return:
        """
        user = self.model.Users()
        user.destruct(id)
        return self.jsonResponse({'deleted': 'success'}, 200)
