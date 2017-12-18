# -*- coding: utf-8 -*-
from tradingbot.algorithms.base_algorithm import BaseAlghoritm
from tradingbot.exchangers.livecoin_exchanger import LivecoinExchanger
from tradingbot.deciders.simple_decider import SimpleDecider


BaseAlghoritm(LivecoinExchanger(),
              SimpleDecider,
              "livecoin_config.json").run()
