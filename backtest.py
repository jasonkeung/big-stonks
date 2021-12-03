import unittest

from ticker import Ticker
import warnings


class Backtest(unittest.TestCase):
    
    @unittest.skip # uncomment this to skip
    def testJasonTrader(self):
        from jasontrader import JasonTrader
        tickers = Ticker.get_tickers(['GE', 'AMD', 'F', 'MSFT'], interval='15m', period='1mo')

        jasontrader = JasonTrader(tickers, 10000, eps=0.015, stop_loss=.5)
        jasontrader.run()
        
        jasontrader.print_ending_info()

    # @unittest.skip # uncomment this to skip
    def testClaudeaTrader(self):
        from claudeatrader import ClaudeaTrader
        ticker_msft = Ticker('MSFT', '1d', period = '8mo')

        claudeatrader = ClaudeaTrader([ticker_msft], 10000, training_days = 30)
        claudeatrader.run()

        claudeatrader.print_ending_info()
        
if __name__ == '__main__':
    unittest.main()

