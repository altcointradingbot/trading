# -*- coding: utf-8 -*-
from tradingbot.Algorithms.base_algorithm import BaseAlghoritm
from tradingbot.Exchangers.livecoin_exchanger import LivecoinExchanger
from tradingbot.Deciders.simple_decider import SimpleDecider


testing = BaseAlghoritm(LivecoinExchanger(),
                        SimpleDecider,
                        "livecoin_config.json")

testing.run()
