import os
import importlib
from alembic.config import Config

ROOTPATH = os.path.dirname(os.path.abspath(__name__))


# ** BASE SOURCE INIT CONFIGURATION **
def iniConfig(path=ROOTPATH):
    '''
    ### INITIATE CONFIG
    ---
    function ini config in root path
    ---
    '''
    return Config(os.path.join(path, 'config.ini'))
