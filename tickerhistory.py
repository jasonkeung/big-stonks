import yfinance as yf

class TickerHistory:

    def __init__(self, symbol, interval, range):
        self.prices = yf.download(tickers=symbol,
                                  period=range,
                                  interval=interval)
    
    def get_mva(self, range):
        # TODO: implement
        print('asd')