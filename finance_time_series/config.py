#! python3
# -*- coding: utf-8 -*-
from pymongo import MongoClient

# mongodb配置
client = MongoClient('localhost', 27017)
db = client['xin_hua_she']
china_data_dict = db['china_data_dict']
america_data_dict = db['america_data_dict']

china_db = client['xin_hua_she_china']
america_db = client['xin_hua_she_america']

tong_hua_shun_db = client['tong_hua_shun']
tong_hua_shun_response = tong_hua_shun_db['tong_hua_shun_response']


east_money_db = client['east_money_db']
east_money_response = east_money_db['east_money_response']

__all__ = [china_db, america_db, china_data_dict, america_data_dict, tong_hua_shun_db, tong_hua_shun_response,
           east_money_db, east_money_response]
