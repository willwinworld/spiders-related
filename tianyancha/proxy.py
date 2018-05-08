#! python3
# -*- coding: utf-8 -*-
import os
import asyncio
import aiohttp
import json
import requests
import subprocess
from random import choice
from headers import headers
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Proxy(object):
    proxy_url = 'http://127.0.0.1:5000/proxy?count=5&anonymity=anonymous&protocol=https'
    test_url = 'https://www.tianyancha.com/search?key=%E5%B9%B3%E5%AE%89&rnd='

    @staticmethod
    def trigger_proxy():
        base_path = os.path.abspath(os.path.dirname(__file__))
        subprocess.Popen(['py', '-3', 'run.py'], cwd='%s' % base_path)

    @classmethod
    def get_proxy(cls):
        five_fastest_proxy = requests.get(cls.proxy_url).content
        five_fastest_proxy_list = json.loads(five_fastest_proxy)
        usable = []
        for proxy in five_fastest_proxy_list:
            try:
                requests_format_proxy = {'http': 'http://' + proxy[0] + ':' + proxy[1],
                                         'https': 'http://' + proxy[0] + ':' + proxy[1]}
                r = requests.get(cls.test_url, headers=headers, verify=False, timeout=1, proxies=requests_format_proxy)
                if r.status_code == 200:
                    usable.append(requests_format_proxy)
            except Exception as err:
                continue
        if len(usable) != 0:
            return choice(usable)
        else:
            return -1

    @classmethod
    async def proxy_request(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.proxy_url) as response:
                return await response.text()

    @classmethod
    async def proxy_response(cls):
        response_text = await cls.proxy_request()
        return response_text

    @classmethod
    async def proxy_random(cls):
        result = await cls.proxy_response()
        proxy_list = json.loads(result)
        usable = []
        for proxy in proxy_list:
            proxy_ip_address = 'http://' + proxy[0] + ':' + proxy[1]
            usable.append(proxy_ip_address)
        return choice(usable)

    @classmethod
    async def proxy_usable(cls):
        result = await cls.proxy_response()
        proxy_list = json.loads(result)
        usable = []
        for proxy in proxy_list:
            requests_format_proxy = {'http': 'http://' + proxy[0] + ':' + proxy[1],
                                     'https': 'http://' + proxy[0] + ':' + proxy[1]}
            try:
                r = requests.get(cls.test_url, headers=headers,
                                 verify=False, proxies=requests_format_proxy, timeout=1)
                if r.status_code == 200:
                    aiohttp_format_proxy = 'http://' + proxy[0] + ':' + proxy[1]
                    print(aiohttp_format_proxy)
                    usable.append(aiohttp_format_proxy)
            except Exception as err:
                continue
        if len(usable) != 0:
            return choice(usable)
        else:
            return -1


__all__ = [Proxy]
# if __name__ == '__main__':
#     res = Proxy().get_proxy()
#     print(res)
#     loop = asyncio.get_event_loop()
#     f = asyncio.wait([Proxy().proxy_usable()])
#     try:
#         completed = loop.run_until_complete(f)
#         print(completed)
#     finally:
#         loop.close()
