#! python3
# -*- coding: utf-8 -*-
import requests
import time
from random import uniform
from pyquery import PyQuery as Pq
from bson.objectid import ObjectId
from headers import xin_hua_headers
from config import china_data_dict, america_data_dict, xin_hua_she_china_db, xin_hua_she_america_db
from proxy import Proxy


def save(collection, data):
    collection.insert(data, check_keys=False)


def data_link(url, collection):
    """
    获取http://dc.xinhua08.com/8001的外链接，以及对应名称
    获取http://dc.xinhua08.com/8002的外链接，以及对应名称
    :return:
    """
    r = requests.get(url, headers=xin_hua_headers)
    r.encoding = None
    d = Pq(r.text).make_links_absolute(base_url=url)
    relationship = [{i.text(): i.attr('href')} for i in d('.mainContent li a').items() if i.text() != '']
    print(relationship)
    for element in relationship:
        print(element)
        save(collection=collection, data=element)


def specific_data(database, collection):
    for record in collection.find({"_id": {"$gt": ObjectId("5ae043180e948e692c94d37e")}}):
        try:
            print(record)
            for key, value in record.items():
                if key != '_id' and len(key) != 0:
                    print(key)
                    print(Proxy.get_proxy())
                    r = requests.get(value, headers=xin_hua_headers, proxies=Proxy.get_proxy())
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
                            rest_r = requests.get(link, headers=xin_hua_headers, proxies=Proxy.get_proxy())
                            time.sleep(uniform(2, 4))
                            rest_r.encoding = None
                            rest_d = Pq(rest_r.text).make_links_absolute(base_url=link)
                            page_rest_result = [{'category': key, 'category_url': value,
                                                 'article_url': i('a').attr('href'),
                                                 'article_title': i('a').text(),
                                                 'article_time': i('span').text()}
                                                for i in rest_d('.unilist li').items()]
                            total_result.extend(page_rest_result)
                    print(total_result)
                    for item in total_result:
                        target_collection = database[key]
                        save(target_collection, item)
        except Exception as err:
            print(err)
            continue


if __name__ == '__main__':
    # data_link('http://dc.xinhua08.com/8001', china_data_dict)
    # data_link('http://dc.xinhua08.com/8002', america_data_dict)
    # specific_data(xin_hua_she_china_db, china_data_dict)
    specific_data(xin_hua_she_america_db, america_data_dict)

# 在伪造数据之前，先要得到低偏差， 高方差的分类器
# 增大分类器的特征，或者在神经网络中增加隐藏层的单元数，直到你得到偏差比较小的分类器
