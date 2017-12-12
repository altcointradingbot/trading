# -*- coding: utf-8 -*-
import hashlib
import hmac
import httplib
import json
import time
import urllib
import tradingbot.ThirdParty.third_party

from collections import OrderedDict
from collections import namedtuple

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
    if len(args):
        result = [result]

    Exchange_ticker = namedtuple("Exchange_ticker", get_namedtuple(result[0]))

    return map(lambda x: Exchange_ticker(**x), result)


def get_exchange_last_trades(currency_pair, *args):

    result = get_data("/exchange/last_trades", ("currencyPair",
                                                currency_pair), *args)

    Exchange_last_trades = namedtuple("Exchange_last_trades", get_namedtuple(
        result[0]))

    return map(lambda x: Exchange_last_trades(**x), result)


def get_exchange_order_book(currency_pair, *args):
    result = get_data("/exchange/order_book", ("currencyPair",
                                               currency_pair), *args)

    Exchange_order_book = namedtuple("Exchange_order_book",
                                     get_namedtuple(result))

    return map(lambda x: Exchange_order_book(**x), [result])


# problem
def get_exchange_all_order_book(*args):
    data = get_data("/exchange/all/order_book", *args)
    Exchange_all_order_book = namedtuple("Exchange_order_book",
                                         get_namedtuple(data.values()[0]))
    result = {}
    for currency in data:
        result[currency] = map(lambda x: Exchange_all_order_book(**x),
                               [data[currency]])

    return result


def get_exchange_maxbid_minask(*args):
    data = get_data("/exchange/maxbid_minask", *args)
    currency_pairs = data.get("currencyPairs")[0]
    Exchange_maxbid_minask = namedtuple("Exchange_maxbid_minask",
                                        get_namedtuple(currency_pairs[0]))

    result = map(lambda x: Exchange_maxbid_minask(**x), currency_pairs)

    return result


def get_exchange_restrictions(*args):
    data = get_data("/exchange/restrictions", *args)
    restrictions = data.get("restrictions")
    Exchange_restrictions = namedtuple("Exchange_restrictions",
                                       get_namedtuple(restrictions[0]))
    result = map(lambda x: Exchange_restrictions(**x), restrictions)

    return result


def get_info_coin_info(*args):
    data = get_data("/info/coinInfo", *args)
    info = data.get("info")
    Info_coin_info = namedtuple("Info_coin_info", get_namedtuple(info[0]))
    result = map(lambda x: Info_coin_info(**x), info)

    return result


# приватные данные пользователя


def get_exchange_trades(*args):
    result = get_data("/exchange/trades", *args)
    if len(args):
        result = [result]

    Exchange_trades = namedtuple("Exchange_trades",
                                 get_namedtuple(result[0]))

    return map(lambda x: Exchange_trades(**x), result)


# сложно взаимодействие с системой
def get_exchange_client_orders(*args):
    data = get_data("/info/coinInfo", *args)
    info = data.get("info")
    Exchange_client_orders = namedtuple("Exchange_client_orders",
                                        get_namedtuple(info[0]))
    result = map(lambda x: Exchange_client_orders(**x), info)

    return result


def get_exchange_order(order_id):
    result = get_data("/exchange/order", ("orderId", order_id))

    Exchange_order = namedtuple("Exchange_order", get_namedtuple(result))

    return map(lambda x: Exchange_order(**x), [result])[0]


def get_payment_balances(*args):
    result = get_data("/payment/balances", *args)

    Payment_balances = namedtuple(
        "Payment_balances", get_namedtuple(result[0]))

    return map(lambda x: Payment_balances(**x), result)


def get_payment_balance(currency):
    result = get_data("/payment/balances", ("currency", currency))
    Payment_balance = namedtuple("Payment_balance", get_namedtuple(result[0]))

    return map(lambda x: Payment_balance(**x), result)


def get_payment_history_transactions(start, end, *args):
    result = get_data(" /payment/history/transactions", ("start", start),
                      ("end", end), *args)

    Payment_history_transactions = namedtuple("Payment_history_transactions",
                                              get_namedtuple(result[0]))

    return map(lambda x: Payment_history_transactions(**x), result)


def get_payment_history_size(start, end, *args):
    result = get_data(" /payment/history/transactions", ("start", start),
                      ("end", end), *args)
    return result


def get_exchange_commission():
    result = get_data("/exchange/commission", )

    Payment_history_transactions = namedtuple("Payment_history_transactions",
                                              get_namedtuple(result))

    return map(lambda x: Payment_history_transactions(**x), [result])


def get_exchange_commission_common_info():

    result = get_data("/exchange/commissionCommonInfo", )
    Exchange_commission_common_info = namedtuple("Payment_history_transactions",
                                                 get_namedtuple(result))

    return map(lambda x: Exchange_commission_common_info(**x), [result])


def post_exchange_buy_limit(currency_pair, price, quantity):
    print currency_pair, price, quantity
    result = post_data("/exchange/buylimit", ("currencyPair", currency_pair),
                       ("price", price), ("quantity", quantity))

    Post_exchange_buy_limit = namedtuple("Post_exchange_buylimit",
                                         get_namedtuple(result))

    return map(lambda x: Post_exchange_buy_limit(**x), [result])[0]


def post_exchange_sell_limit(currency_pair, price, quantity):
    result = post_data("/exchange/selllimit", ("currencyPair", currency_pair),
                       ("price", price), ("quantity", quantity))
    Post_exchange_sell_limit = namedtuple("Post_exchange_buylimit",
                                          get_namedtuple(result))

    return map(lambda x: Post_exchange_sell_limit(**x), [result])[0]


def post_exchange_buy_market(currency_pair, quantity):
    result = post_data("/exchange/buymarket", ("currencyPair", currency_pair),
                       ("quantity", quantity))
    Post_exchange_buy_market = namedtuple("Post_exchange_buylimit",
                                          get_namedtuple(result))

    return map(lambda x: Post_exchange_buy_market(**x), [result])


def post_exchange_sell_market(currency_pair, quantity):
    result = post_data("/exchange/sellmarket", ("currencyPair", currency_pair),
                       ("quantity", quantity))
    Post_exchange_sell_market = namedtuple("Post_exchange_sellmarket",
                                           get_namedtuple(result))

    return map(lambda x: Post_exchange_sell_market(**x), [result])


def post_exchange_cancel_limit(currency_pair, order_id):
    result = post_data("/exchange/cancellimit", ("currencyPair", currency_pair),
                       ("orderId", order_id))
    Post_exchange_cancel_limit = namedtuple("Post_exchange_cancellimit",
                                            get_namedtuple(result))

    return map(lambda x: Post_exchange_cancel_limit(**x), [result])
