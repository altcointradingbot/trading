# -*- coding: utf-8 -*-
from tradingbot.Utils.Structures import BufferPair
from tradingbot.ExchangersAPI.livecoin_api import get_exchange_ticker


class SimpleDecider(object):

    def __init__(self, exclusion_currency, comission, min_bid,
                 start_pair, max_number_of_pairs, income):
        self.exclusion_currency = exclusion_currency
        self.comission = comission
        self.min_bid = min_bid
        self.start_pair = start_pair
        self.max_number_of_pairs = max_number_of_pairs
        self.income = income
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

            result = map(lambda x: BufferPair(x.symbol, x.best_bid + (10 ** (-7)),
                                              self.get_quantity(x)), correct_pairs)
            for element in result:
                print "decide to buy", element.symbol, element.quantity

        return result

    def set_small_balance(self):
        self.small_balance = self.balance / self.number_of_pairs - 10 ** (-8)

    def get_quantity(self, pair):
        return self.small_balance / ((pair.best_bid + 10 ** (-7)) * (1 + self.comission))

    def set_number_of_pairs(self):
        result = self.max_number_of_pairs
        if self.balance / self.min_bid * 200 < self.max_number_of_pairs:
            result = float(self.balance / (self.min_bid * 200))
        self.number_of_pairs = max(0, result - len(self.current_pairs))

    def get_correct_pairs(self):

        pairs = [el for el in self.all_pairs if
                 "/BTC" in el.symbol and el.best_bid > self.min_bid]

        pairs = sorted(pairs, key=lambda element: get_rank(element),
                       reverse=True)

        current_symbols = [el.symbol for el in self.current_pairs
                           if el.quantity > 100 * self.min_bid]

        correct_pairs = [el for el in pairs
                         if el.symbol not in current_symbols and
                         el.symbol not in self.exclusion_currency and
                         float(el.best_ask) / float(el.best_bid) < 1.5]

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
                    (cur_value.best_ask - 10 ** (-7)) * pair.quantity > 10 ** (-4):
                result.append(BufferPair(pair.symbol,
                                         cur_value.best_ask - 10 ** (-7),
                                         pair.quantity))
        return result


def get_rank(el):
    return ((float(el.best_ask) / float(el.best_bid) - 1)
            * float(el.volume) * float(el.vwap))


def set_buy_price(x):

    return x.best_bid + 10 ** (-7)
