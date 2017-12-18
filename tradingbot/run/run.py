from tradingbot.algorithms.base_algorithm import BaseAlghoritm
from tradingbot.exchangers.livecoin_exchanger import LivecoinExchanger
from tradingbot.deciders.simple_decider import SimpleDecider


Algoritm = BaseAlghoritm(LivecoinExchanger(), SimpleDecider, "livecoin_config.json")

Algoritm.run()
