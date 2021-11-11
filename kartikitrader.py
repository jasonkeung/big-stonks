#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

import yfinance as yf
import datetime
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression


# In[2]:


from trader import Trader

class KartikiTrader(Trader):
    
    
    #major edits needed: adjusting function to work with current classes
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

# Will also use the US Dollar index and the SPDR S&P 500 ETF 




    def run(self):
        # Fetch data from yfinance
        # 3-year daily data for J&J, P&G, SPY, USD index
        
        end1 = datetime.date(2021, 11, 1)
        start1 = end1 - pd.Timedelta(days = 365 * 3)
        
        
        jj_df = yf.download("JNJ", start = start1, end = end1, progress = False)
        pg_df = yf.download("PG", start = start1, end = end1, progress = False)
        spy_df = yf.download("SPY", start = start1, end = end1, progress = False)
        usdx_df = yf.download("DX-Y.NYB", start = start1, end = end1, progress = False)

        # Log returns based on closing price (return per day?)
        jj_df['jj'] = np.log(jj_df['Adj Close'] / jj_df['Adj Close'].shift(1))
        pg_df['pg'] = np.log(pg_df['Adj Close'] / pg_df['Adj Close'].shift(1))
        spy_df['spy'] = np.log(spy_df['Adj Close'] / spy_df['Adj Close'].shift(1))
        usdx_df['usdx'] = np.log(usdx_df['Adj Close'] / usdx_df['Adj Close'].shift(1))
        
        # Create a dataframe with X's (spy, pg, usdx) and Y (jj)
        df = pd.concat([spy_df['spy'], jj_df['jj'], 
                pg_df['pg'], usdx_df['usdx']], axis = 1).dropna()
        
        # Multiple linear regression steps
        mlr_skl_model = LinearRegression()
        X = df[['pg', 'spy', 'usdx']]
        y = df['jj']
        mlr_skl_model.fit(X, y)
        
        #edit line below
        pred_Y = mlr_skl_model.predict(X)
        
        #finish
        return None 


# In[ ]:




