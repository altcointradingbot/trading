# -*- coding: utf-8 -*-
import time
import pandas as pd
from tradingbot.ThirdParty.third_party import get_data_dir2




class Collecting(object):

    def __init__(self, exchanger, period):
        self.exchanger = exchanger
        self.period = period

    def collecting(self):
        collecting_df = pd.DataFrame(self.exchanger.get_pairs())
        collecting_df["time"] = time.ctime()
        collecting_df.to_csv(get_data_dir2() + "collecting.csv", mode="a", index=False)

    def job(self):
        i = 0
        while True:
            print("Iteration #{}".format(i))
            self.collecting()
            i += 1
            time.sleep(self.period)
