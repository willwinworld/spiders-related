#! python3
# -*- coding: utf-8 -*-
import requests
import time
from headers import headers
from random import uniform
from company_name import get_company_name
from dialogue.dumblog import dlog
from config import search_db, search_response
from proxy import Proxy
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


logger = dlog(__name__, console='debug')


def save(collection, data):
    collection.insert(data, check_keys=False)


def company_search_url(company_series):
    """
    通过表格的上市公司组成搜索url
    :return:
    """
    search_urls = []
    for index, item in company_series.iteritems():
        url = 'https://www.tianyancha.com/search?key={}'.format(item)
        search_urls.append(url)
    return search_urls


def send_search_request(url, count):
    proxy = Proxy().get_proxy()
    if isinstance(proxy, str):
        if count % 2 == 0:
            logger.info('has proxy, using proxy: {}'.format(proxy))
            r = requests.get(url, headers=headers, proxy=proxy, verify=False)
        else:
            logger.info('has proxy, not using proxy')
            r = requests.get(url, headers=headers, verify=False)
    else:
        logger.info('no proxy')
        r = requests.get(url, headers=headers, verify=False)
    logger.info(r.status_code)
    time.sleep(uniform(4, 8))
    if r.status_code == 200:
        data = r.text
        return {url: data}
    else:
        return {url: None}


def save_search_response(search_urls):
    count = 0
    for url in search_urls:
        logger.info(url)
        save(search_response, send_search_request(url, count))
        count += 1


def main():
    search_urls = company_search_url(get_company_name())
    save_search_response(search_urls[0:100])


if __name__ == '__main__':
    main()
