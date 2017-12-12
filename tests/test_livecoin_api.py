import unittest

from tradingbot.ExchangersAPI.livecoin_api import get_exchange_ticker
from tradingbot.ExchangersAPI.livecoin_api import get_exchange_last_trades
from tradingbot.ExchangersAPI.livecoin_api import get_exchange_order_book
from tradingbot.ExchangersAPI.livecoin_api import get_exchange_maxbid_minask
from tradingbot.ExchangersAPI.livecoin_api import get_exchange_restrictions
from tradingbot.ExchangersAPI.livecoin_api import get_info_coin_info
from tradingbot.ExchangersAPI.livecoin_api import get_exchange_trades
from tradingbot.ExchangersAPI.livecoin_api import get_exchange_client_orders
from tradingbot.ExchangersAPI.livecoin_api import get_payment_balances
from tradingbot.ExchangersAPI.livecoin_api import get_payment_balance
from tradingbot.ExchangersAPI.livecoin_api import get_exchange_commission
from tradingbot.ExchangersAPI.livecoin_api\
    import get_exchange_commission_common_info


class TestLivecoinApi(unittest.TestCase):

    def test_get_exchange_ticker(self):
        self.assertGreater(len(get_exchange_ticker()), 0)

    def test_get_exchange_last_trades(self):
        self.assertGreater(len(get_exchange_last_trades("BTC/USD")), 0)

    def test_get_exchange_order_book(self):
        self.assertGreater(len(get_exchange_order_book("BTC/USD")), 0)

    def test_get_exchange_maxbid_minask(self):
        self.assertGreater(len(get_exchange_maxbid_minask()), 0)

    def test_get_exchange_restrictions(self):
        self.assertGreater(len(get_exchange_restrictions()), 0)

    def test_get_info_coin_info(self):
        self.assertGreater(len(get_info_coin_info()), 0)

    def test_get_exchange_trades(self):
        self.assertGreater(len(get_exchange_trades()), 0)

    def test_get_exchange_client_orders(self):
        self.assertGreater(len(get_exchange_client_orders()), 0)

    def test_get_payment_balances(self):
        self.assertGreater(len(get_payment_balances()), 0)

    def test_get_payment_balance(self):
        self.assertGreater(len(get_payment_balance("BTC")), 0)

    def test_get_exchange_commission(self):
        self.assertGreater(len(get_exchange_commission()), 0)
