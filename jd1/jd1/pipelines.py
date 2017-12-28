# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
class Jd1Pipeline(object):
    def __init__(self):
        #刚开始时连接对应数据库
        self.conn=pymysql.connect(host="127.0.0.1", user="root", passwd="root", db="mypydb")
    def process_item(self, item, spider):
        #将获取到的name和keywd分别赋给变量name和变量key
        for i in range(0,len(item['name'])):
            name=item["name"][i]
            price=item["price"][i]
            link=item["link"][i]
            comnum=str(item["comnum"][i])
            bookid = item["bookid"][i]
            #构造对应的sql语句
            sql="insert into mytb(name,price,link,comnum,bookid) VALUES('"+name+"','"+price+"','"+link+"','"+comnum+"','"+bookid+"')"
            #通过query实现执行对应的sql语句
            self.conn.query(sql)
        return item
    def close_spider(self,spider):
        self.conn.close()