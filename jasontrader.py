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

    def __init__(self, tickers_list, starting_bal, eps=0.001, stop_loss=.3):
        """
        Call's Trader's init and sets custom parameters.

        :param tickers_list: list of Tickers over the same interval/period to provide to the Trader
        :param starting_bal: dollar amount for the Trader to trade with
        :param eps: (Optional) parameter for the minimum percent gain for the Trader to sell
        :param stop_loss: (Optional) the maximum fraction of starting_bal the Trader will lose, i.e. JasonTrader will lose, at max, stop_loss of starting_bal
        """
        super().__init__(tickers_list, starting_bal)
        self.eps = eps
        self.bal_saved = self.balance * (1 - stop_loss)
        self.balance -= self.bal_saved # set aside money so we only use self.balance * stop_loss to trade

        # map from sym to (map from buyprice to quantity)
        self.init_buy_points = {sym: {} for sym in self.tickers.keys()}
        self.curr_buy_points = {sym: {} for sym in self.tickers.keys()}


    def run(self):
        """
        Runs JasonTrader over the time range of self.tickers

        :return: None
        """
        date_index = self.tickers[list(self.tickers.keys())[0]].prices.index # gets the prices index from a random ticker in self.tickers

        for date in date_index:
            for sym, ticker in self.tickers.items():
                self.trade(sym, ticker, date)

        self.balance += self.bal_saved # add back bal_saved that was set aside
    
    def trade(self, sym, ticker, date):
        init_buys = self.init_buy_points[sym]
        curr_buys = self.curr_buy_points[sym]

        curr_price = ticker.prices["Close"][date]
        
        # if no positions, buy using self.balance / len(self.tickers) / 2
        if not self.portfolio[sym]:
            to_spend = self.balance / len(self.tickers) / 2
            num_to_buy = to_spend / curr_price
            self.buy(sym, num_to_buy, curr_price, date)
            init_buys[curr_price] = num_to_buy
            curr_buys[curr_price] = num_to_buy
        else:
            num_to_buy = 0
            num_to_sell = 0

            for buy_price, curr_quantity in curr_buys.items():
                init_quantity = init_buys[buy_price]
                price_change = (curr_price - buy_price) / buy_price
                if price_change > self.eps:
                    # sell a fraction of initial buy quantity, min 1/64 or the rest of it
                    fraction_to_sell = init_quantity / (2 ** (math.floor(price_change / self.eps)))
                    num_to_sell += min(curr_quantity, max(fraction_to_sell, init_quantity / 64))
                    self.curr_buy_points[sym][buy_price] -= num_to_sell
            
            
            # buy if 30 mva > 180 mva
            


            # compare buys and sells to make the net order
            num_change = num_to_buy - num_to_sell
            if num_change > 0:
                self.buy(sym, num_change, curr_price, date)
                self.init_buy_points[sym][curr_price] = num_change
                self.curr_buy_points[sym][curr_price] = num_change
            elif num_change < 0:
                self.sell(sym, -num_change, curr_price, date)