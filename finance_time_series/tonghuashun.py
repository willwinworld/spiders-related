#! python3
# -*- coding: utf-8 -*-
import requests
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from tonghuashun_headers import headers
from config import tong_hua_shun_db, tong_hua_shun_response

year_2014_param = ['2014{}'.format(i) for i in range(10, 13)]
year_2015_param = ['20150{}'.format(i) if i < 10 else '2015{}'.format(i) for i in range(1, 13)]
year_2016_param = ['20160{}'.format(i) if i < 10 else '2016{}'.format(i) for i in range(1, 13)]
year_2017_param = ['20170{}'.format(i) if i < 10 else '2017{}'.format(i) for i in range(1, 13)]
year_2018_param = ['20180{}'.format(i) for i in range(1, 6)]
total_param = year_2014_param + year_2015_param + year_2016_param + year_2017_param + year_2018_param

base_url = 'http://comment.10jqka.com.cn/tzrl/getTzrlData.php?callback=callback_dt&type=data&date={}'
total_url = [base_url.format(i) for i in total_param]


def request_and_save(url):
    r = requests.get(url, headers=headers)
    tong_hua_shun_response.insert({'response': r.text}, check_keys=False)


def parallel():
    pool = Pool(processes=cpu_count())
    pool.map(request_and_save, total_url)
    pool.close()
    pool.join()


if __name__ == '__main__':
    parallel()