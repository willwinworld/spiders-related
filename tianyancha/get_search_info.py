#! python3
# -*- coding: utf-8 -*-
import json
import requests
import time
from random import uniform
from pyquery import PyQuery as Pq
from headers import headers
from dialogue.dumblog import dlog
from config import search_db, search_response, search_optimal_url, search_info_html
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


logger = dlog(__name__, console='debug')


def save(collection, data):
    collection.insert(data, check_keys=False)


def save_search_html():
    for element in search_optimal_url.find():
        keys = list(element.keys())
        company_name = keys[1]
        logger.info(company_name)
        company_url = element[company_name]
        logger.info(company_url)
        r = requests.get(company_url, headers=headers, verify=False)
        time.sleep(uniform(4, 8))
        if r.status_code == 200:
            data = {'company_name': company_name,
                    'company_url': company_url,
                    'company_html': r.text}
            save(search_info_html, data)


def extract_info():
    for element in search_info_html.find():
        company_name = element['company_name']
        d = Pq(element['company_html'])
        holding_company_head = [i.text() for i in d('#nav-main-holdingCompanyNum #_container_holdingCompany .table.companyInfo-table.f14 thead th').items()]
        holding_company_body = [i('td').text() for i in d('#nav-main-holdingCompanyNum #_container_holdingCompany .table.companyInfo-table.f14 tbody tr').items()]
        print(holding_company_head)
        print(holding_company_body)
        invest_count_head = [i.text() for i in d('#_container_invest .out-investment-container thead th').items()]
        invest_count_body = [i('td').text() for i in d('#_container_invest .out-investment-container tbody tr').items()]
        print(invest_count_head)
        print(invest_count_body)
        top_ten_head = [i.text() for i in d('#_container_topTenNum .table.companyInfo-table.f14 thead th').items()]
        top_ten_body = [i('td').text() for i in d('#_container_topTenNum .table.companyInfo-table.f14 tbody tr').items()]
        print(top_ten_head)
        print(top_ten_body)
        data = {'参股控股标题': holding_company_head, '参股控股内容': holding_company_body,
                '对外投资标题': invest_count_head, '对外投资内容': invest_count_body,
                '十大股东标题': top_ten_head, '十大股东内容': top_ten_body}
        with open('res/{}.json'.format(company_name), 'w') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True))
        # break


if __name__ == '__main__':
    extract_info()


