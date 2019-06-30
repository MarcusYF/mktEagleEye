from jqdatasdk import *
import sys, os

root = os.getcwd()

file = open(root + '/JQData/Conf.txt', "r")
Conf = json.load(file)
auth(Conf['username'], Conf['password'])
get_price("000001.XSHE", start_date="2017-01-01", end_date="2017-12-31")