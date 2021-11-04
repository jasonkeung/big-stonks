from yfinance import ticker
from ticker import Ticker


class Trader:
    """
    Trader with balance, portfolio, tickers to trade, algorithm to use, and orders made.

    Attributes:
        tickers: List of tickers for the trader to use
        starting_bal: Starting dollar balance for the trader to use
        balance: Current balance of the trader
        portfolio: Map of tickers and quantity held Ex: {'GOOG': 2, 'TSLA': 3}
        orders: List of all Orders made Ex: [Order('B', 2, 53.21), Order('S', 2, 64.53)]
    """
    def __init__(self, tickers, starting_bal, alg):
        
        self.tickers = tickers
        self.starting_bal = starting_bal
        self.balance = starting_bal
        self.portfolio = {tick: 0 for tick in self.tickers}
        self.orders = []

    def get_profit(orders):
        """
        :param orders: list of buy/sell orders
        Ex: [{'order_type': B', 'num_shares': 2, 'price': 43.1}, {'order_type': B', 'num_shares': 1, 'price': 45.86}, {'order_type': B', 'num_shares': 2, 'price': 51.25}]

        :return: total dollar profit from selling (does not include starting balance)
        """
        profit = 0

        for order in orders:
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
    

