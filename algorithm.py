class Algorithm:

    def __init__(self, ticker_history, budget):
        self.prices = ticker_history
        self.balance = budget
        return None

    def get_profit(orders):
        """
        :param orders: list of buy/sell orders
        Ex: ('B', 2, '43.1'), ('B', 1, 45.21), ('S', 2, 51.54)]

        :return: total profit
        """
        res = 0

        for order in orders:
            order_type = order[0]
            quantity = order[1]
            price = order[2]

            if order_type == 'B':
                res -= quantity * price
            elif order_type == 'S':
                res += quantity * price
            else:
                raise Exception(f'Invalid order type: {order}')
            
        return res
