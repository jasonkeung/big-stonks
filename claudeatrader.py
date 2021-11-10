from datetime import datetime
import math
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")



from trader import Trader
from order import Order

class ClaudeaTrader(Trader):

    def run(self):
        """
        Runs asdasdasdasd

        :return: None
        """
        
        start_date = "2021-04-01"
        end_date = "2021-05-30"
        for sym, ticker in self.tickers.items():
            price = ticker.prices["Close"]
            for date in pd.date_range(start_date, end_date, freq = "1d"):
                if date in ticker.prices.index:
                    past_price = price.loc[:date]
                    curr_price = price[date]
                    mod = sm.tsa.statespace.SARIMAX(past_price,
                                    order=(1, 1, 1),
                                    seasonal_order=(1, 0, 1, 18),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False, disp=False)
                    results = mod.fit(disp = False)
                    pred = results.forecast(1).values[0]
                    # pred_ci = pred.conf_int()
                    if pred > curr_price and self.balance > curr_price:
                        # buy
                        num_to_buy = math.floor((self.balance) / curr_price)

                        self.orders.append(Order(sym, 'B', num_to_buy, curr_price, date))
                        self.balance -= num_to_buy * curr_price
                        self.portfolio[sym] += num_to_buy
                    if pred < price[date] and self.portfolio[sym] > 0:
                        # sell
                        num_to_sell = self.portfolio[sym]

                        self.orders.append(Order(sym, 'S', num_to_sell, curr_price, date)) 
                        self.balance += num_to_sell * curr_price
                        self.portfolio[sym] -= num_to_sell

        return None