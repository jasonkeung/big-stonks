from datetime import datetime

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
    def __init__(self, tickers_list, starting_bal):
        """
        Create a new Trader.

        :param tickers_list: list of Tickers over the same interval/period to provide to the Trader
        :param starting_bal: dollar amount for the Trader to trade with
        """
        self.tickers = {t.symbol : t for t in tickers_list}
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
        
        trader_return = (((self.balance + portfolio_val) / self.starting_bal) - 1) * 100

        sp500_return = self.get_sp500_return()

        return trader_return - sp500_return

    def get_sp500_return(self):
        """
        Calulates the return of SPY S&P 500 over the period of self.tickers

        :return: percentage return of SPY S&P 500
        """
        arbitrary_ticker = self.tickers[list(self.tickers.keys())[0]] # get a random ticker from self.tickers to get its interval/period
        sp500 = Ticker('SPY', arbitrary_ticker.interval, arbitrary_ticker.period)
        sp500_return = (sp500.prices.iloc[-1]['Close'] / sp500.prices.iloc[0]['Close']) - 1 # percentage return of entire range of SPY/S&P 500
        return sp500_return * 100

    def get_ticker_hold_return(self, ticker):
        """
        Calculates the return of buying at start and holding for the entire period of ticker
        
        :param ticker: Ticker for which to buy and hold for entire period
        :return: percentage return of buying and holding
        """
        ticker_hold_return = (ticker.prices.iloc[-1]['Close'] / ticker.prices.iloc[0]['Close']) - 1 # percentage return of entire range of SPY/S&P 500
        return ticker_hold_return * 100

    def get_profit(self):
        """
        :return: total dollar profit from selling (does not include starting balance)
        """
        profit = 0

        for order in self.orders:
            order_type = order['order_type']
            quantity = order['quantity']
            price = order['price']

            if order_type == 'B':
                profit -= quantity * price
            elif order_type == 'S':
                profit += quantity * price
            else:
                raise Exception(f'Invalid order type: {order}')
            
        return profit
    
    def get_portfolio_val(self, time):
        """
        Returns the total value of self.portfolio at time
        If time is not in the ticker prices dataframe (like if time is a weekend), uses the last known price

        :param time: datetime date at which to evaluate the portfolio at

        :return: total value of self.portfolio at time
        """
        portfolio_val = 0
        for symbol, quantity in self.portfolio.items():
            ticker = self.tickers[symbol]
            last_price = ticker.prices.loc[ticker.prices.index <= time]['Close'].iloc[-1]
            portfolio_val += quantity * last_price
        
        return round(portfolio_val, 3)

    def print_ending_info(self):
        """
        Prints relevant information for after a Trader has run.
        """
        print(f'{type(self).__name__} Results:')
        print('Orders Made: ')
        for order in self.orders:
            print('\t' + str(order))
        print(f'Starting Balance: ${self.starting_bal}')
        print(f'Ending Balance: ${round(self.balance, 3)}')
        print(f'Ending Portfolio: {self.portfolio} -- ${self.get_portfolio_val(datetime.now())}')
        print(f'Ending Net Asset Value: ${round(self.balance, 3) + self.get_portfolio_val(datetime.now())}')
        print(f'Net Asset Percentage Gain: {Trader.calc_percent_change_str(self.starting_bal, self.balance + self.get_portfolio_val(datetime.now()))}')
        print(f'S&P 500 performance: {round(self.get_sp500_return(), 3)}%')
        print(f'Alpha: {round(self.get_alpha(), 3)}%')
        print('Baseline hold performances:')
        for sym, ticker in self.tickers.items():
            print(f'\t{sym}: {round(self.get_ticker_hold_return(ticker), 3)}%')
        print('------------------------------------------------')
    
    def calc_percent_change_str(start, end):
        return str(round(((end / start) - 1) * 100, 3)) + '%'
    

