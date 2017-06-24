import logging

import oandapy

from config_loader.loader import ConfigLoader

if __name__ == '__main__':
    environment, access_token = ConfigLoader.load()

    logging.basicConfig(level=logging.DEBUG)
    logging.info(f'Obtaining credentials for {environment} environment')

    oanda = oandapy.API(environment=environment, access_token=access_token)
    response = oanda.get_history()
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(response)
