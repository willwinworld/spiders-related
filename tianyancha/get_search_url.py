#! python3
# -*- coding: utf-8 -*-
import re
from pyquery import PyQuery as Pq
from dialogue.dumblog import dlog
from config import search_db, search_response, search_optimal_url


logger = dlog(__name__, console='debug')


def save(collection, data):
    collection.insert(data, check_keys=False)


def get_optimal_search_url():
    for element in search_response.find():
        keys = list(element.keys())
        target_key = keys[1]
        logger.info(target_key)
        html = element[target_key]
        d = Pq(html).make_links_absolute(base_url='https://www.tianyancha.com')
        # url = d('.b-c-white.search_result_container div:eq(0) .search_right_item.ml10 div:eq(0) a').attr('href')
        url = d('.query_name.sv-search-company.f18.in-block.vertical-middle').attr('href')
        logger.info(url)
        company_name = re.findall(r'key=.+', target_key)[0].replace('key=', '')
        logger.info(company_name)
        if url is not None:
            data = {company_name: url}
            save(search_optimal_url, data)
        # break


if __name__ == '__main__':
    get_optimal_search_url()
