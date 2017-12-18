from tradingbot.algorithms.base_algorithm import BaseAlghoritm
from tradingbot.exchangers.livecoin_exchanger import LivecoinExchanger
from tradingbot.deciders.simple_decider import SimpleDecider


def main():
    algoritm = BaseAlghoritm(
        LivecoinExchanger(), SimpleDecider, "livecoin_config.json")

    algoritm.run()
