# -*- coding: utf-8 -*-
import hashlib
import hmac
import httplib
import json
import time
import urllib
from collections import OrderedDict
from collections import namedtuple
import tradingbot.third_party.third_party

# pylint: disable=invalid-name
API_URl = "api.livecoin.net"


def get_namedtuple(result):
    return " ".join(map(str, set(result)))


def get_data(method, *args):
    time.sleep(1)

    server = API_URl
    keys = tradingbot.third_party.third_party.get_keys()
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
    keys = tradingbot.third_party.third_party.get_keys()
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
    """
    To retrieve information on a particular currency pair for the last 24 hours. 
    There are the following fields in the response:
        *	max_bid, min_ask - maximal bid and minimal ask for the last 24 hours
        *	best_bid, best_ask - best current bid and ask

    """
    result = get_data("/exchange/ticker", *args)
    if args:
        result = [result]

    exchange_ticker = namedtuple("Exchange_ticker", get_namedtuple(result[0]))

    return [exchange_ticker(**element) for element in result]


def get_exchange_last_trades(currency_pair, *args):
    """
    To retrieve information on the latest transactions for a specified currency pair. You may receive data within the last hour or the last minute.
    """
    result = get_data("/exchange/last_trades", ("currencyPair",
                                                currency_pair), *args)

    exchange_last_trades = namedtuple("Exchange_last_trades", get_namedtuple(
        result[0]))

    return [exchange_last_trades(**element) for element in result]


def get_exchange_order_book(currency_pair, *args):
    """
    Used to get the orderbook for a given market (the grouping attribute can be set by price)
    """
    result = get_data("/exchange/order_book", ("currencyPair",
                                               currency_pair), *args)

    exchange_order_book = namedtuple("Exchange_order_book",
                                     get_namedtuple(result))

    return exchange_order_book(**result)


# problem
def get_exchange_all_order_book(*args):
    """
    Returns orderbook for every currency pair
    """
    data = get_data("/exchange/all/order_book", *args)
    exchange_all_order_book = namedtuple("Exchange_order_book",
                                         get_namedtuple(data.values()[0]))
    result = {}
    for currency in data:
        result[currency] = exchange_all_order_book(**data[currency])

    return result


def get_exchange_maxbid_minask(*args):
    """"
    Returns maximum bid and minimum ask in current orderbook
    """"
    data = get_data("/exchange/maxbid_minask", *args)
    currency_pairs = data.get("currencyPairs")
    print currency_pairs
    exchange_maxbid_minask = namedtuple("Exchange_maxbid_minask",
                                        get_namedtuple(currency_pairs[0]))

    result = [exchange_maxbid_minask(**element) for element in currency_pairs]

    return result


def get_exchange_restrictions(*args):
    """"
    Returns limits for minimum amount to open order, for each pair. Also returns maximum number of digits after the decimal point for price.
    """"
    data = get_data("/exchange/restrictions", *args)
    restrictions = data.get("restrictions")
    exchange_restrictions = namedtuple("Exchange_restrictions",
                                       get_namedtuple(restrictions[0]))
    result = [exchange_restrictions(**element) for element in restrictions]

    return result


def get_info_coin_info(*args):
    """"  
    Returns public data for currencies:
        *	name - name of cryptocurrency
        *	symbol - trading symbol of cryptocurrency
        *	walletStatus - actual status of the wallet:
            **	normal - Wallet online
            **	delayed - No new block for 1-2 hours
            **	blocked - Out of sync (no new block for at least 2 hours)
            **	blocked_long - No new block for at least 24h (Out of sync)
            **	down - Wallet temporary offline or in maintenance
            **	delisted - Coin will be delisted soon, withdraw your funds.
            **	closed_cashin - Only withdrawal is available
            **	closed_cashout - Only deposit is available
        *	withdrawFee - fee for outgoing transactions
        *	minDepositAmount - minimum amount for deposit
        *	minWithdrawAmount - minimum amount for withdrawal

    """"
    data = get_data("/info/coinInfo", *args)
    info = data.get("info")
    info_coin_info = namedtuple("Info_coin_info", get_namedtuple(info[0]))
    result = [info_coin_info(**element) for element in info]

    return result


# private user data


def get_exchange_trades(*args):
    """
    To retrieve information on your latest transactions. 
    
    This method requires authorization.
    """
    result = get_data("/exchange/trades", *args)
    if args:
        result = [result]

    exchange_trades = namedtuple("Exchange_trades",
                                 get_namedtuple(result[0]))

    return [exchange_trades(**element) for element in result]


# interaction with the system
def get_exchange_client_orders(*args):
    """
    To retrieve full information on your trade-orders for the specified currency pair. You can optionally limit the response to orders of a certain type (open, closed, etc.)
    
    This method requires authorization.
    """
    data = get_data("/info/coinInfo", *args)
    info = data.get("info")
    exchange_client_orders = namedtuple("Exchange_client_orders",
                                        get_namedtuple(info[0]))
    result = [exchange_client_orders(**element) for element in info]

    return result


def get_exchange_order(order_id):
    """
    To retrieve an order's information by its ID.
    
    This method requires authorization.

    """
    result = get_data("/exchange/order", ("orderId", order_id))

    exchange_order = namedtuple("Exchange_order", get_namedtuple(result))

    return exchange_order(**result)


def get_payment_balances(*args):
    """
    Returns an array with your balances. There are four types of balances for every currency: total, available (for trading), trade (amount in open orders), available_withdrawal (amount available for withdrawal)
    
    This method requires authorization.
    """
    result = get_data("/payment/balances", *args)

    payment_balances = namedtuple(
        "Payment_balances", get_namedtuple(result[0]))

    return [payment_balances(**element) for element in result]


def get_payment_balance(currency):
    """
    Returns available balance for selected currency

    This method requires authorization.

    """
    result = get_data("/payment/balances", ("currency", currency))
    payment_balance = namedtuple("Payment_balance", get_namedtuple(result[0]))

    return [payment_balance(**element) for element in result]


def get_payment_history_transactions(start, end, *args):
    """"
    Returns a list of your transactions

    This method requires authorization.
    """"
    result = get_data(" /payment/history/transactions", ("start", start),
                      ("end", end), *args)

    payment_history_transactions = namedtuple("Payment_history_transactions",
                                              get_namedtuple(result[0]))

    return [payment_history_transactions(**element) for element in result]


def get_payment_history_size(start, end, *args):
    """"
    Returns your transaction count for the specified period

    This method requires authorization.
    """"
    result = get_data("/payment/history/size", ("start", start),
                      ("end", end), *args)
    return result


def get_exchange_commission():
    """
    Returns actual trading fee for client

    This method requires authorization.
    """
    result = get_data("/exchange/commission", )

    exchange_commission = namedtuple("exchange_commission",
                                     get_namedtuple(result))

    return exchange_commission(**result)


def get_exchange_commission_common_info():
    """
    Returns actual trading fee and volume for the last 30 days in USD

    This method requires authorization.
    """
    result = get_data("/exchange/commissionCommonInfo", )
    exchange_commission_common_info = namedtuple("Payment_history",
                                                 get_namedtuple(result))

    return exchange_commission_common_info(**result)


def post_exchange_buy_limit(currency_pair, price, quantity):
    """
    To set a buy order (limit) for a particular currency.

    This method requires authorization.
    """
    print currency_pair, price, quantity
    result = post_data("/exchange/buylimit", ("currencyPair", currency_pair),
                       ("price", price), ("quantity", quantity))

    exchange_buy_limit = namedtuple("exchange_buy_limit",
                                    get_namedtuple(result))

    return exchange_buy_limit(**result)


def post_exchange_sell_limit(currency_pair, price, quantity):
    """
    To set a sell order (limit) for a specific currency pair. Additional parameters are similar to those for buy orders.

    This method requires authorization.
    """
    result = post_data("/exchange/selllimit", ("currencyPair", currency_pair),
                       ("price", price), ("quantity", quantity))
    exchange_sell_limit = namedtuple("exchange_sell_limit",
                                     get_namedtuple(result))

    return exchange_sell_limit(**result)


def post_exchange_buy_market(currency_pair, quantity):
    """
    Open a buy order (market) of the specified amount for a specific currency pair.

    This method requires authorization.
    """
    result = post_data("/exchange/buymarket", ("currencyPair", currency_pair),
                       ("quantity", quantity))
    exchange_buy_market = namedtuple("exchange_buy_market",
                                     get_namedtuple(result))

    return exchange_buy_market(**result)


def post_exchange_sell_market(currency_pair, quantity):
    """
    To set a sell order (market) of the specified amount for a specific currency pair.

    This method requires authorization.

    """
    result = post_data("/exchange/sellmarket", ("currencyPair", currency_pair),
                       ("quantity", quantity))
    exchange_sell_market = namedtuple("exchange_sell_market",
                                      get_namedtuple(result))

    return exchange_sell_market(**result)


def post_exchange_cancel_limit(currency_pair, order_id):
    """
    Cancel limit order.

    This method requires authorization.
    """
    result = post_data("/exchange/cancellimit",
                       ("currencyPair", currency_pair),
                       ("orderId", order_id))
    exchange_cancel_limit = namedtuple("exchange_cancel_limit",
                                       get_namedtuple(result))

    return exchange_cancel_limit(**result)
