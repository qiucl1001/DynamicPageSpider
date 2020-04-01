# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import os
import csv
import json
import hashlib
from urllib.parse import quote
from dynamicpagespider.utils import get_page
from dynamicpagespider.useragents import GetRandomUserAgent
from dynamicpagespider.items import DouBanItems

import pymongo
from dynamicpagespider.settings import MONGODB_HOST, MONGODB_PORT, MONGO_DB, CLASSIFICATION_MAPPING


class DouBanMovieSpider(object):
    """获取豆瓣排行榜中的各种类型电影的相关信息"""
    def __init__(self):
        self.url = "https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start=0&limit={}"
        self.headers = {
            "User-Agent": GetRandomUserAgent().random,
            "Referer": "https://movie.douban.com/typerank?type_name={}&type={}&interval_id=100:90"
                       "&action=",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # mongodb数据库连接相关配置
        self.client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
        self.db = self.client[MONGO_DB]

        self.type_name = None
        self.csv_field_flag = False  # 设置csv表头字段只写一次

    def get_page_source(self, type_name, type_, limit):
        """
        获取网页源代码
         :param type_name:电影剧情类型名称  str数据类型
        :param type_:电影部剧情类型编号  str数据类型
        :param limit:电影部数  str数据类型
        :return:
        """
        self.headers["Referer"] = self.headers["Referer"].format(quote(type_name), type_)
        options = self.headers
        response = get_page(self.url.format(type_, limit), options)
        if response:
            json_str = response.json()
            self.parse_page(json_str)

    def parse_page(self, json_str):
        """
        解析网页数据
        :param json_str: 网页源代码  str类型   '[{}, {}, {} ...]'
        :return: item
        """
        item = DouBanItems()
        # 定义一个自定义字段与json数据中额字段的映射关系，key：item中的自定义字段，value: json数据中的字段
        filed_map = {
            "rank": "rank",
            "title": "title",
            "actors": "actors",
            "publish_date": "release_date",
            "country": "regions",
            "types": "types",
            "score": "score",
            "vote_count": "vote_count",
            "avatar_url": "cover_url",
            "detail_url": "url"
        }
        for movie in json_str:
            for field, attr in filed_map.items():
                item[field] = movie.get(attr)

            movie_tag = hashlib.md5(str(movie).encode("utf-8")).hexdigest()

            # 将数据保存到数据库
            self.save_movie_2_mongodb(item, movie_tag)
            # 将数据保存到本地json文件中
            self.save_movie_2_json(item, movie_tag)
            # 将数据保存到本地csv文件中
            self.save_movie_2_csv(item, movie_tag)

    def save_movie_2_mongodb(self, message, movie_tag):
        """
        将数据保存到mongodb数据库
        :param message: 每部电影相关数据信息
        :param movie_tag: 每部电影生成的电子指纹
        :return:
        """
        if self.db[self.type_name].insert_one(dict(message)):
            print("--->  {} save mongodb success!  <---".format(movie_tag))

    def save_movie_2_json(self, message, movie_tag):
        """
        将数据保以json格式保存到本地
        :param message: 每部电影相关数据信息
        :param movie_tag: 每部电影生成的电子指纹
        :return:
        """
        movie_data = json.dumps(dict(message), ensure_ascii=False)
        json_path = os.path.join(self.base_path, "json")
        if not os.path.exists(json_path):
            os.makedirs(json_path)
        filename = os.path.join(json_path, self.__class__.__name__ + ".json")
        with open(filename, "a", encoding="utf-8") as f:
            f.write(movie_data + "\n")
        print("--->  {} save json success!  <---".format(movie_tag))

    def save_movie_2_csv(self, message, movie_tag):
        """
        将数据以csv格式保存到本地
        :param message:每部电影相关数据信息
        :param movie_tag: 每部电影生成的电子指纹
        :return:
        """
        field_names = list(message.keys())
        csv_path = os.path.join(self.base_path, "csv")
        if not os.path.exists(csv_path):
            os.makedirs(csv_path)
        filename = os.path.join(csv_path, self.__class__.__name__ + ".csv")
        with open(filename, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            if not self.csv_field_flag:
                writer.writeheader()
                self.csv_field_flag = True
            writer.writerow(message)
        print("--->  {} save csv success!  <---".format(movie_tag))

    def run(self):
        """程序入口"""
        movie_category = list(CLASSIFICATION_MAPPING.keys())
        print("=="*50)
        print("豆瓣电影分类排行榜剧情如下：")
        print(movie_category)
        print("=="*50)
        print(" ")
        category_num = input("请输入要查看的电影剧情分类序号：")

        type_name = list(CLASSIFICATION_MAPPING.get(category_num).keys())[0]
        self.type_name = type_name
        type_ = list(CLASSIFICATION_MAPPING.get(category_num).values())[0]

        limit = input("请输入要查看的的电影部数：")
        if all([
            category_num,
            limit
        ]):
            self.get_page_source(type_name, type_, limit)
        else:
            print("非法输入， 输入不能为空，请重新输入！")
            self.run()


if __name__ == '__main__':
    d = DouBanMovieSpider()
    d.run()
