from typing import NamedTuple, Any, Dict

from oandapy import API


class Price(NamedTuple):
    instrument: str
    bid: float
    time: str
    ask: float
    status: str


class Account(NamedTuple):
    accountId: int
    balance: float
    accountName: str
    unrealizedPl: float
    realizedPl: float
    marginUsed: float
    marginAvail: float
    openTrades: int
    openOrders: int
    marginRate: float
    accountCurrency: str


class AvailableUnitsCalculator(object):
    RATE = 20

    def __init__(self, account_id: str, api: API,
                 instrument: str = 'EUR_USD') -> None:
        self.account_id = account_id
        self.instrument = instrument
        self.api = api

        super().__init__()

    def get_available_units(self) -> int:
        prices: Dict[str, Any] = self.api.get_prices(
            instruments=self.instrument)['prices'][0]
        price: Price = Price(**prices)
        account: Account = Account(**self.api.get_account(self.account_id))
        return int(account.marginAvail * self.RATE / price.bid)
