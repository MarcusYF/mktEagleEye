import requests, time, datetime, os, xlwt, xlrd, random, pandas as pd
import itertools
from bs4 import BeautifulSoup
import threading
import os,sys

class myThread(threading.Thread):
    def __init__(self, threadID, name, code):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.code = code

    def run(self):
        print("Starting " + self.name)
        East(self.code)
        print("Exiting " + self.name)

class East(object):
    def __init__(self, code):
        self.code = code
        self.Url = 'http://hq.sinajs.cn/list='
        self.data = {"code": self.code, "name": "", "date":"", "open_price": -1, "close_price":-1, "max_price":-1, "min_price":1e9, "price_gain":"", "volume_gain":0, "price":-1, "volume":-1, "share":-1, "time":""}
        self.price = [0]
        self.volume = [0]
        self.share = [0]
        self.time = [0]
        self.Date = time.strftime('%Y%m%d')
        self.root = sys.path[0]

        print('execute path:', sys.path[0])
        print('Start tracking realtime data ...')

        now = datetime.datetime.now()
        start = datetime.datetime(2019, 6, 28, 8, 59, 0, 0)
        stop = datetime.datetime(2019, 6, 28, 15, 1, 0, 0)

        self.Record = self.root \
                      + '/RealTimeData_' \
                      + str(code) + '_' \
                      + self.Date + '_' \
                      + str(now.hour) + '_' \
                      + str(now.minute) + '_' \
                      + str(now.second) + '-' \
                      + str(stop.hour) + '_' \
                      + str(stop.minute) + '_' \
                      + str(stop.second) \
                      + '.txt'
        record_dumper = open(self.Record, 'w')
        while now.__gt__(start) and now.__lt__(stop):
            soup = self.get_data()
            if soup:
                record_dumper.write(soup)
            now = datetime.datetime.now()

        record_dumper.close()

    def genUrl(self):
        return self.Url + 'sh' + str(self.code)

    def write_excel(self):

        pda = pd.DataFrame(self.Data)

        writer = pd.ExcelWriter(self.Record)

        pda.to_excel(writer, sheet_name='Data', startcol=0, index=False, header=None)
        writer.save()

    # 爬虫获取数据
    def get_data(self):

        time.sleep(1)

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
            self.data["price_gain"] = '{:.2f}%'.format((self.data["price"] - self.data["close_price"]) / self.data["close_price"] * 100)
            self.price.append(self.data["price"])
            self.data["share"] = int(float(data[8]) / 100)
            self.share.append(self.data["share"])
            self.data["volume"] = int(float(data[9]) / 10000)
            self.volume.append(self.data["volume"])
            self.data["volume_gain"] = self.volume[-1] - self.volume[-2]
            print("标的：{name}, 时间：{time}, 当前价：{price}, 涨幅：{price_gain}, 成交额：{volume}, 成交额增量：{volume_gain}".format(**self.data))
            return soup

        else:
            return None


def main():
    # East(162411) ## 华宝油气
    # East(512880) ## 证券etf
    # East(600519)  ## 贵州茅台
    # East("000001") ## 上证指数

    code_map = {'上证50': 510050,
                '沪深300': 510310,
                '中证500': 510500,
                '创业板': 159915,
                '证券': 512880,
                '券商': 512000,
                '医药': 512010,
                '环保': 512580,
                '消费': 159928,
                '军工': 512660,
                '银行': 512800,
                '信息': 159939,
                '传媒': 512980,
                '有色': 512400,
                '房地产': 512200,
                '工业': 512310,
                '能源': 159945}

    thread_pool = []
    i = 1
    for k in code_map.keys():
        thread_pool.append(myThread(i, k, code_map.get(k)))
        i += 1
    [thread.start() for thread in thread_pool]

    # 创建新线程
    # thread1 = myThread(1, "证券ETF", 512880)
    # thread2 = myThread(2, "贵州茅台", 600519)
    # thread1.start()
    # thread2.start()


if __name__ == '__main__':
    main()
