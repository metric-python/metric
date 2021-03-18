import logging
from datetime import datetime

from metric.src import ini_configuration
from metric.src import ROOTPATH


class Cabin:
    _config = ini_configuration(ROOTPATH)
    _now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    def __init__(self):
        try:
            logging.basicConfig(filename=self._config.get_section_option('app', 'logs'), level=logging.INFO)
        except Exception:
            logging.basicConfig(level=logging.INFO)

    def info(self, info):
        logging.info(f'{self._now}: {info}')

    def warning(self, warning):
        logging.warning(f'{self._now}: {warning}')

    def error(self, error):
        logging.error(f'{self._now}: {error}')
