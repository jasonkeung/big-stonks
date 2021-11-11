from datetime import datetime, tzinfo
import pytz
import math
import pandas as pd

from trader import Trader
from order import Order

class MoonTrader(Trader):

    def run(self):
        """
        Buys on new moons and sells on full moons for 2021.

        :return: None
        """
        new_moons = ['01-12', '02-11', '03-13', '04-11', '05-11', '06-10', '07-09', '08-08', '09-06', '10-06', '11-04', '12-03']
        full_moons = ['01-28', '02-27', '03-28', '04-26', '05-26', '06-24', '07-23', '08-22', '09-20', '10-20', '11-19', '12-28']

        # convert new and full moons to datetime objects
        for i in range(len(new_moons)):
            new_moons[i] = datetime.strptime('2021-' + new_moons[i], '%Y-%m-%d')
            new_moons[i] = new_moons[i].astimezone(pytz.timezone('US/Eastern'))

        for i in range(len(full_moons)):
            full_moons[i] = datetime.strptime('2021-' + full_moons[i], '%Y-%m-%d')
            full_moons[i] = full_moons[i].astimezone(pytz.timezone('US/Eastern'))

        all_moons = []
        all_moons.extend(new_moons)
        all_moons.extend(full_moons)
        all_moons.sort()

        for order_time in all_moons:
            # buy on new moon, sell on full moon
            for sym, ticker in self.tickers.items():
                if pd.to_datetime(order_time) in ticker.prices.index:
                    curr_price = ticker.prices.loc[pd.to_datetime(order_time)]['Close'] # assume we buy/sell on close

                    if order_time in new_moons:
                        # use max half of our balance to buy this stock
                        num_to_buy = math.floor((self.balance / 2) / curr_price)
                        
                        self.buy(sym, num_to_buy, curr_price, order_time)
                    elif order_time in full_moons:
                        # sell half the shares we own of this stock
                        num_to_sell = self.portfolio[sym] // 2

                        self.buy(sym, num_to_sell, curr_price, order_time)
