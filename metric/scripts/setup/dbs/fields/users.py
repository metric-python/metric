""" ____PLANTATION {$name}, CREATED AT: {$timestamp}_____ """

from metric.db.plantation import Plantation
from metric.app.helper import hashString


class Users(Plantation):
    """
    Users plantation database field!
    """
    def __init__(self):
        super(Users, self).__init__()

    def planting(self):
        """
        Function to planting your seed database here!
        """
        data = [{}, {
            'name': 'Administrator',
            'username': 'administrator',
            'email': 'administrator@metric.com',
            'password': hashString('password'),
            'is_active': 1
        }, {
            'name': 'Users',
            'username': 'users',
            'email': 'users@metric.com',
            'password': hashString('password'),
            'is_active': 1
        }]
        users = self.model.Users()
        users.add(*data)
