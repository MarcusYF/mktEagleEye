import requests, time, os, xlwt, xlrd, random, pandas as pd
import itertools
import threading
from bs4 import BeautifulSoup

import os,sys


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, code):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.code = code

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        East(self.code)
        print("Exiting " + self.name)



class East(object):
    def __init__(self, code):
        self.code = code
        self.Url = 'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/'
        self.yearSpan = list(range(2020, 2000, -1))
        self.jiduSpan = [4, 3, 2, 1]
        self.tableName = ""
        self.Data = []
        self.Date = time.strftime('%Y%m%d')
        self.root = sys.path[0]
        self.Record = self.root + '/HistoryData_' + str(code) + '.xls'
        print(self.Record)
        if os.path.exists(self.Record):
            print('Record exist...')
        else:
            print('execute path:', sys.path[0])
            print('Get data ...')
            self.get_data()
            self.write_excel()

    def genUrl(self, year, jidu):
        return self.Url + str(self.code) + '.phtml?year=' + str(year) + '&jidu=' + str(jidu)

    def write_excel(self):

        pda = pd.DataFrame(self.Data)

        writer = pd.ExcelWriter(self.Record)

        pda.to_excel(writer, sheet_name='Data', startcol=0, index=False, header=None)
        writer.save()


    # 爬虫获取数据
    def get_data(self):
        # 请求数据
        firstTouch = True
        for year, jidu in itertools.product(self.yearSpan, self.jiduSpan):
            print('Get data from ' + str(self.code) + ', ' + str(year) + ' ,' + str(jidu) + '...')
            orihtml = requests.get(self.genUrl(year, jidu), timeout=30)
            orihtml.encoding = 'gb2312'
            # 创建 beautifulsoup 对象
            soup = BeautifulSoup(orihtml.text, 'lxml')
            # 采集每一个股票的信息
            hasData = soup.find('table', id='FundHoldSharesTable')
            if hasData is not None:

                fundHoldSharesTable = soup.find('table', id='FundHoldSharesTable').find_all('tr')
                print('record cnt: ' + str(len(fundHoldSharesTable)))
                if firstTouch:
                    self.tableName = fundHoldSharesTable[0].get_text().split('<|>')[0].strip('\r|\n|\t')
                    tableSchema = fundHoldSharesTable[1].get_text().strip('\r|\n|\t').split('\n')
                    self.Data.append(tableSchema)
                    firstTouch = False

                for tableRecord in fundHoldSharesTable[2:]:

                    record = [div.get_text().strip('\r|\n|\t') for div in tableRecord.find_all('div')]
                    self.Data.append(record)
            else:
                if firstTouch:
                    continue
                else:
                    break

            time.sleep(random.randint(0, 5) + random.random())  # 随机延时?.?s  以防封IP

def main():
    # East(162411) ## 华宝油气
    # East(512880) ## 证券etf


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

    for code in code_map.values():
        East(code)

    # 中概互联 513050


    # 创建新线程
    # thread1 = myThread(1, "证券ETF", 512200)
    # thread2 = myThread(2, "华宝油气", 162411)
    # thread1.start()
    # thread2.start()


if __name__ == '__main__':
    main()
#
# realtimeUrl =  'https://www.cnblogs.com/seacryfly/articles/stock.html'
# Url = 'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/162411.phtml?year=1019&jidu=3'
# orihtml = requests.get(Url).text
# soup = BeautifulSoup(orihtml, 'lxml')
# soup
# with open('draft5.txt', 'w') as f:
#     f.write(a.get_text().encode('gb2312'))
#
# a.get_text()
# soup.find('div', class_='nav_menu').find_all('a', {'target': '_blank'})
#
# reg = "<a target='_blank's+href='http://biz.finance.sina.com.cn/stock/history_min.php?symbol=shd{6}&date=d{4}-d{2}-d{2}'>s*([^s]+)s+</a>s*</div></td>s*<td[^d]*([^<]*)</div></td>s+<td[^d]*([^<]*)</div></td>s+<td[^d]*([^<]*)</div></td>s+<td[^d]*([^<]*)</div></td>s+"
#
# <a target='_blank' href='http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=sz162411&date=2019-06-25'>
#
# a = [['a','b','v'],[1,2,3],[3,4,5]]
# pda = pd.DataFrame(a)
#
# writer = pd.ExcelWriter('/Users/yaofan29597/Desktop/project/mktEagleEye/test.xlsx')
#
# pda.to_excel(writer, sheet_name='Data1', startcol=0, index=False, header=None)
# writer.save()
#


import requests,json
url="https://dataapi.joinquant.com/apis"
#获取调用凭证
body={
    "method": "get_token",
    "mob": "17801050240",  #mob是申请JQData时所填写的手机号
    "pwd": "7q5s94rg",  #Password为聚宽官网登录密码，新申请用户默认为手机号后6位
}
response = requests.post(url, data = json.dumps(body))
token=response.text
#调用get_security_info获取单个标的信息
body={
    "method": "get_all_securities",
    "token": token,
    "code": "stock",
}
response = requests.post(url, data = json.dumps(body))
print(response.text[:1000])

len(response.text)
