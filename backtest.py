from algorithm import Algorithm
from naivealg import NaiveAlgorithm
from tickerhistory import TickerHistory


from naivealg import NaiveAlgorithm

class Backtest:

    def test1():
        """
        :return: profit
        """
        prices = TickerHistory('GOOG', '1d', '30d')
        alg = NaiveAlgorithm(prices, 10000)
        orders = alg.run()
        profit = Algorithm.get_profit(orders)
        return profit

print(Backtest.test1())