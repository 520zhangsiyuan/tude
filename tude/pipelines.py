# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.utils.project import get_project_settings
import pymysql

class TudePipeline(object):
    def __init__(self):
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.pwd = settings['DB_PWD']
        self.name = settings['DB_NAME']
        self.charset = settings['DB_CHARSET']

        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.host,
                             port=self.port,
                             user=self.user,
                             password=self.pwd,
                             db=self.name,
                             charset=self.charset)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()

    def process_item(self, item, spider):
        sql = "UPDATE charges SET latitude = '%s' ,longitude='%s' where charge_name = '%s'"%(item['latitude'],item['longitude'],item['charge_name'])
        # 执行sql语句
        self.cursor.execute(sql)
        self.conn.commit()
        return item


