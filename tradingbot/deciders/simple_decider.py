# -*- coding: utf-8 -*-
from tradingbot.utils.Structures import BufferPair
from tradingbot.exchangers_api.livecoin_api import get_exchange_ticker

SATOSHI = 0.00000001


class SimpleDecider(object):
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=unnecessary-lambda
    def __init__(self, data):
        self.exclusion_currency = data["EXCLUSION_CURRENCY"]
        self.comission = data["COMMISSION"]
        self.min_bid = 100 * SATOSHI
        self.start_pair = data["START_PAIR"]
        self.max_number_of_pairs = data["NUMBER_OF_PAIRS"]
        self.income = data["INCOME"]
        self.number_of_pairs = None
        self.balance = None
        self.small_balance = None
        self.all_pairs = None
        self.current_pairs = None

    def get_buy_solution(self, balance, all_pairs, current_pairs):
        self.balance = balance
        self.all_pairs = all_pairs
        self.current_pairs = current_pairs
        self.set_number_of_pairs()
        result = []
        if self.number_of_pairs:
            self.set_small_balance()
            correct_pairs = self.get_correct_pairs()

            result = [BufferPair(element.symbol,
                                 element.best_bid + (10 ** (-7)),
                                 self.get_quantity(element))
                      for element in correct_pairs]

            for element in result:
                print "decide to buy", element.symbol, element.quantity

        return result

    def set_small_balance(self):
        self.small_balance = self.balance / self.number_of_pairs - 10 ** (-8)

    def get_quantity(self, pair):
        return self.small_balance / ((pair.best_bid + 10 ** (-7))
                                     * (1 + self.comission))

    def set_number_of_pairs(self):
        result = self.max_number_of_pairs
        if self.balance / self.min_bid * 200 < self.max_number_of_pairs:
            result = float(self.balance / (self.min_bid * 200))
        self.number_of_pairs = max(0, result - len(self.current_pairs))

    def get_correct_pairs(self):

        pairs = [element for element in self.all_pairs if
                 "/BTC" in element.symbol and element.best_bid > self.min_bid]

        pairs = sorted(pairs, key=lambda element: get_rank(element),
                       reverse=True)

        current_symbols = [element.symbol for element in self.current_pairs
                           if element.quantity > 100 * self.min_bid]

        correct_pairs = [element for element in pairs
                         if element.symbol not in current_symbols and
                         element.symbol not in self.exclusion_currency and
                         float(element.best_ask) /
                         float(element.best_bid) < 1.5]

        end_pair = self.start_pair + self.number_of_pairs

        return correct_pairs[self.start_pair:end_pair]

    def get_sell_solution(self, pairs):
        result = []
        for pair in pairs:
            cur_value = get_exchange_ticker(("currencyPair", pair.symbol))[0]

            print "symbol {}".format(pair.symbol)
            print "buy={} now={} ratio = {} quantiy = {}".\
                format(pair.price, cur_value.best_ask,
                       cur_value.best_ask / pair.price,
                       pair.quantity)
            print "quant ", (cur_value.best_ask - 10 ** (-7)) * pair.quantity

            if (cur_value.best_ask >= pair.price * self.income or
                    cur_value.best_ask / pair.price < 0.5) and \
                    (cur_value.best_ask - 10 ** (-7)) * \
                    pair.quantity > 10 ** (-4):
                result.append(BufferPair(pair.symbol,
                                         cur_value.best_ask - 10 ** (-7),
                                         pair.quantity))
        return result


def get_rank(element):
    return ((float(element.best_ask) / float(element.best_bid) - 1)
            * float(element.volume) * float(element.vwap))


def set_buy_price(element):

    return element.best_bid + 10 ** (-7)
