# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jd.items import JdItem


class JdSpider(CrawlSpider):
    name = 'Jdspd'
    allowed_domains = ['jd.com']
    start_urls = ['https://list.jd.com/list.html?cat=12473,12479&ev=3184_79114']

    rules = (
        Rule(LinkExtractor(allow=(r'.+?\?cat=12473,12479&ev=3184_79114&page=[0-9]+.+')),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = JdItem()
        i['name']=response.xpath("//div[@class='p-name']/text()").extract()
        i['price']=response.xpath("//span[@class='price_n']/text()").extract()
        print(i['name'])
        # print(i['price'])
        i['link']=response.xpath("//a[@name='itemlist-title']/@href").extract()
        i['comnum']=response.xpath("//a[@dd_name='单品评论']/text()").extract()

        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
