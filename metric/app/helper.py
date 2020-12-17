import bcrypt
import base64

from metric.src import iniConfig
from metric.src import ROOTPATH


def hashString(data):
    salt_key = iniConfig(ROOTPATH).get_section_option('app', 'key')
    salt_key = base64.b64decode(salt_key)
    return bcrypt.hashpw(data.encode('utf-8'), salt_key)
