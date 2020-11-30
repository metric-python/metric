import sys
from datetime import datetime
from logging import Logger


class Cabin:
    def __init__(self) -> None:
        self.now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    def info(self, info, **kwargs):
        log = f'{self.now}: {info}'
        sys.stdout.write(log)
