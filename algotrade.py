import logging

import oandapy
import pandas as pd

from config_loader.loader import ConfigLoader
from strategies.decision_maker import DecisionMaker
from strategies.ema.decision_maker import EMADecisionMaker
from utils.available_units_calculator import AvailableUnitsCalculator

if __name__ == '__main__':
    environment, access_token, account_id = ConfigLoader.load()

    logging.basicConfig(level=logging.DEBUG)
    logging.info(f'Obtaining credentials for {environment} environment')

    oanda = oandapy.API(environment=environment, access_token=access_token)

    counter = 0

    while True:
        response = oanda.get_history(instrument='EUR_USD')

        df = pd.DataFrame(response['candles'])
        df_mean = df.ewm(com=10).mean()

        decision_maker = EMADecisionMaker(oanda, account_id, 10)
        decision: str = decision_maker.decide(df)
        print(decision)

        available_units: int = AvailableUnitsCalculator(
            account_id,
            oanda
        ).get_available_units()
        print(available_units)

        if (decision == DecisionMaker.Constants.SELL or
                decision == DecisionMaker.Constants.BUY):
            oanda.create_order(account_id=account_id,
                               instrument='EUR_USD',
                               units=available_units - 1,
                               side=decision,
                               type='market')
            counter = 0
        elif decision == DecisionMaker.Constants.CLOSE and counter >= 3:
            trade = oanda.get_trades(account_id)['trades'][0]
            print(trade)
            print(oanda.close_trade(account_id, trade['id']))
        else:
            counter += 1
