import os

from metric.src import Base
from metric.src import ROOTPATH


class Conf:

    @staticmethod
    def reset(path=ROOTPATH):
        """
        ## Reset

        [ID]
            Fungsi static untuk melakukan reset pada konfigurasi.

        @param path:
        @return:
        """
        config = Base.base_configuration(path).file_config
        configuration = {
            'alembic': {
                'version_locations': '%(here)s/versions',
                'script_location': os.path.join(path, 'scripts'),
                'output_encoding': 'utf-8'
            },
            'app': {
                'name': 'Metric',
                'key': Base.base_key_salted(),
                'session_expiry': '1800'
            }
        }

        print(configuration)

        for k, v in configuration.items():
            if k != 'alembic':
                config.add_section(k)

            for x, y in v.items():
                config.set(k, x, y)

        with open(os.path.join(path, 'config.ini'), 'w') as f:
            config.write(f)
            f.close()
