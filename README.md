# DynamicPageSpider

备注：本项目主要演示了动态页面加载反爬虫，
该项目含3个子项目：
1. 豆瓣电影剧情分类排行榜动态加载抓取， 并将数据分别输入json, csv, mongodb
2. 腾讯招聘网站动态分页加载耳机页面岗位信息抓取， 并将数据分别写入mongodb, mysql数据库
3. 哔哩哔哩网站小视屏以及图片等二进制数据抓取， 将文件保存到本地文件

# 环境安装
python3+以上版本

# 三方库安装
```
pip install -r requirements.txt

```

# 启动程序
```
cd dynamicpagespider
python main.py

```

# node
```
# 查看所有数据库命令：
show databases;

# 创建mysql数据库命令：
create database if not exists python_spider default charset="utf8";

# 切换数据库命令：
use database_name
e.g.
mysql> use python_spider
Database changed

mysql> show tables;
+-------------------------+
| Tables_in_python_spider |
+-------------------------+
|                         |
+-------------------------+
0 row in set (0.00 sec)

# 创建数据表命令：
create table ten_cent_career(
	id int unsigned not null primary key auto_increment,
	position_name varchar(255),
	location  varchar(64),
	category varchar(128),
	responsibility longtext,
	requirement longtext,
	publish_date varchar(128),
	detail_url varchar(128)
);

mysql> show tables;
+-------------------------+
| Tables_in_python_spider |
+-------------------------+
| ten_cent_career         |
+-------------------------+
1 row in set (0.00 sec)

#
mysql> describe ten_cent_career;
+----------------+------------------+------+-----+---------+----------------+
| Field          | Type             | Null | Key | Default | Extra          |
+----------------+------------------+------+-----+---------+----------------+
| id             | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| position_name  | varchar(255)     | YES  |     | NULL    |                |
| location       | varchar(64)      | YES  |     | NULL    |                |
| category       | varchar(128)     | YES  |     | NULL    |                |
| responsibility | longtext         | YES  |     | NULL    |                |
| requirement    | longtext         | YES  |     | NULL    |                |
| publish_date   | varchar(128)     | YES  |     | NULL    |                |
| detail_url     | varchar(128)     | YES  |     | NULL    |                |
+----------------+------------------+------+-----+---------+----------------+
8 rows in set (0.01 sec)

```

