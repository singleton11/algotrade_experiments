from typing import Tuple, Dict

import yaml


class ConfigLoader(object):
    """Config loader.

    Load config from yaml

    Yaml example:
        environment: 'practice'
        access_token: 'this is token'

    Examples:

    >>> ConfigLoader.load()
    'practice', 'token'

    >>> ConfigLoader.load('key.yaml')
    'practice', 'token'

    """

    class Constants(object):
        ENVIRONMENT: str = 'environment'
        ACCESS_TOKEN: str = 'access_token'

    @staticmethod
    def load(file_name: str = 'key.yaml') -> Tuple[str, str]:
        """Returns ``environment`` and ``access_token``."""
        with open(file_name) as f:
            settings: Dict[str, str] = yaml.load(f)
            return (settings.get(ConfigLoader.Constants.ENVIRONMENT),
                    settings.get(ConfigLoader.Constants.ACCESS_TOKEN))
