from datetime import datetime
import math
import pandas as pd
import yfinance as yf


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
        """
        https://github.com/alpacahq/example-scalping
        
        """
        
        start_date = "2021-04-01"
        end_date = "2021-05-30"
        for date in pd.date_range(start_date, end_date, freq = "1d"):
            for sym, ticker in self.tickers.items():
                curr_price = ticker.prices["Close"][date]
                

                        