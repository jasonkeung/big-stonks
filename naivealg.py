class NaiveAlgorithm(Algorithm):

    def run(self):
        """
        :return: list of buy/sell orders
        Ex: ('B', 2, '43.1'), ('B', 1, 45.21), ('S', 2, 51.54)]

        """
        for row in self.prices:
            print(row)
        
        return []