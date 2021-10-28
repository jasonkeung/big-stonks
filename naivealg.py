from algorithm import Algorithm

class NaiveAlgorithm(Algorithm):

    def run(self):
        """
        :return: list of buy/sell orders
        Ex: [('B', 2, '43.1'), ('B', 1, 45.21), ('S', 3, 51.54)]

        """
        print(self.history.prices)
        
        return [('B', 2, 43.1), ('B', 1, 45.21), ('S', 3, 51.54)]