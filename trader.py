import math
from datetime import datetime
import pytz

from ticker import Ticker
from order import Order


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
        self.tickers = {t.symbol: t for t in tickers_list}
        self.starting_bal = starting_bal
        self.balance = starting_bal
        self.portfolio = {sym: 0 for sym in self.tickers.keys()}
        self.orders = []

    def buy(self, sym, num_to_buy, curr_price, date):
        """
        Wraps needed actions for placing a buy order.
        Appends a new Order to self.orders
        Subtracts from self.balance accordingly
        Adds to self.portfolio accordingly

        :param sym: symbol of ticker to buy
        :param num_to_buy: number of shares to buy
        :param curr_price: price of ticker to buy at
        :param date: datetime at which to buy at

        :return: None
        """
        assert not math.isclose(
            num_to_buy, 0), f'Cannot buy shares too close to zero: {num_to_buy} shares'
        assert num_to_buy > 0, f'Cannot buy negative shares {num_to_buy} < 0'
        to_spend = num_to_buy * curr_price
        assert to_spend <= self.balance or math.isclose(
            self.balance - to_spend, 0, abs_tol=1e-7), f'Insufficient balance to buy {num_to_buy} {sym} shares @ ${round(curr_price, 3)} with balance ${round(self.balance, 3)}, costs ${round(num_to_buy * curr_price, 3)}'

        self.orders.append(Order(sym, 'B', num_to_buy, curr_price, date))
        self.balance -= to_spend
        self.portfolio[sym] += num_to_buy

    def sell(self, sym, num_to_sell, curr_price, date):
        """
        Wraps needed actions for placing a sell order.
        Appends a new Order to self.orders
        Adds from self.balance accordingly
        Removes to self.portfolio accordingly

        :param sym: symbol of ticker to sell
        :param num_to_sell: number of shares to sell
        :param curr_price: price of ticker to sell at
        :param date: datetime at which to sell at

        :return: None
        """
        assert not math.isclose(
            num_to_sell, 0), f'Cannot sell shares too close to zero: {num_to_sell} shares'
        assert num_to_sell > 0, f'Cannot sell negative shares {num_to_sell} < 0'
        assert num_to_sell <= self.portfolio[
            sym], f'Cannot sell {num_to_sell} shares with only {self.portfolio[sym]} in portfolio'

        self.orders.append(Order(sym, 'S', num_to_sell, curr_price, date))
        self.balance += num_to_sell * curr_price
        self.portfolio[sym] -= num_to_sell

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

        trader_return = (((self.balance + portfolio_val) /
                         self.starting_bal) - 1) * 100

        sp500_return = self.get_sp500_return()

        return trader_return - sp500_return

    def get_sp500_return(self):
        """
        Calulates the return of SPY S&P 500 over the period of self.tickers

        :return: percentage return of SPY S&P 500
        """
        # Get a random ticker from self.tickers to get its interval/period
        arbitrary_ticker = self.tickers[list(self.tickers.keys())[0]]
        sp500 = Ticker('SPY', arbitrary_ticker.interval, arbitrary_ticker.period)

        # percentage return of entire range of SPY/S&P 500
        sp500_return = (sp500.prices.iloc[-1]['Close'] / sp500.prices.iloc[0]['Close']) - 1
        return sp500_return * 100

    def get_ticker_hold_return(self, ticker):
        """
        Calculates the return of buying at start and holding for the entire period of ticker

        :param ticker: Ticker for which to buy and hold for entire period
        :return: percentage return of buying and holding
        """
        # Percentage return of entire range of SPY/S&P 500
        ticker_hold_return = (ticker.prices.iloc[-1]['Close'] / ticker.prices.iloc[0]['Close']) - 1  
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

            if hasattr(ticker.prices.index.dtype, 'tz'):
                time = time.astimezone(pytz.timezone("US/Eastern"))

            last_price = ticker.prices.loc[ticker.prices.index <= time]['Close'].iloc[-1]
            portfolio_val += quantity * last_price

        return round(portfolio_val, 3)

    def print_ending_info(self):
        """
        Prints relevant information for after a Trader has run.
        """
        print(f'\n{type(self).__name__} Results:')
        print('Orders Made: ')
        for order in self.orders:
            print('\t' + str(order))
        print(f'Starting Balance: ${self.starting_bal}')
        print(f'Ending Balance: ${round(self.balance, 3)}')
        print(
            f'Ending Portfolio: {self.portfolio} -- ${self.get_portfolio_val(datetime.now())}')
        print(
            f'Ending Net Asset Value: ${round(self.balance, 3) + self.get_portfolio_val(datetime.now())}')
        print(
            f'Net Asset Percentage Gain: {Trader.calc_percent_change_str(self.starting_bal, self.balance + self.get_portfolio_val(datetime.now()))}')
        print(f'S&P 500 performance: {round(self.get_sp500_return(), 3)}%')
        print(f'Alpha: {round(self.get_alpha(), 3)}%')
        print('Baseline hold performances:')
        for sym, ticker in self.tickers.items():
            print(f'\t{sym}: {round(self.get_ticker_hold_return(ticker), 3)}%')
        print('------------------------------------------------')

    def calc_percent_change_str(start, end):
        return str(round(((end / start) - 1) * 100, 3)) + '%'
