class Algorithm:

    def __init__(self, ticker_history, budget):
        self.history = ticker_history
        self.balance = budget
        self.num_holding = 0


    def get_profit(orders):
        """
        :param start_bal: starting balance
        :param orders: list of buy/sell orders
        Ex: [{'order_type': B', 'num_shares': 2, 'price': 43.1}, {'order_type': B', 'num_shares': 1, 'price': 45.86}, {'order_type': B', 'num_shares': 2, 'price': 51.25}]

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
    

