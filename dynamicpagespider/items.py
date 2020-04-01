# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import scrapy


class DouBanItems(scrapy.Item):
    """创建一个用来存储豆瓣电影的Item字段对象"""
    # 排名
    rank = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 演员
    actors = scrapy.Field()
    # 年份
    publish_date = scrapy.Field()
    # 国家
    country = scrapy.Field()
    # 类型
    types = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评价人数
    vote_count = scrapy.Field()
    # 海报
    avatar_url = scrapy.Field()
    # 详情地址
    detail_url = scrapy.Field()


class CareerTenCentItems(scrapy.Item):
    """创建一个用来存储腾讯招聘岗位的Item字段对象"""
    collections = tables = "ten_cent_career"
    # 岗位名称
    position_name = scrapy.Field()
    # 地点
    location = scrapy.Field()
    # 岗位所属分类
    category = scrapy.Field()
    # 岗位职责
    responsibility = scrapy.Field()
    # 岗位要求
    requirement = scrapy.Field()
    # 发布时间
    publish_date = scrapy.Field()
    # 详情地址
    detail_url = scrapy.Field()



