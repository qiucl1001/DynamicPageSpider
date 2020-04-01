# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import os
import time
import random
import requests
from hashlib import md5


class BiBiVideoSpider(object):
    """获取bilibili网站小视频"""
    def __init__(self):
        """初始化"""
        self.base_url = 'https://api.vc.bilibili.com/board/v1/ranking/top?page_size=10&next_offset={}' \
                        '&tag=%E4%BB%8A%E6%97%A5%E7%83%AD%E9%97%A8&platform=pc'
        self.headers = {
            # "Accept": "application/json, text/plain, */*",
            # "Accept-Language": "en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            # "Connection": "keep-alive",
            # "Host": "api.vc.bilibili.com",
            # "Origin": "https://vc.bilibili.com",
            # "Referer": "https://vc.bilibili.com/p/eden/rank",
            # "Sec-Fetch-Dest": "empty",
            # "Sec-Fetch-Mode": "cors",
            # "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
        }
        self.base_path = os.path.dirname(os.path.abspath(__file__))

    def parse_page(self, page_url):
        """
        获取列表页源代码
        :param page_url: 列表页代码
        :return:
        """
        resp = requests.get(url=page_url, headers=self.headers)
        if resp:
            json_str = resp.json()
            videos = json_str.get("data").get("items")
            for video in videos:
                video_url = video.get("item").get("video_playurl")
                self.download_video(video_url)

    def download_video(self, video_url):
        """
        下载小视频
        :param video_url:小视频下载链接地址
        :return:
        """
        video_content = requests.get(url=video_url, headers=self.headers).content
        filename = md5(video_content).hexdigest()

        video_path = os.path.join(self.base_path, "videos")

        if not os.path.exists(video_path):
            os.makedirs(video_path)
        filename_path = os.path.join(video_path, "{}.mp4".format(filename))
        with open(filename_path, "wb") as f:
            f.write(video_content)
        print("--------->{} 下载完成！<--------".format(filename))

    def run(self):
        page_number = int(input("请输入要抓取的小视屏页数："))
        page_list = [self.base_url.format(str(page*10 + 1)) for page in range(0, page_number + 1)]
        # print(page_list)
        for page_url in page_list:
            self.parse_page(page_url)
            time.sleep(random.randint(1, 3))


if __name__ == '__main__':
    b = BiBiVideoSpider()
    b.run()


