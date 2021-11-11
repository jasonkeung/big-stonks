import unittest

from ticker import Ticker
import warnings


class Backtest(unittest.TestCase):
    
    # @unittest.skip # uncomment this to skip
    def testJasonTrader(self):
        from jasontrader import JasonTrader
        ticker_ge = Ticker('GE', '15m', '1w')
        ticker_amd = Ticker('AMD', '15m', '1w')

        jasontrader = JasonTrader([ticker_ge], 10000)
        jasontrader.run()

        jasontrader.print_ending_info()

    # @unittest.skip # uncomment this to skip
    def testClaudeaTrader(self):
        from claudeatrader import ClaudeaTrader
        ticker_msft = Ticker('MSFT', '1d', '1y')

        claudeatrader = ClaudeaTrader([ticker_msft], 10000)
        claudeatrader.run()

        claudeatrader.print_ending_info()
        
if __name__ == '__main__':
    unittest.main()

