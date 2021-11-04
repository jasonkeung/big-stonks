from datetime import datetime

from moontrader import MoonTrader
from moontrader import MoonTrader
from ticker import Ticker

class Backtest:

    def testMoonTrader():
        ticker_goog = Ticker('TSLA', '1d', 'ytd')
        ticker_amd = Ticker('TGT', '1d', 'ytd')

        moontrader = MoonTrader([ticker_goog, ticker_amd], 10000)
        moontrader.run()

        moontrader.print_ending_info()
        

Backtest.testMoonTrader()
