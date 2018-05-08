#! python3
# -*- coding: utf-8 -*-
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
search_db = client['search']
search_response = search_db['search_response']  # 查询搜索原始网页结果
search_optimal_url = search_db['search_optimal_url']  # 解析过后的最优查询url
search_info_html = search_db['search_info_html']  # 查询结果的url的html

__all__ = [search_db, search_response, search_optimal_url]
