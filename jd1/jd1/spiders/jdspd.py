# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jd1.items import Jd1Item
import requests
import json

class JdspdSpider(CrawlSpider):
    name = 'jdspd'
    allowed_domains = ['jd.com']
    start_urls = ['https://list.jd.com/list.html?cat=12473,12479&ev=3184%5F79114&page=1&sort=sort%5Frank%5Fasc&trans=1&JL=6_0_0']
    xpath=["//span[@class='p-num']/a[@class=' ']","//span[@class='p-num']/a[@class='curr']","//span[@class='p-num']/a[@class='']"]
    rules = (
        Rule(LinkExtractor(allow=r'.+\?cat=12473,12479&ev=3184%5F79114&page=[1-9][0-9]*&sort=sort%5Frank%5Fasc&trans=1&JL=6_0_0',restrict_xpaths=(xpath)), callback='parse_item', follow=True),
    )
    def parse_item(self, response):
        i = Jd1Item()
        i['name'] = response.xpath("//div[@class='p-name']/a/em/text()").extract()
        i['bookid']=response.xpath("//div[@class='gl-i-wrap j-sku-item']/@data-sku").extract()
        i['link'] = response.xpath("//div[@class='p-name']/a/@href").extract()
        p_idstr='%2CJ_'.join(i['bookid'])
        price_url = 'http://p.3.cn/prices/mgets?skuIds=J_' + p_idstr
        p_data=requests.get(price_url).json()
        i['price']=list(map(lambda x:x['p'],p_data))
        c_idstr = ','.join(i['bookid'])
        comment_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=' + c_idstr
        c_data = requests.get(comment_url).json()
        i['comnum'] = list(map(lambda x:x['CommentCount'],c_data['CommentsCount']))
        return i


