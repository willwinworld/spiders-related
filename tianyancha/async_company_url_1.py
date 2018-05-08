#! python3
# -*- coding: utf-8 -*-
import requests
import asyncio
import aiohttp
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


semaphore = asyncio.Semaphore(3)


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


async def send_search_request(url, count):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            # 阈值是在100个url左右，所以取50，每隔50url，睡眠1min
            logger.info(count)
            if count >= 50 and count % 50 == 0:
                # 神经网络识别验证码
                # https://antirobot.tianyancha.com/captcha/verify?
                logger.info('sleep really long time, trying to escape captcha')
                time.sleep(uniform(180, 300))
            proxy = await Proxy().proxy_usable()
            if isinstance(proxy, str):
                # 如果有可用的代理，通过奇偶数交替进行
                if count % 2 == 0:
                    logger.info('has proxy, using proxy: {}'.format(proxy))
                    session_get = session.get(url, headers=headers, proxy=proxy)
                    await asyncio.sleep(uniform(4, 8))
                else:
                    logger.info('has proxy, not using proxy')
                    session_get = session.get(url, headers=headers)
                    await asyncio.sleep(uniform(8, 16))
            else:
                # 如果没有可用的代理
                logger.info('no proxy')
                session_get = session.get(url, headers=headers)
                await asyncio.sleep(uniform(8, 16))
            logger.info(url)
            async with session_get as response:
                logger.info(response.status)
                data = await response.text()
            return {url: data}


async def save_search_response(search_urls):
    tasks = []

    count = 0
    for url in search_urls:
        task = asyncio.ensure_future(send_search_request(url, count))
        tasks.append(task)
        count += 1

    responses = await asyncio.gather(*tasks)
    [save(search_response, i) for i in responses]
    logger.info('saving to mongodb')
    return responses


def main():
    search_urls = company_search_url(get_company_name())
    logger.info(len(search_urls))
    loop = asyncio.get_event_loop()
    f = asyncio.wait([save_search_response(search_urls)])
    try:
        loop.run_until_complete(f)
    except Exception as err:
        loop.close()


if __name__ == '__main__':
    main()
    # proxies_list = [{'http': 'http://119.127.18.96:9999', 'https': 'https://119.127.18.96:9999'},
    #                 {'http': 'http://120.77.254.116:3128', 'https': 'https://120.77.254.116:3128'},
    #                 {'http': 'http://123.56.75.209:3128', 'https': 'https://123.56.75.209:3128'},
    #                 {'http': 'http://113.116.183.112:9000', 'https': 'https://113.116.183.112:9000'},
    #                 {'http': 'http://175.11.214.90:808', 'https': 'https://175.11.214.90:808'}]
    # for proxies in proxies_list:
    #     try:
    #         r = requests.get('https://www.tianyancha.com/search?key=%E4%B8%87%E7%A7%91A&rnd=&rnd=&rnd=', headers=headers,
    #                          verify=False, proxies=proxies, timeout=1)
    #         print(r.status_code)
    #         if r.status_code == 200:
    #             print(r.text)
    #     except Exception as err:
    #         print(err)
    #         continue

    # https://antirobot.tianyancha.com/captcha/verify?return_url=https%3A%2F%2Fwww.tianyancha.com%2Fsearch%3Fkey%3D%25E4%25B8%2587%25E8%25BE%25BE%26rnd%3D&rnd=
