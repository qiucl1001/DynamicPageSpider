# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import time
import random
import hashlib
from urllib import parse
from dynamicpagespider.utils import get_page
from dynamicpagespider.items import CareerTenCentItems

import pymongo
from dynamicpagespider.settings import MONGODB_HOST, MONGODB_PORT, MONGO_TENCENT_DB

import pymysql
from dynamicpagespider.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


class CareerTenCentSpider(object):
    """腾讯招聘岗位抓取"""
    def __init__(self):
        """初始化"""
        self.base_url = "https://careers.tencent.com/tencentcareer/api/post/Query?"
        self.headers = {
            "authority": "careers.tencent.com",
            "method": "GET",
            "scheme": "https",
            "cookie": "pgv_pvi=8189616128; _ga=GA1.2.550222449.1574580516; _gcl_au=1.1.992385802.1584328697; "
                      "pgv_pvid=9007732956; loading=agree",
            # "referer": "https://careers.tencent.com/en-us/search.html",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }
        self.detail_base_url = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?"

        # mongodb数据库连接相关配置
        self.client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
        self.db = self.client[MONGO_TENCENT_DB]

        # mysql数据库连接相关配置
        self.conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset="utf8"
        )
        self.cursor = self.conn.cursor()
        self._sql = None
        self.keys = None
        self.values = None
        self.table = None
        self.career_data = None
        self.item = None

    @staticmethod
    def generate_ts():
        """
        生成时间戳
        :return:
        """
        return round(time.time()*1000)

    def parse_index_page(self, page_index):
        """
        获取列表页源代码，并提取相关数据
        :param page_index: 列表页码数
        :return:
        """
        params = {
            "timestamp": self.generate_ts(),
            "countryId": "",
            "cityId": "",
            "bgIds": "",
            "productId": "",
            "categoryId": "",
            "parentCategoryId": "",
            "attrId": "",
            "keyword": "",
            "pageIndex": page_index,
            "pageSize": "10",
            "language": "en-us",
            "area": ""
        }
        params_url_encode = parse.urlencode(params)
        list_page_url = self.base_url + params_url_encode
        self.headers["path"] = self.base_url.split(".com")[-1] + params_url_encode
        options = self.headers

        response = get_page(list_page_url, options)
        if response:
            json_str = response.json()

            # 提取详情页链接所需的参数PostId
            post_ids = json_str.get("Data").get("Posts")
            for post_id in post_ids:
                pd = post_id.get("PostId")
                query_detail_string = {
                    "timestamp": self.generate_ts(),
                    "postId": pd,
                    "language": "zh-cn"
                }
                detail_url = self.detail_base_url + parse.urlencode(query_detail_string)
                self.parse_detail_page(detail_url)
                time.sleep(random.randint(1, 4))
                # break

    def parse_detail_page(self, detail_url):
        """
        获取详情页网页源代码
        :param detail_url: 详情页地址
        :return:
        """
        item = CareerTenCentItems()

        # 定义一个自定义字段与json数据中额字段的映射关系，key：item中的自定义字段，value: json数据中的字段
        field_map = {
            "position_name": "RecruitPostName",
            "location": "LocationName",
            "category": "CategoryName",
            "responsibility": "Responsibility",
            "requirement": "Requirement",
            "publish_date": "LastUpdateTime",
            "detail_url": "PostURL"
        }

        path = detail_url.split(".com")[-1]
        self.headers["path"] = path
        options = self.headers

        resp = get_page(detail_url, options)
        if resp:
            json_str = resp.json()
            career = json_str.get("Data")
            career_tag = hashlib.md5(str(career).encode("utf-8")).hexdigest()
            for field, attr in field_map.items():
                item[field] = career.get(attr)

            # 将数据保存到mongo数据库
            self.save_career_2_mongo(item, career_tag)
            # 将数据保存到mysql数据库
            self.save_career_2_mysql(item, career_tag)

    def save_career_2_mongo(self, item, career_tag):
        """
        将数据保存到mongo数据库
        :param item: 招聘岗位网页源代码
        :param career_tag: 每个招聘岗位信息的电子指纹
        :return:
        """
        print(item)
        print("=="*100)
        if self.db[item.collections].insert_one(dict(item)):
            print("--->  {} save mongodb success!  <---".format(career_tag))

    def save_career_2_mysql(self, item, career_tag):
        """
        将数据保存到mysql数据库
        :param item:
        :param career_tag:
        :return:
        """
        print(item)
        print("==" * 100)

        self.item = item
        self.career_data = dict(item)
        try:
            self.cursor.execute(self.sql, tuple(self.career_data.values()))
            self.conn.commit()
            print("--->  {} save mysql success!  <---".format(career_tag))
        except Exception as e:
            print(e.args)
            self.conn.rollback()

    @property
    def sql(self):
        self.keys = ", ".join(self.career_data.keys())
        self.values = ", ".join(["%s"] * len(self.career_data))
        self.table = self.item.tables
        print({"keys": self.keys, "values": self.values, "table": self.table})
        if not self._sql:
            self._sql = "insert into %s(%s) values(%s);" % (self.table, self.keys, self.values)
            return self._sql
        return self._sql

    def run(self):
        try:
            total_page_index = int(input("请输入你要获取的总页数："))
            for page in range(1, total_page_index + 1):
                self.parse_index_page(page)
                time.sleep(random.uniform(1, 3))
        except ValueError:
            print("非法输入，您输入的不是一个数字，请重新输入！")
            self.run()


if __name__ == '__main__':
    c = CareerTenCentSpider()
    c.run()
