import jqdatasdk as jqd
from jqdatasdk import *
import json
from os import path
import os,sys

root = os.getcwd()

file = open(root + '/JQData/Conf.txt', "r")
Conf = json.load(file)
# auth(Conf['username'], Conf['password'])


# jqd.get_price("000001.XSHE", start_date="2017-01-01", end_date="2017-12-31")

#查询当日剩余可调用数据条数
count=get_query_count()
print(count)

df = get_all_securities(['etf'])
print(df)

df[df.display_name == '中小板']


# https://www.joinquant.com/default/index/sdk