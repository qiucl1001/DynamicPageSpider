# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import requests
from requests.exceptions import ConnectionError


# 默认请求头
BASE_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3,application/json, text/javascript",
    "Accept-Language": "en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
}


def get_page(url, options={}):
    """抓取网页"""
    headers = dict(BASE_HEADERS, **options)

    try:
        response = requests.get(url=url, headers=headers)
        url = response.url
        status_code = response.status_code
        if response.status_code == 200:
            print({"info": "抓取成功...", "url": url, "status_code": status_code})
            return response
        else:
            print({"info": "抓取失败...", "url": url, "status_code": status_code})
    except ConnectionError:
        print("抓取失败...")
        return None
