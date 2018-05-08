#! python3
# -*- coding: utf-8 -*-
from pymongo import MongoClient


client = MongoClient('192.168.1.110', 47017)
xin_hua_she_db = client['xin_hua_she']
china_data_dict = xin_hua_she_db['china_data_dict']
america_data_dict = xin_hua_she_db['america_data_dict']

xin_hua_she_china_db = client['xin_hua_she_china']
xin_hua_she_america_db = client['xin_hua_she_america']


__all__ = [china_data_dict, america_data_dict, xin_hua_she_china_db, xin_hua_she_america_db]

