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
        :param eps: (Optional) decimal interval at which to capture profits, 0.001 means selling more every .1% profit
        :param stop_loss: (Optional) decimal fraction of starting_bal for max loss, .3 means max loss of 30%
        """
        super().__init__(tickers_list, starting_bal)
        self.eps = eps
        self.bal_saved = self.balance * (1 - stop_loss)
        # set aside money so we only use self.balance * stop_loss to trade
        self.balance -= self.bal_saved

        # map from sym to (map from buyprice to quantity)
        self.init_buy_points = {sym: {} for sym in self.tickers.keys()}
        self.curr_buy_points = {sym: {} for sym in self.tickers.keys()}

    def run(self):
        """
        Runs trades for each day and ticker over the time range of self.tickers

        :return: None
        """
        # Get the prices index from a random ticker in self.tickers
        date_index = self.tickers[list(self.tickers.keys())[0]].prices.index

        # Add moving average columns to each ticker prices DataFrame
        for sym, ticker in self.tickers.items():
            ticker.prices["mva30"] = ticker.get_mva(30)
            ticker.prices["mva180"] = ticker.get_mva(180)

        # Make a trade for each ticker for each date in chron. order
        for date in date_index:
            for sym, ticker in self.tickers.items():
                self.trade(sym, ticker, date)

        # Add back bal_saved that was set aside
        self.balance += self.bal_saved

    def trade(self, sym, ticker, date):
        """
        Makes a single trade call given a symbol, Ticker object, and date.
        Looks at past/current buy positions and sells them for a profit at each self.eps interval

        :param sym: String ticker symbol to trade
        :param ticker: Ticker object to trade
        :param date: datetime object to trade at

        :return: None
        """
        init_buys = self.init_buy_points[sym]
        curr_buys = self.curr_buy_points[sym]
        curr_price = ticker.prices["Close"][date]

        num_to_buy = 0
        num_to_sell = 0

        mva30_today = ticker.prices["mva30"][date]
        mva180_today = ticker.prices["mva180"][date]
        mva30_yest = ticker.prices.loc[ticker.prices.index < date]["mva30"]
        mva180_yest = ticker.prices.loc[ticker.prices.index < date]["mva180"]

        if not mva180_yest.any():
            return 
        mva30_yest = mva30_yest.iloc[-1]
        mva180_yest = mva180_yest.iloc[-1]

        # if fastline rises over slowline today
        if mva30_today > mva180_today and mva30_yest <= mva180_yest:
            bal_to_spend = self.balance / len(self.tickers) / 2

            # Only buy if the amount to spend is significant
            if bal_to_spend > (self.starting_bal - self.bal_saved) * .05:
                num_to_buy +=  bal_to_spend / curr_price

        # if fastline drops below slowline today
        elif mva30_today < mva180_today and mva30_yest >= mva180_yest:
            # Absolutely set num_to_sell as the holdings
            num_to_sell = self.portfolio[sym]
            
        # compare buys and sells to make the net order
        num_change = num_to_buy - num_to_sell
        if num_change > 0:
            self.buy(sym, num_change, curr_price, date)
            self.init_buy_points[sym][curr_price] = num_to_buy
            self.curr_buy_points[sym][curr_price] = num_to_buy
        elif num_change < 0:
            self.sell(sym, -num_change, curr_price, date)
