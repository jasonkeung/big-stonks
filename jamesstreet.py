from datetime import datetime
import math
import pandas as pd
import yfinance as yf
import numpy as np


from trader import Trader
from order import Order

class JamesTrader(Trader):
    """
    Trader with balance, portfolio, tickers to trade, and orders made.

    Attributes:
        tickers: Map of symbol: Tickers for the trader to use (all Tickers need to have same period/interval)
        starting_bal: Starting dollar balance for the trader to use
        balance: Current balance of the trader
        portfolio: Map of tickers and quantity held Ex: {'GOOG': 2, 'TSLA': 3}
        orders: List of all Orders made Ex: [Order('GOOG', 'B', 2, 53.21, datetime(2021, 08, 02)), Order('GOOG', 'S', 2, 64.53, datetime(2021, 10, 21))]
    """

    def run(self):
        
        # add slow and fast moving averages lines and signals for the intersections of these lines
        for sym, ticker in self.tickers.items():
            ticker.prices["fastline"] = ticker.get_mva(50)
            ticker.prices["slowline"] = ticker.get_mva(200)
            ticker.prices.loc[:, 'signal'] = np.where(ticker.prices['slowline'] > ticker.prices['fastline'], 1, -1)
            ticker.prices["cross"] = ticker.prices["signal"].diff() 
            
        # identify if intersection is golden cross and death cross
        for dateindex in self.tickers[list(self.tickers.keys())[0]].prices.index:
            for sym, ticker in self.tickers.items():
                curr_price = ticker.prices["Close"][dateindex]
                if ticker.prices['cross'][dateindex] == 2:  
                    # buy
                    amt = self.balance/curr_price
                    if amt != 0.0:
                        self.buy(sym, amt, curr_price, dateindex)
                elif ticker.prices['cross'][dateindex] == -2:
                    # sell
                    amt = self.portfolio[sym]/curr_price
                    if amt != 0.0:
                        self.sell(sym, amt, curr_price, dateindex)
                    


                        