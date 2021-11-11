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
        bal_saved = self.balance * .7
        self.balance -= bal_saved # set aside 80% of starting_bal as a stop loss

        # map from sym to (map from buyprice to quantity)
        init_buy_points = {sym: {} for sym in self.tickers.keys()}
        curr_buy_points = {sym: {} for sym in self.tickers.keys()}
        eps = .002 # epsilon for alg, hyperparameter to be tuned

        for date in date_index:
            for sym, ticker in self.tickers.items():
                init_ticker_buys = init_buy_points[sym]
                curr_ticker_buys = curr_buy_points[sym]

                curr_price = ticker.prices["Close"][date]
                
                # if no positions, buy using self.balance / len(self.tickers) / 2
                if not self.portfolio[sym]:
                    to_spend = self.balance / len(self.tickers) / 2
                    num_to_buy = to_spend / curr_price
                    self.buy(sym, num_to_buy, curr_price, date)
                    init_ticker_buys[curr_price] = num_to_buy
                    curr_ticker_buys[curr_price] = num_to_buy
                else:
                    num_to_buy = 0
                    num_to_sell = 0

                    for buy_price, curr_quantity in curr_ticker_buys.items():
                        init_quantity = init_ticker_buys[buy_price]
                        price_change = (curr_price - buy_price) / buy_price
                        if price_change > eps:
                            # sell a fraction of initial buy quantity, min 1/32 or the rest of it
                            fraction_to_sell = init_quantity / (2 ** (math.floor(price_change / eps)))
                            num_to_sell += min(curr_quantity, max(fraction_to_sell, init_quantity / 32))
                            curr_buy_points[sym][buy_price] -= num_to_sell
                        elif price_change < -eps:
                            # buy using .1 of balance
                            num_to_buy += .1 * self.balance / curr_price
                    
                    num_change = num_to_buy - num_to_sell
                    if num_change > 0:
                        self.buy(sym, num_change, curr_price, date)
                        init_buy_points[sym][curr_price] = num_to_buy
                        curr_buy_points[sym][curr_price] = num_to_buy
                    elif num_change < 0:
                        self.sell(sym, -num_change, curr_price, date)

        self.balance += bal_saved # add back bal_saved that was set aside
