import pandas as pd
from oandapy import API


class DecisionMaker(object):
    """Interface should every decision part of strategy implement"""

    class Constants(object):
        SELL: str = 'sell'
        BUY: str = 'buy'
        CLOSE: str = 'close'

    def decide(self, df: pd.DataFrame, api: API) -> str:
        """Make a decision

        Args:
            df: Historical data of trades
            api: API instance, was injected to be able to replace API by
                simulation to make backtesting

        Returns:
            What decider should do on market

        """
        raise NotImplementedError
