from metric.app.resource import Resource
from metric.db.schemas import Schemas


class Home(Resource, Schemas):
    def get(self):
        user = self.model.Users()
        user.select('')
