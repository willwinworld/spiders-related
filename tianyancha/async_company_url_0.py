#! python3
# -*- coding: utf-8 -*-
import requests
import asyncio
import aiohttp
from headers import headers
from company_name import get_company_name
from dialogue.dumblog import dlog
from config import search_db, search_response
from proxy import Proxy
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
    search_urls = []
    for index, item in company_series.iteritems():
        url = 'https://www.tianyancha.com/search?key={}'.format(item)
        search_urls.append(url)
    return search_urls


async def send_search_request(session, url):
    # proxy = await Proxy().proxy_random()
    # logger.info(proxy)
    async with session.get(url, headers=headers) as response:
        try:
            response_value = await response.text()
        except Exception as err:
            raise ValueError
        finally:
            response.release()
        return response_value


async def bound_send_search_request(sem, session, url):
    async with sem:
        await send_search_request(session, url)
        sem.release()


async def control():
    sem = asyncio.BoundedSemaphore(1000)
    search_urls = company_search_url(get_company_name()[0:2])

    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in search_urls:
            logger.info(url)
            task = asyncio.ensure_future(bound_send_search_request(sem, session, url))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        print(responses)
        return responses


def main():
    loop = asyncio.get_event_loop()
    f = asyncio.wait([control()])
    completed, pending = loop.run_until_complete(f)
    # for future in completed:
    #     print(future.result())
    #     break


if __name__ == '__main__':
    main()
    r = requests.get('https://www.tianyancha.com/search?key=%E4%B8%87%E7%A7%91A&rnd=&rnd=&rnd=', headers=headers, verify=False)
    print(r.text)