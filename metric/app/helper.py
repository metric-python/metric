import bcrypt

from metric.src import iniConfig
from metric.src import ROOTPATH


def hashString(data):
    salt_key = iniConfig(ROOTPATH).get_section_option('app', 'key')
    return bcrypt.hashpw(data, salt_key)
