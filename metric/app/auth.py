import bcrypt
import datetime
from flask_jwt_extended import create_access_token, create_refresh_token

from metric.src import ROOTPATH
from metric.src import iniConfig


class Auth:
    auth_username = 'username'
    _current_time = datetime.datetime.now()
    _config = iniConfig(ROOTPATH)

    @classmethod
    def attempt(cls, **kwargs):
        """
        attempt to auth the user from database
        """
        password = kwargs['password'].encode('utf-8')
        user_check = cls().select().filter(cls.auth_username, kwargs[cls.auth_username]).first()
        user_check = user_check.result()

        try:
            if bcrypt.checkpw(password, user_check.password.encode('utf-8')):
                return {
                    'identity': user_check.id
                }
            else:
                return False

        except AttributeError:
            return None

    def createToken(self, identity):
        """
        create access and refresh token
        """
        minutes = 180

        try:
            minutes = self._config.get_section_option('auth', 'expiry_time')
        except Exception:
            pass
        finally:
            expired = datetime.timedelta(minutes=minutes)

        return {
            'token_access': create_access_token(identity=identity, expires_delta=expired),
            'token_refresh': create_refresh_token(identity=identity)
        }
