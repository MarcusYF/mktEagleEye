import pandas as pd

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

    def print_summary(self, current_value):
        stock_value = self.share * current_value
        print("总资产:{:.2f}, 可用资金:{:.2f}, 市值:{:.2f}, 持仓:{:.2f}, 成本:{:.3f}, 现价:{:.3f}, 盈亏:{:.2%}" \
              .format(self.cash + stock_value, self.cash, \
                stock_value, self.share, self.avg_price, current_value, (-self.avg_price+current_value) / self.avg_price))


def main():
    t = pd.read_excel("HistoryData_510050.xls")
    t['收盘价'].values


    t = tradeManager(100000)
    t.buy(1, 10000)
    t.print_summary(1)
    t.buy(0.9, 11000)
    t.print_summary(0.9)
    t.buy(0.8, 12500)
    t.print_summary(0.8)
    t.buy(0.7, 14000)
    t.print_summary(0.7)
    t.sell(0.8, 14000)
    t.print_summary(0.8)
    t.buy(0.7, 14000)
    t.sell(0.8, 14000)
    t.buy(0.7, 14000)
    t.sell(0.8, 14000)
    t.buy(0.7, 14000)
    t.sell(0.8, 14000)
    t.buy(0.7, 14000)
    t.sell(0.8, 14000)
    t.buy(0.7, 14000)
    t.sell(0.8, 14000)
    t.buy(0.7, 14000)
    t.sell(0.8, 14000)
    t.buy(0.7, 14000)
    t.sell(0.8, 14000)
    t.buy(0.7, 14000)
    t.sell(0.8, 14000)
    t.buy(0.7, 14000)
    t.sell(0.8, 14000)
    t.buy(0.7, 14000)
    t.sell(0.8, 14000)
    t.buy(0.7, 14000)
    t.sell(0.8, 14000)
    t.print_summary(0.77)


if __name__ == '__main__':
    main()