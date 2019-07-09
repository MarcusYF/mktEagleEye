
class tradeManager(object):

    def __init__(self, cash):
        self.cash = cash
        self.share = 0
        self.stock_value = 0
        self.avg_price = 0

    def buy(self, price, share):
        cash_in = price * share
        self.share += share
        self.stock_value += cash_in
        self.cash -= cash_in
        self.avg_price = self.stock_value / self.share

    def sell(self, price, share):
        cash_out = price * share
        self.share -= share
        self.stock_value -= cash_out
        self.cash += cash_out
        self.avg_price = self.stock_value / self.share


def main():
    t = tradeManager(100000)


if __name__ == '__main__':
    main()