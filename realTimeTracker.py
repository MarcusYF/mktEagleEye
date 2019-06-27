import requests, time, datetime, os, xlwt, xlrd, random, pandas as pd
import itertools
from bs4 import BeautifulSoup

import os,sys

class East(object):
    def __init__(self, code):
        self.code = code
        self.Url = 'http://hq.sinajs.cn/list='
        self.data = {"code": self.code, "name": "", "date":"", "open_price": -1, "close_price":-1, "max_price":-1, "min_price":1e9, "gain":"", "price":-1, "volume":-1, "share":-1, "time":""}
        self.price = []
        self.volume = []
        self.share = []
        self.time = []
        self.Date = time.strftime('%Y%m%d')
        self.root = sys.path[0]
        self.Record = self.root + '/RealTimeData_' + str(code) + '.xls'
        print(self.Record)
        if os.path.exists(self.Record):
            print('Record exist...')
        else:
            print('execute path:', sys.path[0])
            print('Track data ...')

            now = datetime.datetime.now()
            stop = datetime.datetime(2019, 6, 27, 15, 1, 00, 0)
            while not now.__gt__(stop):
                self.get_data()
                now = datetime.datetime.now()
            # self.write_excel()

    def genUrl(self):
        return self.Url + 'sh' + str(self.code)

    def write_excel(self):

        pda = pd.DataFrame(self.Data)

        writer = pd.ExcelWriter(self.Record)

        pda.to_excel(writer, sheet_name='Data', startcol=0, index=False, header=None)
        writer.save()

    # 爬虫获取数据
    def get_data(self):

        time.sleep(5)
        orihtml = requests.get(self.genUrl(), timeout=30)
        soup = BeautifulSoup(orihtml.text, 'lxml').getText()
        data = soup.split("\"")[1].split(',')
        self.data["name"] = data[0]
        self.data["open_price"] = float(data[1])
        self.data["close_price"] = float(data[2])
        curTime = data[31]
        if not self.time or curTime != self.time[-1]:
            self.data["date"] = data[30]

            self.data["max_price"] = max(self.data["max_price"], float(data[4]))
            self.data["min_price"] = min(self.data["min_price"], float(data[5]))
            self.data["time"] = data[31]
            self.time.append(self.data["time"])
            self.data["price"] = float(data[3])
            self.data["gain"] = '{:.2f}%'.format((self.data["price"] - self.data["close_price"]) / self.data["close_price"] * 100)
            self.price.append(self.data["price"])
            self.data["share"] = int(float(data[8]) / 100)
            self.share.append(self.data["share"])
            self.data["volume"] = int(float(data[9]) / 10000)
            self.volume.append(self.data["volume"])

        print("标的：{name}, 当前价：{price}, 涨幅：{gain}, 成交额：{volume}".format(**self.data))



def main():
    # East(162411) ## 华宝油气
    # East(512880) ## 证券etf
    East(600519)  ## 贵州茅台
    # East("000001") ## 上证指数


if __name__ == '__main__':
    main()

