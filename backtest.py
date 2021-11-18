import unittest

from moontrader import MoonTrader
from claudeatrader import ClaudeaTrader
from jasontrader import JasonTrader
from hentaytrader import HenTayTrader
from ticker import Ticker

class Backtest(unittest.TestCase):
    '''
    def testJasonTrader(self):
        ticker_ge = Ticker('GE', '1d', 'ytd')
        ticker_amd = Ticker('AMD', '1d', 'ytd')

        jasontrader = JasonTrader([ticker_ge, ticker_amd], 10000)
        jasontrader.run()

        jasontrader.print_ending_info()
    
    def testClaudeaTrader(self):
        ticker_msft = Ticker('MSFT', '1d', '1y')

        claudeatrader = ClaudeaTrader([ticker_msft], 10000)
        claudeatrader.run()

        claudeatrader.print_ending_info()
    '''
    def testHenTayTrader(self):
        ticker_goog = Ticker('GOOG', '1d', '1y')
        ticker_tsla = Ticker('TSLA', '1d', '1y')

        # hentaytrader = HenTayTrader([ticker_goog], 10000)
        hentaytrader = HenTayTrader([ticker_tsla], 10000)
        hentaytrader.run()
        hentaytrader.print_ending_info()
        
if __name__ == '__main__':
    unittest.main()

