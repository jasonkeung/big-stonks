#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

import yfinance as yf
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

from sklearn.neural_network import MLPRegressor

# In[2]:

from trader import Trader

class KartikiTrader(Trader):



    """
    Trader with balance, portfolio, tickers to trade, and orders made.
    Attributes:
        tickers: Map of symbol: Tickers for the trader to use (all Tickers need to have same period/interval)
        starting_bal: Starting dollar balance for the trader to use
        balance: Current balance of the trader
        portfolio: Map of tickers and quantity held Ex: {'GOOG': 2, 'TSLA': 3}
        orders: List of all Orders made Ex: [Order('GOOG', 'B', 2, 53.21, datetime(2021, 08, 02)), Order('GOOG', 'S', 2, 64.53, datetime(2021, 10, 21))]
    """
    # Will work with stocks in the consumer products domain

    # Will use historical returns of Johnson & Johnson & its rival (Proctor & Gamble)

    # Will also use the US Dollar index and the SPDR S&P 500 ETF & run a neural network on these features



    def run(self):
        #Buy (based on NN prediction and moving average)
        def buy_nn(date, curr_Y, pred_Y, pred_prevY, mva20, mva100):
            if (self.balance >= pred_Y) and (pred_prevY < pred_Y) and (mva20 > mva100):
                self.buy('JNJ', 1 , curr_Y, date)
            return None

        #Sell (based on NN prediction and moving average)
        def sell_nn(date, curr_Y, pred_Y, pred_prevY, mva20, mva100):
            if (pred_prevY > pred_Y) and (mva20 < mva100):
                self.sell('JNJ', 1 , curr_Y, date)
            return None

        # Fetch data from yfinance
        # 3-year daily data for J&J, P&G, SPY, USD index

        end1 = datetime.date(2021, 11, 15)
        start1 = end1 - pd.Timedelta(days = 365 * 3)


        jj_df = yf.download('JNJ', start = start1, end = end1, progress = False)
        pg_df = yf.download('PG', start = start1, end = end1, progress = False)
        spy_df = yf.download('SPY', start = start1, end = end1, progress = False)
        usdx_df = yf.download('DX-Y.NYB', start = start1, end = end1, progress = False)

        # Log returns based on closing price (return per day?)
        jj_df['jj'] = np.log(jj_df['Adj Close'] / jj_df['Adj Close'].shift(1))
        pg_df['pg'] = np.log(pg_df['Adj Close'] / pg_df['Adj Close'].shift(1))
        spy_df['spy'] = np.log(spy_df['Adj Close'] / spy_df['Adj Close'].shift(1))
        usdx_df['usdx'] = np.log(usdx_df['Adj Close'] / usdx_df['Adj Close'].shift(1))

        # Create a dataframe with X's (spy, pg, usdx) and Y (jj)
        df = pd.concat([spy_df['spy'], jj_df['jj'],
                pg_df['pg'], usdx_df['usdx']], axis = 1).dropna()


        # Neural network steps
        pred_model = MLPRegressor(hidden_layer_sizes = 10, activation = 'identity', solver = 'lbfgs', random_state = 1)
        X = df[['pg', 'spy', 'usdx']]
        y = df['jj']
        pred_model.fit(X, y)
        date_index = self.tickers[list(self.tickers.keys())[0]].prices.index


        for date in date_index:

            curr_price_x = []
            prev_price_x = []
            curr_Y = 0


            limit = datetime.datetime.now() - relativedelta(years=2)
            if date < limit:
                pass
            else:

                for sym, ticker in self.tickers.items():
                    if sym == 'JNJ':
                        curr_Y = ticker.prices['Close'][date]

                        ticker.prices['mva20'] = ticker.get_mva(20)
                        ticker.prices['mva100'] = ticker.get_mva(100)
                        mva20 = ticker.prices['mva20'][date]
                        mva100 = ticker.prices['mva100'][date]

                    else:
                        curr_price = ticker.prices['Close'][date]
                        idx = ticker.prices.index.get_loc(date)
                        prev_price = ticker.prices['Close'].iloc[[idx - 1]][0]
                        curr_price_x.append(curr_price)
                        prev_price_x.append(prev_price)


                pred_Y = pred_model.predict([curr_price_x])[0]
                pred_prevY = pred_model.predict([prev_price_x])[0]
                buy_nn(date, curr_Y, pred_Y, pred_prevY, mva20, mva100)
                sell_nn(date, curr_Y, pred_Y, pred_prevY, mva20, mva100)


        return None










# In[ ]:
