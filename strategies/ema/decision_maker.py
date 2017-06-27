from typing import List, Dict, NamedTuple

import pandas as pd
from oandapy import API

from ..decision_maker import DecisionMaker


class Trade(NamedTuple):
    """Interface of order"""
    side: str


class EMADecisionMaker(DecisionMaker):
    """Simple decision maker which based on EMA.

    In case when EMA crosses close price, depends from direction of price
    moving and orders places makes a decision by following rule:

         - If account has order placed on market, order should be closed
         - If close price is lesser than EMA, should buy
         - If close price is greater than EMA, should sell

    """

    def __init__(self, api: API, window: int = 10) -> None:
        """Initialize with ``window`` arg

        Args:
            window: EMA window
        """

        self.window = window
        self.api = api

        super().__init__()

    def decide(self, df: pd.DataFrame, account_id: str) -> str:
        if 'closeBid' not in df:
            raise ValueError("There are no 'closeBid' field in data frame")

        df = df['closeBid']  # Working only with close price
        df_mean: pd.DataFrame = df.ewm(com=self.window).mean()

        i: int = len(df) - 1
        diff = df[i] - df_mean[i]
        new_diff = diff

        # Checking diff and new_diff both has the same sign
        while i >= 0 and diff * new_diff >= 0:
            diff = new_diff
            i -= 1
            new_diff = df[i] - df_mean[i]

        orders: List[Dict] = self.api.get_trades(
            account_id=account_id)['trades']

        if not len(orders):
            return (DecisionMaker.Constants.SELL
                    if new_diff > 0 else DecisionMaker.Constants.BUY)
        else:
            # Obtains the first order, another should be ignored, if exists
            order: Trade = Trade(**orders[0])

            if (order.side == DecisionMaker.Constants.BUY and new_diff <= 0 or
                    order.side == DecisionMaker.Constants.SELL and
                    new_diff >= 0):
                return DecisionMaker.Constants.CLOSE
            else:
                return DecisionMaker.Constants.DO_NOTHING
