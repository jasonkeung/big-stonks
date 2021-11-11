import math

from trader import Trader

class JasonTrader(Trader):
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
        Runs JasonTrader over the time range of self.tickers

        :return: None
        """
        date_index = self.tickers[list(self.tickers.keys())[0]].prices.index # gets the prices index from a random ticker in self.tickers
        bal_saved = self.balance * .8
        self.balance -= bal_saved # set aside 80% of starting_bal as a stop loss

        buy_points = {} # map from sym to (map from buyprice to quantity)

        eps = .005 # epsilon for alg, hyperparameter to be tuned

        for date in date_index:
            for sym, ticker in self.tickers.items():
                ticker_buys = buy_points[sym]
                curr_price = ticker.prices["Close"][date]
                # TODO: if no positions, buy using half of balance

                for buy_price, quantity in ticker_buys:
                    price_diff_percent = (curr_price - buy_price) / buy_price
                    if price_diff_percent > eps:
                        num_to_sell = quantity / (2 ** math.floor(price_diff_percent / eps))
                    elif price_diff_percent < -eps:
                        num_to_buy = 0

        
        self.balance += bal_saved # add back bal_saved that was set aside
        return None
