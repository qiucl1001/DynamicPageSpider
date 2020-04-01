# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

from dynamicpagespider.mapping import create_func


def main():
    print("movie")
    print("career")
    print("bilibili")
    name = input("请选择想要爬取的数据类型：")
    class_ = create_func(name)
    print(class_)
    class_().run()


if __name__ == '__main__':
    main()
