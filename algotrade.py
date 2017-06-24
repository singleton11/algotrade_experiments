import logging

from config_loader.loader import ConfigLoader

if __name__ == '__main__':
    environment, access_token = ConfigLoader.load()

    logging.basicConfig(level=logging.DEBUG)
    logging.info(f'Obtaining credentials for {environment} environment')
