# -*- coding: utf-8 -*-
class BufferPair(object):

    def __init__(self, symbol, price, quatity):
        self.symbol = symbol
        self.price = price
        self.quantity = quatity

    def get_symbol(self):
        return self.symbol

    def get_price(self):
        return self.price

    def get_quantty(self):
        return self.quantity
