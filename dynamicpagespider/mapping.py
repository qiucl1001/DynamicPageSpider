# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

from dynamicpagespider.doubanspider import DouBanMovieSpider
from dynamicpagespider.careertencentspider import CareerTenCentSpider
from dynamicpagespider.bibivideospider import BiBiVideoSpider


run_map = {
    "movie": DouBanMovieSpider,
    "career": CareerTenCentSpider,
    "bilibili": BiBiVideoSpider
}


def create_func(name):
    return run_map.get(name)

