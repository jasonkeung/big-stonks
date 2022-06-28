from datetime import datetime
import math
import warnings
import statsmodels.api as sm
from itertools import product

from trader import Trader
from order import Order

class ClaudeaTrader(Trader):
    """
    Trader with balance, portfolio, tickers to trade, and orders made.

    Attributes:
        tickers: Map of symbol: Tickers for the trader to use (all Tickers need to have same period/interval)
        starting_bal: Starting dollar balance for the trader to use
        balance: Current balance of the trader
        portfolio: Map of tickers and quantity held Ex: {'GOOG': 2, 'TSLA': 3}
        orders: List of all Orders made Ex: [Order('GOOG', 'B', 2, 53.21, datetime(2021, 08, 02)), Order('GOOG', 'S', 2, 64.53, datetime(2021, 10, 21))]
    """
    warnings.filterwarnings("ignore")

    def __init__(self, tickers_list, starting_bal, training_days = 180):
        """
        Call's Trader's init and sets custom parameters.
        """
        super().__init__(tickers_list, starting_bal)
        date_index = self.tickers[list(self.tickers.keys())[0]].prices.index
        if len(date_index) > training_days:
            self.training_date = date_index[0:training_days]
            self.trading_date = date_index[training_days:len(date_index)]
            self.models = {sym: self.train_model(self.training_date, sym, ticker) for sym, ticker in self.tickers.items()} # the model for each sym

        else:
            raise Exception(f'the number of training days is too big for the period of time given.')
        # profit change before taking action
        self.alpha = 0.05
        # number of stocks being traded
        self.n = len(self.tickers.keys())

    
    def run(self):
        """
        Runs trader per day for each stocks

        :return: None
        """
        # record history of stocks bought
        buy_history = {sym: 0 for sym in self.tickers.keys()}

        # proportion of balance per stock
        balance_prop_sym = {sym: 1 / self.n for sym in self.tickers.keys()} 

        for date in self.trading_date:
            # update balance proportion if necessary
            if not all(value == 0 for value in buy_history.values()):
                balance_prop_sym = self.adjust_balance(balance_prop_sym, buy_history, date)

            for sym, ticker in self.tickers.items():
                # make prediction for each stock
                price = ticker.prices["Close"]
                past_price = price.loc[:date]
                curr_price = price[date]
                mod = sm.tsa.statespace.SARIMAX(past_price,
                                order=self.models[sym]["pdq"],
                                seasonal_order=self.models[sym]["PDQS"],
                                enforce_stationarity=False,
                                enforce_invertibility=False, disp=False)
                results = mod.fit(disp = False)
                pred = sum(results.forecast(5)) / 5

                # if prediction is higher and we have enough balance, then buy
                if pred > curr_price and balance_prop_sym[sym]*self.balance > curr_price:
                    num_to_buy = math.floor(balance_prop_sym[sym]*self.balance / curr_price)
                    self.buy(sym, num_to_buy, curr_price, date)
                    buy_history[sym] += curr_price*num_to_buy

                # sell if prediction is lower and we are not at lost
                elif pred < curr_price and self.portfolio[sym] > 0 and buy_history[sym] / self.portfolio[sym] < curr_price:
                    num_to_sell = self.portfolio[sym]
                    self.sell(sym, num_to_sell, curr_price, date)
                    buy_history[sym] = 0
                
                # sell if we gain alpha
                # elif self.portfolio[sym] > 1 and (buy_history[sym] / self.portfolio[sym])*(1+self.alpha) < curr_price:
                #     num_to_sell = self.portfolio[sym] // 2
                #     self.sell(sym, num_to_sell, curr_price, date)
                #     buy_history[sym] = 0
        return None

    # give larger percentage for those who give higher profit
    def adjust_balance(self, balance_prop_sym, buy_history, date):
        for sym, ticker in self.tickers.items():
            current_value = ticker.prices["Close"][date]*self.portfolio[sym]
            if buy_history[sym]*(1.1) < current_value:
                balance_prop_sym[sym] = min(0.1 + balance_prop_sym[sym], 1)
            elif buy_history[sym]*(.9) > current_value:
                balance_prop_sym[sym] = max(balance_prop_sym[sym] - 0.1, 0)
        return balance_prop_sym

    def train_model(self, date, sym, ticker):
        # default parameters
        best_pdq, best_PDQS = (1, 1, 1), (1, 0, 1, 18)

        # better to tune with larger parameter choices but will take too long to run
        # p = q = range(10)
        # d = D = P = Q = range(3)
        # S = [0, 12, 13, 14, 15, 16, 17, 18]

        # # uncomment to tune in model rather than using default parameters
        # training_price =  ticker.prices.loc[date, "Close"]
        # p = q = range(2)
        # d = D = P = Q = range(2)
        # S = [0, 5, 12, 18]

        # pdq = list(product(p, d, q))
        # PDQS = list(product(P,D,Q,S))
        # min_ic = float("inf")
        # best_pdq, best_PDQS = None, None
        # for comb in pdq:
        #     for COMBS in PDQS:
        #         try:
        #             model = sm.tsa.statespace.SARIMAX(training_price, order=comb,
        #             seasonal_order=COMBS,
        #             enforce_stationarity=False,
        #             enforce_invertibility=False, disp=False)
        #             res = model.fit(disp = False)
        #             ic = res.aic + res.bic + res.aicc
        #             if ic < min_ic:
        #                 best_pdq, best_PDQS = comb, COMBS
        #         except:
        #             continue
        # print(sym, " ARIMA:", best_pdq, best_PDQS)

        return {"pdq": best_pdq, "PDQS": best_PDQS}
