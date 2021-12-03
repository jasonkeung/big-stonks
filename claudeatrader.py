from datetime import datetime
import math
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import warnings
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import pmdarima as pm
from pmdarima.pipeline import Pipeline
from pmdarima.preprocessing import BoxCoxEndogTransformer

# from pyramid.arima import auto_arima




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

        :param tickers_list: list of Tickers over the same interval/period to provide to the Trader
        :param starting_bal: dollar amount for the Trader to trade with
        :param eps: (Optional) decimal interval at which to capture profits, 0.001 means selling more every .1% profit
        :param stop_loss: (Optional) decimal fraction of starting_bal for max loss, .3 means max loss of 30%
        """
        super().__init__(tickers_list, starting_bal)
        date_index = self.tickers[list(self.tickers.keys())[0]].prices.index
        print(len(date_index))
        if len(date_index) > training_days:
            self.training_date = date_index[0:training_days]
            self.trading_date = date_index[training_days:len(date_index)]
            self.models = {sym: self.train_model(self.training_date, sym, ticker) for sym, ticker in self.tickers.items()} # the model for each sym

        else:
            raise Exception(f'the number of training days is too big for the period of time given.')
        
        # map from sym to (map from buyprice to quantity)
        self.buy_points = {sym: [] for sym in self.tickers.keys()}
        self.alpha = 0.01
    def run(self):
        """
        Runs asdasdasdasd

        :return: None
        """
        pass
        for date in self.trading_date:
            for sym, ticker in self.tickers.items():
                price = ticker.prices["Close"]
                past_price = price.loc[:date]
                curr_price = price[date]
                # mod = sm.tsa.statespace.SARIMAX(past_price,
                #                 order=(1, 1, 1),
                #                 seasonal_order=(1, 0, 1, 18),
                #                 enforce_stationarity=False,
                #                 enforce_invertibility=False, disp=False)
                results = self.models[sym].fit(past_price)
                pred = sum(results.predict(5))/5
                # pred_ci = pred.conf_int()
                if pred > curr_price and self.balance > curr_price:
                    # buy
                    num_to_buy = math.floor((self.balance) / curr_price)
                    self.buy(sym, num_to_buy, curr_price, date)
                    self.buy_points[sym].append(curr_price)

                elif pred < curr_price and max(self.buy_points[sym], default = 0) < curr_price and self.portfolio[sym] > 0:
                    # sell
                    num_to_sell = self.portfolio[sym]
                    self.sell(sym, num_to_buy, curr_price, date)
                    self.buy_points[sym] = []
                
                elif max(self.buy_points[sym], default = 0)*(1+self.alpha) < curr_price and self.portfolio[sym] > 0:
                    num_to_sell = self.portfolio[sym]
                    self.sell(sym, num_to_buy, curr_price, date)
                    self.buy_points[sym] = []

    def train_model(self, date, sym, ticker):
        training_price =  ticker.prices.loc[date, "Close"]
        model = pm.auto_arima(training_price, error_action='ignore', seasonal=True, max_p = 10, max_q = 10)
        return model

    # def train_model(self, date, sym, ticker):
    #     training_price =  ticker.prices.loc[date, "Close"]
    #     # train_size = int(len(X) * 0.66)
    #     # train, test = X[0:train_size], X[train_size:]
    #     # history = [x for x in train]
    #     # print(train, test, history)
    #     return self.evaluate_models(training_price, range(0, 1), range(0, 1), range(0, 1))
    #         # for p in range(0, 5):
    #         #     for q in range(0, 5):
    #         #         for d in range(0, 5):
    #         #             mod = sm.tsa.statespace.SARIMAX(past_price,
    #         #                     order=(p, d, q),
    #         #                     seasonal_order=(0, 0, 0, 0),
    #         #                     enforce_stationarity=False,
    #         #                     enforce_invertibility=False, disp=False)

    #         # model = pm.auto_arima(df.value, start_p=1, start_q=1,
    #         #           test='adf',       # use adftest to find optimal 'd'
    #         #           max_p=10, max_q=10, # maximum p and q
    #         #           m=1,              # frequency of series
    #         #           d=None,           # let model determine 'd'
    #         #           seasonal=False,   # No Seasonality
    #         #           start_P=0, 
    #         #           D=0, 
    #         #           trace=True,
    #         #           error_action='ignore',  
    #         #           suppress_warnings=True, 
    #         #           stepwise=True)

    # def evaluate_arima_model(self, X, arima_order):
    #     # prepare training dataset
    #     print("try:", arima_order)
    #     train_size = int(len(X) * 0.66)
    #     train, test = X[0:train_size], X[train_size:]
    #     history = [x for x in train]
    #     # make predictions
    #     predictions = list()
    #     for t in range(len(test)):
    #         print(t)
    #         model = sm.tsa.statespace.SARIMAX(history,
    #                             order=arima_order,
    #                             seasonal_order=(0,0,0,0),
    #                             enforce_stationarity=False,
    #                             enforce_invertibility=False, disp=False)
    #         print(model)
    #         model_fit = model.fit(disp = False)
    #         print(model_fit)
    #         yhat = model_fit.forecast(1).values[0]
    #         print(yhat)
    #         predictions.append(yhat)
    #         history.append(test[t])
    #     # calculate out of sample error
    #     rmse = math.sqrt(mean_squared_error(test, predictions))
    #     print("rmse", rmse)
    #     return rmse

    #     # evaluate combinations of p, d and q values for an ARIMA model
    # def evaluate_models(self, dataset, p_values, d_values, q_values):
    #     dataset = dataset.astype('float32')
    #     best_score, best_cfg = float("inf"), None
    #     for p in p_values:
    #         for d in d_values:
    #             for q in q_values:
    #                 order = (p,d,q)
    #                 try:
    #                     rmse = self.evaluate_arima_model(dataset, order)
    #                     if rmse < best_score:
    #                         best_score, best_cfg = rmse, order
    #                     print('ARIMA%s RMSE=%.3f' % (order,rmse))
    #                 except:
    #                     continue
    #     print('Best ARIMA%s RMSE=%.3f' % (best_cfg, best_score))
    #     return best_cfg
        return None