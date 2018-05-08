#! python3
# -*- coding: utf-8 -*-
import requests
import asyncio
import aiohttp
from company_name import get_company_name
from headers import headers
from dialogue.dumblog import dlog
from config import search_db, search_response
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


logger = dlog(__name__, console='debug')


def save(collection, data):
    collection.insert(data, check_keys=False)


def company_search_url(company_series):
    """
    通过表格的上市公司组成搜索url
    :return:
    """
    search_url = []
    for index, item in company_series.iteritems():
        url = 'https://www.tianyancha.com/search?key={}'.format(item)
        search_url.append(url)
    return search_url


async def send_search_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.text()


async def save_search_response(search_url):
    tasks = []

    for url in search_url:
        logger.info(url)
        task = asyncio.ensure_future(send_search_request(url))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    print(responses[0])
    [save(search_response, {'response_text': i}) for i in responses]
    return responses


# def company_url(search_url):
#     """
#     拿到搜索结果的对应公司的url
#     :param search_url:
#     :return:
#     """
#     for url in search_url:
#         r = requests.get(url, headers=headers, verify=False)
#         print(r.text)
#         d = Pq(r.text).make_links_absolute(base_url=url)
#         optimal_url = d('.b-c-white.search_result_container div:eq(0) .search_right_item.ml10 a').attr('href')
#         print(optimal_url)
#         break


# async def company_url(url):
#     proxy = Proxy.proxy_random()
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=headers, proxy=proxy) as response:
#             return await response.text()






# async def company_url(url):
#     proxy = Proxy.proxy_random()
#     print(proxy)
#     coroutines = [aiohttp.request('get', url=url, headers=headers, proxy=proxy) for url in search_url[0:3]]
#     result = await asyncio.gather(*coroutines, return_exceptions=True)
#     response_data = {
#         url: not isinstance(result, Exception) and result.status == 200
#         for url, result in zip(search_url, result)
#     }
#     # print(response_data)
#     return response_data


# async def company_url(search_url):
#     tasks = []
#
#     async with ClientSession() as session:
#         for url in search_url[0:3]:
#             task = asyncio.ensure_future(fetch(url))
#             tasks.append(task)
#
#         responses = await asyncio.gather(*tasks)
#     return responses


def main():
    loop = asyncio.get_event_loop()
    f = asyncio.wait([save_search_response(company_search_url(get_company_name())[0:3])])
    loop.run_until_complete(f)


if __name__ == '__main__':
    main()

