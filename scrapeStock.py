import requests, time, os, xlwt, xlrd, random, pandas as pd
import itertools
from bs4 import BeautifulSoup

import os,sys

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
            time.sleep(random.randint(0, 0) + random.random())  # 随机延时?.?s  以防封IP
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


def main():
    # East(162411) ## 华宝油气
    East(512880) ## 证券etf
    # East("000001") ## 上证指数


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

