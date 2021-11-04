from datetime import datetime

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

        for i in range(len(full_moons)):
            full_moons[i] = datetime.strptime('2021-' + full_moons[i], '%Y-%m-%d')

        for sym, ticker in self.tickers.items():
            # buy on new moon, sell on full moon
            for order_time, order_price in ticker.prices.iterrows():
                curr_price = order_price['Close'] # assume we buy/sell on close

                if order_time in new_moons:
                    # use max half of our balance to buy this stock
                    num_to_buy = (self.balance / 2) / curr_price

                    self.orders.append(Order(sym, 'B', num_to_buy, curr_price, order_time))
                    self.balance -= num_to_buy * curr_price
                    self.portfolio[sym] += num_to_buy
                elif order_time in full_moons:
                    # sell all shares we own of this stock
                    num_to_sell = self.portfolio[sym]

                    self.orders.append(Order(sym, 'S', num_to_sell, curr_price, order_time)) 
                    self.balance += num_to_sell * curr_price
                    self.portfolio[sym] -= num_to_sell
