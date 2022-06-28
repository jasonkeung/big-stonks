from datetime import datetime
import math
import pandas as pd
import yfinance as yf
#import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")



from trader import Trader
from order import Order

def hft_scalping_algo(self, buy_thresh, sell_thresh):
    start_date = "2020-11-11"
    end_date = "2021-11-11"

    # past_percs = []

    for sym, ticker in self.tickers.items():
        price = ticker.prices["Close"]
        past_price = price[0]

        for date in pd.date_range(start_date, end_date, freq = "1d"):
            if date in ticker.prices.index:
                curr_price = price[date]
                
                perc_change = (curr_price - past_price) / past_price
                    
                trade_multiplier = 1
                
                if perc_change < buy_thresh: #buy
                    if perc_change < (buy_thresh * 2):
                        trade_multiplier = 2
                    if self.balance >= (trade_multiplier * curr_price):
                        self.buy(sym, trade_multiplier, curr_price, date)
                elif perc_change > sell_thresh: #sell
                    if perc_change > (sell_thresh * 2):
                        trade_multiplier = 2
                    if self.portfolio[sym] >= trade_multiplier:
                        self.sell(sym, trade_multiplier, curr_price, date)
                else:
                    continue

                past_price = curr_price
        return None

def trend_trader_algo(self, trend_avg_intervals, buy_thresh, sell_thresh):
    start_date = "2020-11-11"
    end_date = "2021-11-11"

    for sym, ticker in self.tickers.items():
        price = ticker.prices["Close"]
        past_price = price[0]

        past_percs = []

        for date in pd.date_range(start_date, end_date, freq = "1d"):
            if date in ticker.prices.index:
                curr_price = price[date]

                # Determining metric to compare later with threshold
                perc_change = (curr_price - past_price) / past_price
                past_percs.append(perc_change)
                if len(past_percs) >= trend_avg_intervals:
                    perc_change_mean = sum(past_percs[:-trend_avg_intervals]) / trend_avg_intervals
                else:
                    perc_change_mean = sum(past_percs) / len(past_percs)

                # Deciding ideal number of shares to be bought/sold (if any)
                buy = False
                sell = False
                trade_multiplier = 1
            
                if perc_change_mean < buy_thresh:
                    trade_multiplier = math.floor((perc_change_mean / buy_thresh) * 10)
                    buy = True
                elif perc_change_mean > sell_thresh:
                    trade_multiplier = math.floor(perc_change_mean / sell_thresh)
                    sell = True
                else:
                    continue

                # Buying/selling as many of ideal number of shares as possible
                if buy == True:
                    list_range = list(range(1, trade_multiplier + 1))
                    if list_range != None:
                        list_range.reverse()
                        for try_multiplier in list_range:
                            print(self.balance, try_multiplier * curr_price)
                            if self.balance >= (try_multiplier * curr_price):
                                self.buy(sym, try_multiplier, curr_price, date)
                                buy = False
                                break

                elif sell == True:
                    list_range = list(range(1, trade_multiplier + 1))
                                    
                    if list_range != None:
                        list_range.reverse()               
                        for try_multiplier in list_range:
                            #print(self.portfolio[sym])
                            if self.portfolio[sym] >= try_multiplier:
                                self.sell(sym, try_multiplier, curr_price, date)
                                sell = False
                                break
                    
                past_price = curr_price
        return None


def trader_mva(self, num_past_days, buy_thresh, sell_thresh):
    #given list of prices + days, let user set how many days before current day
    #they wanna keep track of for moving average
    #on current day we want the price to be some proportion greater than the mva of
    #past days. if its greater than we sell, else buy
    start_date = "2020-11-11"
    end_date = "2021-11-11"
    past_prices = []

    for sym, ticker in self.tickers.items():
        price = ticker.prices["Close"]
        
        for date in pd.date_range(start_date, end_date, freq = "1d"):
            if date in ticker.prices.index:
                curr_price = price[date]
                if len(past_prices) >= num_past_days:
                    mva = sum(past_prices[:-num_past_days]) / num_past_days
                    ratio = curr_price / mva
                    trade_mult = 1

                    #buy if curr price is less than mva
                    if ratio < buy_thresh:
                        trade_mult = ratio * 5
                        if self.balance >= trade_mult * curr_price:
                            self.buy(sym, trade_mult, curr_price, date)
                    #sell if curr price greater than mva
                    elif ratio > sell_thresh:
                        print(mva, num_past_days)
                        #trade_mult = math.ceil(ratio)
                        if self.portfolio[sym] >= trade_mult: #have at least one stock
                            self.sell(sym, trade_mult, curr_price, date)
                    else:
                        continue

                past_prices.append(curr_price)

    return None

class HenTayTrader(Trader):
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
        # hft_scalping_algo(self, buy_thresh = -0.001, sell_thresh = 0.05)
        '''
        trend_trader_algo(self, 
                          trend_avg_intervals = 3, 
                          buy_thresh = 0.1, 
                          sell_thresh = 0.1)
        '''
        trader_mva(self, 
                    num_past_days = 3, 
                    buy_thresh = 0.8, 
                    sell_thresh = 1.2)
        return None
   
       