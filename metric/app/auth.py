import bcrypt
import datetime
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_raw_jwt,
                                verify_jwt_in_request,
                                get_jwt_claims)

from metric.src import ROOTPATH
from metric.src import iniConfig


class Auth:
    """
    Auth class extension for models
    
    - auth_identification is attribute for models to defined their identification field
    
    - attempt to attempt create authentication by entering the identification and password
    """
    auth_identification = 'username'
    _config = iniConfig(ROOTPATH)

    @classmethod
    def attempt(cls, **kwargs):
        """
        attempt to auth the user from database
        """
        identification = kwargs[cls.auth_identification]
        password = kwargs["password"].encode("utf-8")

        user_check = cls().select().filter(
            cls.auth_identification, identification
        ).first()
        user_check = user_check.result()

        try:
            if bcrypt.checkpw(password, user_check.password.encode("utf-8")):
                return {"identity": user_check.id}
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

    def tokenVerify(self):
        """
        function to verify the authentication token if verified 
        @return:
        """
        if verify_jwt_in_request():
            return get_jwt_claims()
        else:
            return False
