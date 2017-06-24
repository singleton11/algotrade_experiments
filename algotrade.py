import logging
from typing import Dict, Tuple

import yaml


class ConfigLoader(object):
    class Constants(object):
        ENVIRONMENT: str = 'environment'
        ACCESS_TOKEN: str = 'access_token'

    @staticmethod
    def load(file_name: str = 'key.yaml') -> Tuple[str, str]:
        with open(file_name) as f:
            settings: Dict[str, str] = yaml.load(f)
            return (settings.get(ConfigLoader.Constants.ENVIRONMENT),
                    settings.get(ConfigLoader.Constants.ACCESS_TOKEN))


if __name__ == '__main__':
    environment, access_token = ConfigLoader.load()

    logging.basicConfig(level=logging.DEBUG)
    logging.info(f'Obtaining credentials for {environment} environment')
