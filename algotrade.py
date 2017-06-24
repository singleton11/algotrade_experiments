import logging

import matplotlib.pyplot as plt
import oandapy
import pandas as pd

from config_loader.loader import ConfigLoader

if __name__ == '__main__':
    environment, access_token = ConfigLoader.load()

    logging.basicConfig(level=logging.DEBUG)
    logging.info(f'Obtaining credentials for {environment} environment')

    oanda = oandapy.API(environment=environment, access_token=access_token)
    response = oanda.get_history(instrument='EUR_USD')

    df = pd.DataFrame(response['candles'])

    df['closeBid'].plot()

    plt.show()
