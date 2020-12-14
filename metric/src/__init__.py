import os
import base64
from bcrypt import gensalt
from alembic.config import Config

ROOTPATH = os.path.dirname(os.path.abspath(__name__))


# ** BASE SOURCE INIT CONFIGURATION **
def iniConfig(path=ROOTPATH):
    return Config(os.path.join(path, 'config.ini'))


def saltKey():
    salt_key = gensalt(12)
    return base64.b64encode(salt_key).decode('utf8')
