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

    # @unittest.skip  # uncomment this to skip
    def testClaudeaTrader(self):
        from claudeatrader import ClaudeaTrader
        tickers = Ticker.get_tickers(
            ['MSFT', 'BA', 'AMD', 'TSLA'], interval='1d', period='10mo')

        claudeatrader = ClaudeaTrader(tickers, 10000, training_days = 180)
        claudeatrader.run()

        claudeatrader.print_ending_info()
        claudeatrader.plot_trades()

    @unittest.skip # uncomment this to skip
    def testJamesTrader(self):
        from jamesstreet import JamesTrader
        tickers = Ticker.get_tickers(
            ['GE', 'AMD', 'TSLA', 'BA'], interval='1d', period='2y')

        jamestrader = JamesTrader(tickers, 10000)
        jamestrader.run()

        jamestrader.print_ending_info()
        jamestrader.plot_trades()

    @unittest.skip  # uncomment this to skip
    def testKartikiTrader(self):
        from kartikitrader import KartikiTrader
        tickers = Ticker.get_tickers(
            ['JNJ', 'PG', 'SPY', 'DX-Y.NYB'], interval='1d', period='2y')

        ktrader = KartikiTrader(tickers, 10000)
        ktrader.run()

        ktrader.print_ending_info()
        ktrader.plot_trades()

if __name__ == '__main__':
    unittest.main()
