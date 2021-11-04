from algorithm import Algorithm

class NaiveAlgorithm(Algorithm):

    def run(self):
        """
        :return: list of buy/sell orders
        Ex: [{'order_type': 'B', 'num_shares': 2, 'price': 43.1}, {'order_type': B', 'num_shares': 1, 'price': 45.86}, {'order_type': B', 'num_shares': 2, 'price': 51.25}]

        """
        
        return [{'order_type': 'B', 'num_shares': 2, 'price': 43.1}, {'order_type': 'B', 'num_shares': 1, 'price': 45.86}, {'order_type': 'B', 'num_shares': 2, 'price': 51.25}]