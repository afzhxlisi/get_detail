# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.http import Request
from get_detail.items import GetDetailItem
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb

class CrawlSpider(scrapy.Spider):

    name = "domz"
    allowed_domains = ["sh.lianjia.com"]
    start_urls = ['http://sh.lianjia.com/ershoufang']
    page = 1;
    count =1;
    total = 1;
    def parse(self, response):
        urls = self.getComList();
        for url in urls:
            url = "http://sh.lianjia.com" + url[0]
            yield Request(url, callback=self.parseItem)
    def parseItem(self,response):
        sevenDaycount = response.xpath("//div[contains(@class,'record')]//div[@class='count']/text()").extract()
        totalCount = response.xpath("//div[contains(@class,'record')]//div[@class='totalCount']/span/text()").extract()
        item = GetDetailItem()
        item['sevenDaycount'] = sevenDaycount[0]
        item['totalCount'] = totalCount[0]
        item['fangurl']=response.url
        yield item
    def getComList(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='12345678', db='test', port=3306,
                                        charset='utf8')
        self.cur = self.conn.cursor()

        str = datetime.date.today().__str__()
        cur = self.cur
        cur.execute('select fangurl from lianjia where date(time) =date(\''+str+'\')')
        results = cur.fetchall()
        self.cur.close()
        self.conn.close()
        return results