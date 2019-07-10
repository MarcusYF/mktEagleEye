import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class strategy(object):

    def __init__(self, conf):
        self.code = conf['code']
        t = pd.read_excel('/Users/yaofan29597/Desktop/project/mktEagleEye/HistoryData_'+str(self.code)+'.xls')
        self.v = t['收盘价'].values[::-1]
        self.cash = conf['总资金']
        self.pivot_v = conf['建仓价格']
        self.base = conf['底仓']
        self.v_metric = conf['网格波动梯度']
        self.cash_metric = conf['交易资金梯度']
        self.net_level = conf['网格级数']

        self.pre_position = 0
        self.cur_position = 0
        self.strategy_info = {}.fromkeys(list(range(-self.net_level,1+self.net_level, 1)), [0, 0, 0])

        if self.cash_metric > 0:
            k = self.cash_metric + 1
            unit_cash = (self.cash - self.base) / (k * (k**self.net_level-1) / (k-1) + (k**(-self.net_level) - 1) / (1-k))
        else:
            unit_cash = (self.cash - self.base) / 2 / self.net_level

        for i in range(-self.net_level, self.net_level+1):
            if i != 0:
                v = self.pivot_v * (1 + self.v_metric) ** -i
                s = int(unit_cash * (1 + self.cash_metric) ** i / v)
                self.strategy_info[i] = [v, s, v*s]


        print("总资金:{:.2f}, 建仓价格:{:.2f}, 底仓:{}, 网格波动梯度:{:.2%}, 交易资金梯度:{:.2%}, 网格级数:{}" \
              .format(self.cash, self.pivot_v, self.base, self.v_metric, self.cash_metric, self.net_level))

        print("网格策略明细:")
        for i in range(-self.net_level, self.net_level+1):
            print(i, self.strategy_info[i][0], self.strategy_info[i][1], self.strategy_info[i][2])


class tradeManager(object):

    def __init__(self, strategy):

        self.strategy = strategy

        self.cash = self.strategy.cash
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

    def run_simulation(self):
        for p in v:

    def print_summary(self, current_value):
        stock_value = self.share * current_value
        print("总资产:{:.2f}, 可用资金:{:.2f}, 市值:{:.2f}, 持仓:{:.2f}, 成本:{:.3f}, 现价:{:.3f}, 盈亏:{:.2%}" \
              .format(self.cash + stock_value, self.cash, \
                stock_value, self.share, self.avg_price, current_value, (-self.avg_price+current_value) / self.avg_price))


def main():

    conf = {"code":512880, "总资金":100000, "建仓价格":0.90, "底仓":20000, "网格波动梯度":0.03, "交易资金梯度":0.0, "网格级数":10}

    s1 = strategy(conf)
    tradeManager(100000)

    # t = pd.read_excel("HistoryData_512880.xls")
    # v = t['收盘价'].values[::-1]
    # r = []
    # plt.plot(a)
    # for i in range(len(v)-1):
    #     r.append((v[i]-v[i+1]))
    #
    # plt.hist(r, np.linspace(-0.2, 0.2, 51, endpoint=True), histtype='bar', rwidth=0.8)
    #
    # a = np.random.normal(size=100) / 50
    # a.cumsum()
    # c.append(np.exp(sum(np.log(1+np.random.normal(size=100)/50))))
    #
    # plt.hist(c, np.linspace(-0.5, 1.5, 100, endpoint=True), histtype='bar', rwidth=0.8)
    #
    # t = tradeManager(100000)
    # t.buy(1, 10000)
    # t.print_summary(1)
    # t.buy(0.9, 11000)
    # t.print_summary(0.9)
    # t.buy(0.8, 12500)
    # t.print_summary(0.8)
    # t.buy(0.7, 14000)
    # t.print_summary(0.7)
    # t.sell(0.8, 14000)
    # t.print_summary(0.8)
    # t.buy(0.7, 14000)
    # t.sell(0.8, 14000)
    # t.buy(0.7, 14000)
    # t.sell(0.8, 14000)
    # t.buy(0.7, 14000)
    # t.sell(0.8, 14000)
    # t.buy(0.7, 14000)
    # t.sell(0.8, 14000)
    # t.buy(0.7, 14000)
    # t.sell(0.8, 14000)
    # t.buy(0.7, 14000)
    # t.sell(0.8, 14000)
    # t.buy(0.7, 14000)
    # t.sell(0.8, 14000)
    # t.buy(0.7, 14000)
    # t.sell(0.8, 14000)
    # t.buy(0.7, 14000)
    # t.sell(0.8, 14000)
    # t.buy(0.7, 14000)
    # t.sell(0.8, 14000)
    # t.buy(0.7, 14000)
    # t.sell(0.8, 14000)
    # t.print_summary(0.77)


if __name__ == '__main__':
    main()