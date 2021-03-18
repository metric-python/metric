import os

ADMINPATH = os.path.dirname(__file__)
ADMINSTRUCTUREPATH = {
    "root": os.path.dirname(__file__),
    "view": os.path.join(ADMINPATH, 'view')
}