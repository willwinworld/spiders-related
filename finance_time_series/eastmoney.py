#! python3
# -*- coding: utf-8 -*-
import requests
import time
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from config import east_money_db, east_money_response

date_param = '2018-04-24'
# page_param = '1'
time_param = int(time.time() * 1000)
base_url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=GSRL&sty=GSRL&stat=21&fd={}&p={}&ps=50&cb=callback&callback=callback&_={}'
# test_url = base_url.format(date_param, page_param, time_param)

# r = requests.get(test_url)
# print(r.text)
total_url = [base_url.format(date_param, i, time_param) for i in range(1, 100)]


def request_and_save(url):
    r = requests.get(url)
    east_money_response.insert({'response': r.text}, check_keys=False)


def parallel():
    pool = Pool(processes=cpu_count())
    pool.map(request_and_save, total_url)
    pool.close()
    pool.join()


if __name__ == '__main__':
    parallel()
