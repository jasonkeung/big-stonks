from datetime import datetime
from algorithm import Algorithm

class MoonAlgorithm(Algorithm):

    def run(self):
        """
        :return: list of buy/sell orders
        Ex: [{'order_type': B', 'num_shares': 2, 'price': 43.1}, {'order_type': B', 'num_shares': 1, 'price': 45.86}, {'order_type': B', 'num_shares': 2, 'price': 51.25}]

        """
        res_orders = []
        new_moons = ['01-12', '02-11', '03-13', '04-11', '05-11', '06-10', '07-09', '08-08', '09-06', '10-06', '11-04', '12-03']
        full_moons = ['01-28', '02-27', '03-28', '04-26', '05-26', '06-24', '07-23', '08-22', '09-20', '10-20', '11-19', '12-28']

        # convert new and full moons to datetime objects
        for i in range(len(new_moons)):
            new_moons[i] = datetime.strptime('2021-' + new_moons[i], '%Y-%m-%d')

        for i in range(len(full_moons)):
            full_moons[i] = datetime.strptime('2021-' + full_moons[i], '%Y-%m-%d')

        # buy on new moon, sell on full moon
        for index, row in self.history.prices.iterrows():
            curr_price = row['Close'] # assume we buy/sell on close

            if index in new_moons:
                # use max half of our balance to buy stocks
                num_to_buy = (self.balance / 2) / curr_price 

                res_orders.append(('B', num_to_buy, curr_price))
                self.balance -= num_to_buy * curr_price
                self.num_holding += num_to_buy
            elif index in full_moons:
                res_orders.append(('S', self.num_holding, curr_price)) # sell all shares we own
                self.balance += self.num_holding * curr_price
                self.num_holding -= self.num_holding
        return res_orders
