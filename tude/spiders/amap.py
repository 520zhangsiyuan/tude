# -*- coding: utf-8 -*-
import json
import sys
import scrapy
import pymysql
from scrapy.utils.project import get_project_settings
from tude.items import TudeItem 
class AmapSpider(scrapy.Spider):
    name = 'amap'
    allowed_domains = ['amap.com']
    url = 'https://restapi.amap.com/v3/place/text?key=你申请的key&keywords='
	#初始地名
    name1 = '郑州绕城高速郑州西服务区充电站（东区）'
    start_urls = [url+name]
	#确定爬取的数量
    i = 0
    def __init__(self):
	#初始化连接mysql数据，从setting获取自定义的数据
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.pwd = settings['DB_PWD']
        self.name = settings['DB_NAME']
        self.charset = settings['DB_CHARSET']
        self.connect()

    def connect(self):
	#连接mysql
        self.conn = pymysql.connect(host=self.host,
        	port=self.port,
                user=self.user,
                password=self.pwd,
                db=self.name,
                charset=self.charset)
        #定义游标
	self.cursor = self.conn.cursor()

    def close_spider(self, spider):
	#关闭游标数据库连接等
	self.conn.close()
        self.cursor.close()
    def parse(self, response):
       	item = TudeItem()
	#sql = "select charge_name from charges limit %d,1"%self.i
        reload(sys)
	sys.setdefaultencoding( "utf-8" )
	print self.i
	#print sql
	self.i += 1
	# 执行sql语句
        #self.cursor.execute(sql)
        #result = self.cursor.fetchall()
	#record = result[0]
	#name = record[0]
	#print name
	#new_url = self.url+name
	#data = json.loads(response.body)
	#data = response.body
	#print data
	#data = data.decode('unicode_escape')	
	#data1 = data.replace('\r', '\\r').replace('\n', '\\n')
	r1 = json.loads(response.body,strict=False)
	#print data
	print r1['count']
	#print r1
	if r1['count'] =='1' :
		print '找到了'
		item['charge_name'] = self.name1.encode('utf-8')
		tude = r1['pois'][0]['location'].split(",")
		print tude
		item['latitude'] = tude[1]
		print tude[1]
		item['longitude'] = tude[0]
	else:
		item['charge_name'] = self.name1.encode('utf-8')
                #tude = r1['pois'][0]['location'].split(",")
                #print tude
                item['latitude'] = ""
                #print tude[1]
                item['longitude'] = ""

		print '未找到'
		#yield scrapy.Request(new_url, callback = self.parse)
	sql = "select charge_name from charges limit %d,1"%self.i
	self.cursor.execute(sql)
        result = self.cursor.fetchall()
        record = result[0]
        self.name1 = record[0]
	new_url = self.url+self.name1
 	yield scrapy.Request(new_url, callback = self.parse)
	yield item	
