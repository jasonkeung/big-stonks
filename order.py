class Order:
    """
    Order with ticker symbol, order type, quantity, price, and order time.

    Attributes:
        ticker_symbol: symbol of ticker for the order
        order_type: 'B' or 'S' for buy/sell
        quantity: number of shares
        price: price at which the order was made
        order_time: datetime at which the order was made Ex: datetime(2021, 10, 21)
    """
    
    def __init__(self, ticker_symbol, order_type, quantity, price, order_time):
        self.ticker_symbol = ticker_symbol
        self.order_type = order_type
        self.quantity = quantity
        self.price = price
        self.order_time = order_time

    def __str__(self):
        if self.order_type == 'B':
            return f'{self.ticker_symbol}: bought {round(self.quantity, 3)} shares @ ${round(self.price, 3)} on {self.order_time}'
        elif self.order_type == 'S':
            return f'{self.ticker_symbol}: sold {round(self.quantity, 3)} shares @ ${round(self.price, 3)} on {self.order_time}'
