import bcrypt
import base64

from metric.src import iniConfig
from metric.src import ROOTPATH


def hashString(data, base_64_encode=False):
    """
    Convert data into hash string or convert it as base64 as well

    :@param data: Data need to be converted

    "@param base_64_encode: Toggle is it converted as base64 or raw hash

    :@return: base64 or just hash string
    """
    salt_key = iniConfig(ROOTPATH).get_section_option('app', 'key')
    salt_key = base64.b64decode(salt_key)
    result = bcrypt.hashpw(data.encode('utf-8'), salt_key)
    return base64.b64encode(result) if base_64_encode else result
