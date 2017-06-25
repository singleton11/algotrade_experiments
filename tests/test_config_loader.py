import os
import tempfile

import pytest
import yaml

from ..config_loader.loader import ConfigLoader


@pytest.fixture(scope='function', autouse=False)
def generate_yaml(request):
    tempdir = tempfile.gettempdir()
    os.chdir(tempdir)

    with open('key.yaml', 'w') as f:
        key = {
            'environment': 'practice',
            'access_token': 'access_token',
            'account_id': 'account_id',
        }

        f.write(yaml.dump(key))

        def fin():
            os.remove('key.yaml')

        request.addfinalizer(fin)


@pytest.fixture(scope='function', autouse=False)
def generate_wrong_yaml(request):
    tempdir = tempfile.gettempdir()
    os.chdir(tempdir)

    with open('key.yaml', 'w') as f:
        key = {
            'wrong': 'wrong',
        }

        f.write(yaml.dump(key))

        def fin():
            os.remove('key.yaml')

        request.addfinalizer(fin)


@pytest.mark.usefixtures('generate_yaml')
def test_file_exists_and_correct_structure():
    environment, access_token, account_id = ConfigLoader.load()
    assert environment == 'practice'
    assert access_token == 'access_token'
    assert account_id == 'account_id'


@pytest.mark.usefixtures('generate_wrong_yaml')
def test_wrong_structure():
    environment, access_token, account_id = ConfigLoader.load()
    assert environment is None
    assert access_token is None
    assert account_id is None
