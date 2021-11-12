import yfinance as yf

class Ticker:
    """
    Ticker with price history, interval, period, and symbol

    Attributes:
        data: All stock data relevant to this stock (see https://pypi.org/project/yfinance/)
        prices: Pandas dataframe of price history (index: Date, columns: Open, High, Low, Close, Volume, Dividends, Stock Splits)
        symbol: symbol of ticker Ex: TSLA, GOOG, GE
        interval: interval of prices Ex: 1d, 15m, 1h
        period: range of prices Ex: ytd, 1mo, 1d
    """
    def __init__(self, symbol, interval, period):
        self.data = yf.Ticker(ticker=symbol)
        self.prices = self.data.history(interval=interval, period=period)
        self.symbol = symbol
        self.interval = interval
        self.period = period
    
    def get_mva(self, window_len):
        """
        Adds and returns a column to self.prices representing the moving average taken over window_len
        
        :param window_len: Window length over which to create the moving average

        :return: Column representing the window_len-moving average
        """
        ave = self.prices[['Close']].rolling(window=window_len).mean()
        self.prices[f'{window_len} Moving Average'] = ave['Close']

        return ave['Close']
        
    def get_tickers(symbols, interval, period):
        """
        Creates multiple Ticker objects over the given interval and period.
        Convenience function likely to be used in backtest.py

        :param symbols: List of string symbols to create Tickers for
        :param interval: interval for Tickers created
        :param period: period for Tickers created

        :return: List of Ticker objects
        """
        return [Ticker(sym, interval, period) for sym in symbols]
