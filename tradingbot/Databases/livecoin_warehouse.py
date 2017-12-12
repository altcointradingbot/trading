# -*- coding: utf-8 -*-
import time
from tradingbot.Databases.sqlite3_api import Sqlite3DB, Sqlite3Table
from tradingbot.Utils.Structures import BufferPair


class BufferTable(Sqlite3Table):

    def insert(self, order):
        base_request = self.data[self.table_name]["insert"]
        request = base_request.format(order.id, time.time(),
                                      order.symbol, order.price,
                                      order.quantity)
        self.set_values(request)

    def select(self, pair):
        base_request = self.data[self.table_name]["select"]
        request = base_request.format(pair)

        return self.get_values(request)

    def delete(self, pair):
        base_request = self.data[self.table_name]["delete"]
        request = base_request.format(pair)
        self.set_values(request)


class OperationsTable(Sqlite3Table):

    def insert(self, *args):
        base_request = self.data[self.table_name]["insert"]
        request = base_request.format(*args)
        self.set_values(request)

    def select(self, pair):
        base_request = self.data[self.table_name]["select"]
        request = base_request.format(pair)

        return self.get_values(request)


class LivecoinDB(Sqlite3DB):

    def __init__(self):
        Sqlite3DB.__init__(self, "livecoin")
        self.buy_table = BufferTable(self.db_name, "buy_table")
        self.sell_table = BufferTable(self.db_name, "sell_table")
        self.operations_table = OperationsTable(self.db_name,
                                                "operations_table")

    def update_orders(self, orders):
        for order in orders["buy"]:
            self.buy_table.insert(order)
        for order in orders["sell"]:
            self.sell_table.insert(order)

    def join_buy_on_sell(self):
        request = "Select symbol, count(quantity)" \
                  " from BUY_TABLE GROUP BY symbol"
        return self.buy_table.get_values(request)

    def get_payment_balances(self):
        base_request = self.data["get_payment_balances"]
        return self.get_values(base_request)

    def get_buy_pairs(self):
        base_request = self.data["get_buy_pairs"]
        return [BufferPair(x[0], x[1], x[2])
                for x in self.get_values(base_request)]

    def get_current_pairs(self):
        base_request = self.data["get_current_pairs"]
        print "get cur pairs"
        return [BufferPair(x[0], x[1], x[2])
                for x in self.get_values(base_request)]

    def add_to_operations(self, symbol):
        print "add to operations {}".format(symbol)
        self.set_values(self.data["add_to_operations"].format(symbol))
        self.set_values(self.data["buy_table"]["delete"].format(symbol))
        self.set_values(self.data["sell_table"]["delete"].format(symbol))
