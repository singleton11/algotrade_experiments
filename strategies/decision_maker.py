import pandas as pd


class DecisionMaker(object):
    """Interface should every decision part of strategy implement"""

    class Constants(object):
        DO_NOTHING = 'nothing'
        SELL: str = 'sell'
        BUY: str = 'buy'
        CLOSE: str = 'close'

    def decide(self, df: pd.DataFrame) -> str:
        """Make a decision

        Args:
            df: Historical data of trades

        Returns:
            What decider should do on market

        """
        raise NotImplementedError
