from datetime import datetime

from moontrader import MoonTrader
from moontrader import MoonTrader
from ticker import Ticker

class Backtest:

    def testMoonTrader():
        ticker_goog = Ticker('GE', '1d', 'ytd')
        ticker_amd = Ticker('AMD', '1d', 'ytd')

        moontrader = MoonTrader([ticker_goog, ticker_amd], 10000)
        moontrader.run()

        moontrader.print_ending_info()
    
    def testJasonTrader():
        ticker_goog = Ticker('GE', '1d', 'ytd')
        ticker_amd = Ticker('AMD', '1d', 'ytd')

        jasontrader = JasonTrader([ticker_goog, ticker_amd], 10000)
        jasontrader.run()

        jasontrader.print_ending_info()
        

Backtest.testMoonTrader()
Backtest.testJasonTrader()
