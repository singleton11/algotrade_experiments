import os

import pytest
import yaml

from ..config_loader.loader import ConfigLoader


@pytest.fixture(scope='function', autouse=False)
def generate_yaml(request):
    with open('key.yaml', 'w') as f:
        key = {
            'environment': 'practice',
            'access_token': 'access_token'
        }

        f.write(yaml.dump(key))

        def fin():
            os.remove('key.yaml')

        request.addfinalizer(fin)


@pytest.mark.usefixtures('generate_yaml')
def test_file_exists_and_correct_structure():
    environment, access_token = ConfigLoader.load()
    assert environment == 'practice'
    assert access_token == 'access_token'
