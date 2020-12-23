from metric.db.schemas import Schemas


class Auth(Schemas):
    username = 'username'
    auth = None

    def trying(self, **kwargs):
        auth = self.model.Users()
        auth = auth.select()
        auth = auth.filter(
            self.username, kwargs[self.username]
        ).first()

        if auth is not None:
            return auth
        else:
            return None
