import yfinance as yf

class TickerHistory:

    def __init__(self, symbol, interval, period):
        self.data = yf.Ticker(ticker = symbol)
        self.prices = self.data.history(interval=interval, period=period)

    
    def get_mva(self, window_len=5):
        ave = self.prices[['Close']].rolling(window=window_len).mean()
        self.prices['Moving Average'] = ave['Close']

        return ave['Close']
        
