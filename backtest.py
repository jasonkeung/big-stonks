import unittest

from ticker import Ticker


class Backtest(unittest.TestCase):
    
    # @unittest.skip # uncomment this to skip
    def testJasonTrader(self):
        from jasontrader import JasonTrader
        tickers = Ticker.get_tickers(['MSFT'], interval='1d', period='3y')

        # best_e = -1
        # best_alpha = -100
        # for i in range(10):
        #     e = (i + 1) * .01
        #     jasontrader = JasonTrader(tickers, 10000, eps=e, stop_loss=1)
        #     jasontrader.run()

        #     temp_alpha = jasontrader.get_alpha()
        #     if temp_alpha > best_alpha:
        #         best_alpha = temp_alpha
        #         best_e = e

        jasontrader = JasonTrader(tickers, 10000, eps=.06, stop_loss=1)
        jasontrader.run()

        jasontrader.print_ending_info()

    @unittest.skip # uncomment this to skip
    def testClaudeaTrader(self):
        from claudeatrader import ClaudeaTrader
        ticker_msft = Ticker('MSFT', '1d', '1y')

        claudeatrader = ClaudeaTrader([ticker_msft], 10000)
        claudeatrader.run()

        claudeatrader.print_ending_info()
        
if __name__ == '__main__':
    unittest.main()

