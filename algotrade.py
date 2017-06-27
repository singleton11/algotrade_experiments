import logging

import matplotlib.pyplot as plt
import oandapy
import pandas as pd

from config_loader.loader import ConfigLoader
from strategies.ema.decision_maker import EMADecisionMaker
from utils.available_units_calculator import AvailableUnitsCalculator

if __name__ == '__main__':
    environment, access_token, account_id = ConfigLoader.load()

    logging.basicConfig(level=logging.DEBUG)
    logging.info(f'Obtaining credentials for {environment} environment')

    oanda = oandapy.API(environment=environment, access_token=access_token)
    response = oanda.get_history(instrument='EUR_USD')

    df = pd.DataFrame(response['candles'])
    df_mean = df.ewm(com=10).mean()

    df['closeBid'].plot()
    df_mean['closeBid'].plot()

    decision_maker = EMADecisionMaker(oanda, account_id, 10)
    print(decision_maker.decide(df))

    print(oanda.get_prices(instruments='EUR_USD'))
    print(oanda.get_account(account_id))

    print(AvailableUnitsCalculator(account_id, oanda).get_available_units())

    plt.show()
