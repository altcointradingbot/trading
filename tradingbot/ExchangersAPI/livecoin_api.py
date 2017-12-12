# -*- coding: utf-8 -*-
import hashlib
import hmac
import httplib
import json
import time
import urllib
from collections import OrderedDict
from collections import namedtuple
import tradingbot.ThirdParty.third_party

# pylint: disable=invalid-name
API_URl = "api.livecoin.net"


def get_namedtuple(result):
    return " ".join(map(str, set(result)))


def get_data(method, *args):
    time.sleep(1)

    server = API_URl
    keys = tradingbot.ThirdParty.third_party.get_keys()
    api_key = keys[0]

    secret_key = keys[1]

    data = OrderedDict(args)

    encoded_data = urllib.urlencode(data)
    sign = hmac.new(secret_key, msg=encoded_data,
                    digestmod=hashlib.sha256).hexdigest().upper()
    headers = {"Api-key": api_key, "Sign": sign}

    conn = httplib.HTTPSConnection(server)
    conn.request("GET", method + '?' + encoded_data, '', headers)

    response = conn.getresponse()
    data = json.load(response)
    conn.close()
    return data


def post_data(method, *args):
    time.sleep(1)
    server = API_URl
    keys = tradingbot.ThirdParty.third_party.get_keys()
    api_key = keys[0]
    secret_key = keys[1]

    data = OrderedDict(args)
    encoded_data = urllib.urlencode(data)
    sign = hmac.new(secret_key, msg=encoded_data,
                    digestmod=hashlib.sha256).hexdigest().upper()
    headers = {"Api-key": api_key, "Sign": sign,
               "Content-type": "application/x-www-form-urlencoded"}

    conn = httplib.HTTPSConnection(server)
    conn.request("POST", method, encoded_data, headers)
    response = conn.getresponse()
    data = json.load(response)
    conn.close()
    return data


def get_exchange_ticker(*args):
    result = get_data("/exchange/ticker", *args)
    if args:
        result = [result]

    exchange_ticker = namedtuple("Exchange_ticker", get_namedtuple(result[0]))

    return [exchange_ticker(**element) for element in result]


def get_exchange_last_trades(currency_pair, *args):
    result = get_data("/exchange/last_trades", ("currencyPair",
                                                currency_pair), *args)

    exchange_last_trades = namedtuple("Exchange_last_trades", get_namedtuple(
        result[0]))

    return [exchange_last_trades(**element) for element in result]


def get_exchange_order_book(currency_pair, *args):
    result = get_data("/exchange/order_book", ("currencyPair",
                                               currency_pair), *args)

    exchange_order_book = namedtuple("Exchange_order_book",
                                     get_namedtuple(result))

    return exchange_order_book(**result)


# problem
def get_exchange_all_order_book(*args):
    data = get_data("/exchange/all/order_book", *args)
    exchange_all_order_book = namedtuple("Exchange_order_book",
                                         get_namedtuple(data.values()[0]))
    result = {}
    for currency in data:
        result[currency] = exchange_all_order_book(**data[currency])

    return result


def get_exchange_maxbid_minask(*args):
    data = get_data("/exchange/maxbid_minask", *args)
    currency_pairs = data.get("currencyPairs")
    print currency_pairs
    exchange_maxbid_minask = namedtuple("Exchange_maxbid_minask",
                                        get_namedtuple(currency_pairs[0]))

    result = [exchange_maxbid_minask(**element) for element in currency_pairs]

    return result


def get_exchange_restrictions(*args):
    data = get_data("/exchange/restrictions", *args)
    restrictions = data.get("restrictions")
    exchange_restrictions = namedtuple("Exchange_restrictions",
                                       get_namedtuple(restrictions[0]))
    result = [exchange_restrictions(**element) for element in restrictions]

    return result


def get_info_coin_info(*args):
    data = get_data("/info/coinInfo", *args)
    info = data.get("info")
    info_coin_info = namedtuple("Info_coin_info", get_namedtuple(info[0]))
    result = [info_coin_info(**element) for element in info]

    return result


# приватные данные пользователя


def get_exchange_trades(*args):
    result = get_data("/exchange/trades", *args)
    if args:
        result = [result]

    exchange_trades = namedtuple("Exchange_trades",
                                 get_namedtuple(result[0]))

    return [exchange_trades(**element) for element in result]


# сложно взаимодействие с системой
def get_exchange_client_orders(*args):
    data = get_data("/info/coinInfo", *args)
    info = data.get("info")
    exchange_client_orders = namedtuple("Exchange_client_orders",
                                        get_namedtuple(info[0]))
    result = [exchange_client_orders(**element) for element in info]

    return result


def get_exchange_order(order_id):
    result = get_data("/exchange/order", ("orderId", order_id))

    exchange_order = namedtuple("Exchange_order", get_namedtuple(result))

    return exchange_order(**result)


def get_payment_balances(*args):
    result = get_data("/payment/balances", *args)

    payment_balances = namedtuple(
        "Payment_balances", get_namedtuple(result[0]))

    return [payment_balances(**element) for element in result]


def get_payment_balance(currency):
    result = get_data("/payment/balances", ("currency", currency))
    payment_balance = namedtuple("Payment_balance", get_namedtuple(result[0]))

    return [payment_balance(**element) for element in result]


def get_payment_history_transactions(start, end, *args):
    result = get_data(" /payment/history/transactions", ("start", start),
                      ("end", end), *args)

    payment_history_transactions = namedtuple("Payment_history_transactions",
                                              get_namedtuple(result[0]))

    return [payment_history_transactions(**element) for element in result]


def get_payment_history_size(start, end, *args):
    result = get_data("/payment/history/size", ("start", start),
                      ("end", end), *args)
    return result


def get_exchange_commission():
    result = get_data("/exchange/commission", )

    exchange_commission = namedtuple("exchange_commission",
                                     get_namedtuple(result))

    return exchange_commission(**result)


def get_exchange_commission_common_info():
    result = get_data("/exchange/commissionCommonInfo", )
    exchange_commission_common_info = namedtuple("Payment_history",
                                                 get_namedtuple(result))

    return exchange_commission_common_info(**result)


def post_exchange_buy_limit(currency_pair, price, quantity):
    print currency_pair, price, quantity
    result = post_data("/exchange/buylimit", ("currencyPair", currency_pair),
                       ("price", price), ("quantity", quantity))

    exchange_buy_limit = namedtuple("exchange_buy_limit",
                                    get_namedtuple(result))

    return exchange_buy_limit(**result)


def post_exchange_sell_limit(currency_pair, price, quantity):
    result = post_data("/exchange/selllimit", ("currencyPair", currency_pair),
                       ("price", price), ("quantity", quantity))
    exchange_sell_limit = namedtuple("exchange_sell_limit",
                                     get_namedtuple(result))

    return exchange_sell_limit(**result)


def post_exchange_buy_market(currency_pair, quantity):
    result = post_data("/exchange/buymarket", ("currencyPair", currency_pair),
                       ("quantity", quantity))
    exchange_buy_market = namedtuple("exchange_buy_market",
                                     get_namedtuple(result))

    return exchange_buy_market(**result)


def post_exchange_sell_market(currency_pair, quantity):
    result = post_data("/exchange/sellmarket", ("currencyPair", currency_pair),
                       ("quantity", quantity))
    exchange_sell_market = namedtuple("exchange_sell_market",
                                      get_namedtuple(result))

    return exchange_sell_market(**result)


def post_exchange_cancel_limit(currency_pair, order_id):
    result = post_data("/exchange/cancellimit",
                       ("currencyPair", currency_pair),
                       ("orderId", order_id))
    exchange_cancel_limit = namedtuple("exchange_cancel_limit",
                                       get_namedtuple(result))

    return exchange_cancel_limit(**result)
