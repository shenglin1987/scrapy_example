#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from tutorial.items import DmozItem 
import scrapy

global Debug
Debug = False


class DmozSpider(Spider):
    name = "dmoz"
    site = 'http://www.quanjing.com'
    start_urls = [
      'http://www.quanjing.com/category/104-1.html',
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html
        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        img_urls = response.xpath('//*[@id="ulImgHolder"]/li/span[1]/a/@href').extract()
        for img_url in img_urls:
            #print 'img_url: ', img_url
            img_url = self.site + img_url
            yield scrapy.Request(img_url.encode('utf-8'), callback=self.parse_next_page)

    def parse_next_page(self, response):
        #print 'in function: parse_next_page'
        #print 'response page: ', response.url
   
        try:
            img_urls = response.xpath('//*[@id="gallery-list"]/li/a/@href').extract()
            #print img_urls
        except:
            print 'img_url extract exception: ', img_urls
        for img_url in img_urls:
            img_url = self.site + img_url
            #print 'img_url: ', img_url
            yield scrapy.Request(img_url.encode('utf-8'), callback=self.parse_details)


    def parse_details(self, response):
        if Debug:
            print 'response to url: ', response.url

        img_url = response.xpath('//*[@id="picurl"]/@src').extract()[0]
        img_tags = response.xpath('//*[@id="Ul1"]/li/a').extract()
        import re
        img_tags = [re.findall('>.*<', item, re.U)[0].strip('><') for item in img_tags]

        if Debug:
            print 'img_url: ', img_url
            print 'img_tags: ', img_tags
            for img_tag in img_tags:
                print img_tag
        img_item = DmozItem()
        img_item['img_url'] = img_url
        img_item['img_tags'] = img_tags
        yield img_item
