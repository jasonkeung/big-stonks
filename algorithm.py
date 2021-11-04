class Algorithm:

    def __init__(self, ticker_history, budget):
        self.history = ticker_history
        self.balance = budget
        self.num_holding = 0
        

    def get_profit(orders):
        """
        :param start_bal: starting balance
        :param orders: list of buy/sell orders
        Ex: [('B', 2, 43.1), ('B', 1, 45.21), ('S', 2, 51.54)]

        :return: total dollar profit from selling (does not include starting balance)
        """
        profit = 0

        for order in orders:
            order_type = order[0]
            quantity = order[1]
            price = order[2]

            if order_type == 'B':
                profit -= quantity * price
            elif order_type == 'S':
                profit += quantity * price
            else:
                raise Exception(f'Invalid order type: {order}')
            
        return profit
    

