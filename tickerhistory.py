import yfinance as yf

class TickerHistory:

    def __init__(self, symbol, interval, period):
        self.data = yf.Ticker(ticker = symbol)
        self.prices = self.data.history(interval = interval, period = period)
        print('done downloading!')
    def get_ma(self, moving_ave_range = 5):
        # TODO: implement
        ave = self.prices[['Close']].rolling(window = moving_ave_range).mean()
        self.prices['Moving Average'] = ave['Close']
        print("get MA")
        
