#! python3
# -*- coding: utf-8 -*-


xin_hua_headers = {
    'Host': 'dc.xinhua08.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://dc.xinhua08.com/1/c=1',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '_ga=GA1.2.1574701129.1524464468; _gid=GA1.2.2099190081.1524464468'
}


tong_hua_shun_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '__utmc=156575163; __utmz=156575163.1524543446.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1524543446; __utma=156575163.877258515.1524543446.1524547641.1524552846.3; __utmt=1; __utmb=156575163.1.10.1524552846; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1524552847',
    'Host': 'comment.10jqka.com.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://stock.10jqka.com.cn/fincalendar.shtml',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}


__all__ = [xin_hua_headers, tong_hua_shun_headers]