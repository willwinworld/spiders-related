#! python3
# -*- coding: utf-8 -*-
import time
import requests
import pandas as pd
import numpy as np
from pymongo import MongoClient
from pyquery import PyQuery as Pq
from headers import headers
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 参股控股  https://www.tianyancha.com/pagination/holdingCompany.xhtml?ps=10&pn=2&id=877576&_=1524449171624
# 对外投资
# 股东


# test = int(time.time() * 1000)
# print(test)
# test_str = str(test)
# print(len(test_str))
# ttt = '1524449171624'
# print(len(ttt))
CLIENT = MongoClient('localhost', 27017)
DB = CLIENT['tian_yan_cha']


def share_holdings():
    collection = DB['share_holdings']
    base_url = 'https://www.tianyancha.com/pagination/holdingCompany.xhtml?ps=10&pn={}&id=877576&_={}'
    # pn = 1
    time_param = int(time.time() * 1000)
    all_urls = [base_url.format(i, time_param) for i in range(1, 6)]
    columns = ['关联公司', '参股关系', '参股比例 （%）', '投资金额 （万元）', '被参股公司 净利润(元)', '是否报表合并', '被参股公司 主营业务']
    df = pd.DataFrame(columns=columns)
    for url in all_urls:
        print(url)
        r = requests.get(url, headers=headers, verify=False)
        r.encoding = 'utf8'
        # d = Pq(r.text).make_links_absolute(base_url=url)
        print(r.text)
        collection.insert_one({'share_holding': r.text})
        # titles = [i.text() for i in d('thead tr th').items()]
        # print(titles)
        # data = [i.text() for i in d('tbody tr').items()]
        # print(data)
        # print(data[0])
        # test = np.array(data[0].split(''))
        # print(test)
        # print(type(test))
        # break


if __name__ == '__main__':
    share_holdings()