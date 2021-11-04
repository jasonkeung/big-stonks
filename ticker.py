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
    
    def get_mva(self, window_len=5):
        ave = self.prices[['Close']].rolling(window=window_len).mean()
        self.prices['Moving Average'] = ave['Close']

        return ave['Close']
        
