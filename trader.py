from ticker import Ticker


class Trader:
    """
    Trader with balance, portfolio, tickers to trade, and orders made.

    Attributes:
        tickers: Map of symbol: Tickers for the trader to use (all Tickers need to have same period/interval)
        starting_bal: Starting dollar balance for the trader to use
        balance: Current balance of the trader
        portfolio: Map of tickers and quantity held Ex: {'GOOG': 2, 'TSLA': 3}
        orders: List of all Orders made Ex: [Order('GOOG', 'B', 2, 53.21, datetime(2021, 08, 02)), Order('GOOG', 'S', 2, 64.53, datetime(2021, 10, 21))]
    """
    def __init__(self, tickers, starting_bal):
        self.tickers = tickers
        self.starting_bal = starting_bal
        self.balance = starting_bal
        self.portfolio = {sym: 0 for sym in self.tickers.keys()}
        self.orders = []

    def get_alpha(self):
        """
        Alpha = actual return - expected return. Ex: +30% - +10% = +20%
        If the trader made a 30% gain and sp500 grew 10% over the same period, our alpha is 20%

        :return: alpha percentage
        """
        portfolio_val = 0
        for symbol, quantity in self.portfolio.items():
            ticker = self.tickers[symbol]
            last_price = ticker.prices.iloc[-1]['Close']
            portfolio_val += quantity * last_price
        
        trader_return = ((self.balance + portfolio_val) / self.starting_bal) - 100

        arbitrary_ticker = self.tickers[list(self.tickers.keys())[0]] # get a random ticker from self.tickers to get its interval/period
        sp500 = Ticker('SPY', arbitrary_ticker.interval, arbitrary_ticker.period)
        sp500_return = (sp500.prices.iloc[-1]['Close'] / sp500.prices.iloc[0]['Close']) - 100 # percentage return of entire range of SPY/S&P 500

        return trader_return - sp500_return



    def get_profit(self):
        """
        :return: total dollar profit from selling (does not include starting balance)
        """
        profit = 0

        for order in self.orders:
            order_type = order[0]
            quantity = order[1]
            price = order[2]

            if order_type == 'B':
                profit -= quantity * price
            elif order_type == 'S':
                profit += quantity * price
            else:
                raise Exception(f'Invalid order type: {order}')
            
        return profit
    

