from algorithm import Algorithm
from moonalg import MoonAlgorithm
from naivealg import NaiveAlgorithm
from tickerhistory import TickerHistory


from naivealg import NaiveAlgorithm

class Backtest:

    def test1():
        """
        :return: profit
        """
        history = TickerHistory('GOOG', '1d', 'ytd')
        alg = MoonAlgorithm(history, 10000)
        orders = alg.run()
        print('GOOGLE ORDERS')
        print(orders)
        profit = Algorithm.get_profit(orders)
        print(f'GOOGLE PROFIT: {profit}')

        history = TickerHistory('GE', '1d', 'ytd')
        alg = MoonAlgorithm(history, 10000)
        orders = alg.run()
        print('GE ORDERS')
        print(orders)
        profit = Algorithm.get_profit(orders)
        print(f'GE PROFIT: {profit}')

        history = TickerHistory('SPY', '1d', 'ytd')
        alg = MoonAlgorithm(history, 10000)
        orders = alg.run()
        print('S&P 500 ORDERS')
        print(orders)
        profit = Algorithm.get_profit(orders)
        print(f'S&P 500 PROFIT: {profit}')
        

Backtest.test1()
