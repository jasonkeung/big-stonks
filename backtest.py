from moontrader import MoonTrader
from moontrader import MoonTrader
from ticker import Ticker

class Backtest:

    def testMoonAlg():
        """
        :return: profit of MoonTrader
        """
        ticker_goog = Ticker('GOOG', '1d', 'ytd')
        ticker_ge = Ticker('GE', '1d', 'ytd')
        ticker_amc = Ticker('AMC', '1d', 'ytd')
        ticker_tsla = Ticker('TSLA', '1d', 'ytd')
        moontrader = MoonTrader({'GOOG': ticker_goog, 'GE': ticker_ge, 'AMC': ticker_amc, 'TSLA': ticker_tsla}, 10000)
        
        moontrader.run()

        print(f'Balance: {moontrader.balance}')
        print(f'Orders Made: {moontrader.orders}')
        print(f'Alpha: {moontrader.get_alpha()}')
        

Backtest.testMoonAlg()
