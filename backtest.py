import unittest

from ticker import Ticker


class Backtest(unittest.TestCase):

    @unittest.skip # uncomment this to skip
    def testJasonTrader(self):
        from jasontrader import JasonTrader
        tickers = Ticker.get_tickers(
            ['GE', 'AMD', 'TSLA', 'BA'], interval='1d', period='2y')

        jasontrader = JasonTrader(tickers, 10000, eps=0.015, stop_loss=.7)
        jasontrader.run()

        jasontrader.print_ending_info()

    @unittest.skip  # uncomment this to skip 
    def testClaudeaTrader(self):
        from claudeatrader import ClaudeaTrader
        ticker_msft = Ticker('MSFT', '1d', '1y')

        claudeatrader = ClaudeaTrader([ticker_msft], 10000)
        claudeatrader.run()

        claudeatrader.print_ending_info()

    # @unittest.skip # uncomment this to skip
    def testJamesTrader(self):
        from jamesstreet import JamesTrader
        tickers = Ticker.get_tickers(
            ['GE', 'AMD', 'TSLA', 'BA'], interval='1d', period='2y')

        jamestrader = JamesTrader(tickers, 10000)
        jamestrader.run()

        jamestrader.print_ending_info()
        jamestrader.plot_trades()

if __name__ == '__main__':
    unittest.main()
