#! python3
# -*- coding: utf-8 -*-
import requests
import time
from random import uniform
from pyquery import PyQuery as Pq
from bson.objectid import ObjectId
from xinhua_headers import headers
from proxy import Proxy
from config import china_db, america_db, china_data_dict, america_data_dict


def save(collection, data):
    collection.insert(data, check_keys=False)


def china_data_link(url):
    """
    获取http://dc.xinhua08.com/8001的外链接，以及对应名称
    :return:
    """
    r = requests.get(url, headers=headers)
    r.encoding = None
    d = Pq(r.text).make_links_absolute(base_url=url)
    relationship = [{i.text(): i.attr('href')} for i in d('.mainContent li a').items()]
    print(relationship)
    for element in relationship:
        print(element)
        save(china_data_dict, element)


def america_data_link(url):
    """
    获取http://dc.xinhua08.com/8002的外链接，以及对应名称
    :return:
    """
    r = requests.get(url, headers=headers)
    r.encoding = None
    d = Pq(r.text).make_links_absolute(base_url=url)
    relationship = [{i.text(): i.attr('href')} for i in d('.mainContent li a').items()]
    print(relationship)
    for element in relationship:
        print(element)
        save(america_data_dict, element)


def china_specific_data(collection):
    for record in collection.find():
        try:
            print(record)
            for key, value in record.items():
                if key != '_id' and len(key) != 0:
                    print(key)
                    print(Proxy.get_proxy())
                    r = requests.get(value, headers=headers, proxies=Proxy.get_proxy())
                    time.sleep(uniform(2, 4))
                    r.encoding = None
                    d = Pq(r.text).make_links_absolute(base_url=value)
                    page_one_result = [{'category': key, 'category_url': value, 'article_url': i('a').attr('href'),
                                        'article_title': i('a').text(), 'article_time': i('span').text()}
                                       for i in d('.unilist li').items()]
                    pagination = d('.page_down li').eq(-1).find('a').text()
                    pagination_length = len(pagination)
                    total_result = []
                    total_result.extend(page_one_result)
                    if pagination_length != 0:
                        # 说明不止有一页
                        total_page = int(d('.page_down li').eq(-2).find('a').text().replace('... ', ''))
                        rest_url = [value+'?page={}'.format(i) for i in range(2, total_page+1)]
                        for link in rest_url:
                            print(link)
                            rest_r = requests.get(link, headers=headers, proxies=Proxy.get_proxy())
                            time.sleep(uniform(2, 4))
                            rest_r.encoding = None
                            rest_d = Pq(rest_r.text).make_links_absolute(base_url=link)
                            page_rest_result = [{'category': key, 'category_url': value, 'article_url': i('a').attr('href'),
                                                 'article_title': i('a').text(), 'article_time': i('span').text()}
                                                for i in rest_d('.unilist li').items()]
                            total_result.extend(page_rest_result)
                    print(total_result)
                    for item in total_result:
                        target_collection = china_db[key]
                        save(target_collection, item)
        except Exception as err:
            print(err)
            continue
        # break


def america_specific_data(collection):
    for record in collection.find():
        print(record)
        for key, value in record.items():
            if key != '_id' and len(key) != 0:
                print(key)
                print(Proxy.get_proxy())
                r = requests.get(value, headers=headers, proxies=Proxy.get_proxy())
                time.sleep(uniform(2, 4))
                r.encoding = None
                d = Pq(r.text).make_links_absolute(base_url=value)
                page_one_result = [{'category': key, 'category_url': value, 'article_url': i('a').attr('href'),
                                    'article_title': i('a').text(), 'article_time': i('span').text()}
                                   for i in d('.unilist li').items()]
                pagination = d('.page_down li').eq(-1).find('a').text()
                pagination_length = len(pagination)
                total_result = []
                total_result.extend(page_one_result)
                if pagination_length != 0:
                    # 说明不止有一页
                    total_page = int(d('.page_down li').eq(-2).find('a').text().replace('... ', ''))
                    rest_url = [value+'?page={}'.format(i) for i in range(2, total_page+1)]
                    for link in rest_url:
                        print(link)
                        print(Proxy.get_proxy())
                        rest_r = requests.get(link, headers=headers, proxies=Proxy.get_proxy())
                        time.sleep(uniform(2, 4))
                        rest_r.encoding = None
                        rest_d = Pq(rest_r.text).make_links_absolute(base_url=link)
                        page_rest_result = [{'category': key, 'category_url': value, 'article_url': i('a').attr('href'),
                                             'article_title': i('a').text(), 'article_time': i('span').text()}
                                            for i in rest_d('.unilist li').items()]
                        total_result.extend(page_rest_result)
                print(total_result)
                for item in total_result:
                    target_collection = america_db[key]
                    save(target_collection, item)


if __name__ == '__main__':
    # china_data_link('http://dc.xinhua08.com/8001')
    # america_data_link('http://dc.xinhua08.com/8002')
    china_specific_data(china_data_dict)
    # america_specific_data(america_data_dict)
    # print(db.collection_names())
    # print(Proxy.get_proxy())
    # for test in china_data_dict.find({"_id": {"$gt": ObjectId("5add9f110e948e84dc98da98")}}):
    #     print(test)
