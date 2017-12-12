# -*- coding: utf-8 -*-
import json
import os
import time
from tradingbot.ThirdParty.third_party import get_config_dir


class BaseAlghoritm(object):
    # pylint: disable=too-many-instance-attributes

    def __init__(self, exchanger, decider, config_file):
        self._exchanger = exchanger
        self.config_file = os.path.join(get_config_dir(), config_file)
        with open(self.config_file) as config:
            data = json.load(config)

        self._api_url = data["API_URl"]
        self._max_waiting_time = data["MAX_WAITING_TIME"]
        self._over_burse = data["OVER_BURSE"]
        self._period = data["PERIOD"]
        self._decider = decider(data)

    def close_orders(self):
        print "close orders"
        self._exchanger.update_orders()
        self._exchanger.add_to_operations()
        self._exchanger.close_orders()

    def sell_pairs(self):
        print "sell pairs"
        current_pairs = self._exchanger.get_current_pairs()
        pairs_to_sell = self._decider.get_sell_solution(current_pairs)
        self._exchanger.make_sell_orders(pairs_to_sell)

    def buy_pairs(self):
        print "buy pairs"
        all_pairs = self._exchanger.get_pairs()
        balance = self._exchanger.get_btc_balance()
        current_pairs = self._exchanger.get_current_pairs()

        pairs_to_buy = self._decider.get_buy_solution(balance,
                                                      all_pairs, current_pairs)

        self._exchanger.make_buy_orders(pairs_to_buy)

    def run(self):
        while True:
            print "start"
            self._exchanger.get_orders()
            self.close_orders()
            self.sell_pairs()
            self.buy_pairs()
            self._exchanger.set_orders()

            print " finish"
            time.sleep(self._period)
