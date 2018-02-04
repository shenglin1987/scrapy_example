#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
from tutorial.items import DmozItem 
import scrapy

global Debug
Debug = False


class DmozSpider(Spider):
    name = "pexels"
    site = 'https://www.pexels.com'
    start_urls = []
    categories = ['love', 'blur', 'rain', 'universe', 'sad', 'wall', 'fun', 'person', 'city', 'relax', 'baby', 'family', 'street', 'happy', 'hair', 'couple', 'sea', 'beach', 'success', 'sky']
    for category in categories:
        for i in range(1, 200):
            start_urls.append('https://www.pexels.com/search/%s/?page=%d'%(category, i))
    

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html
        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        img_urls = response.xpath('/html/body/div[1]/div[2]/div[3]/article/a/@href').extract()
        for img_url in img_urls:
            #print 'img_url: ', img_url
            img_url = self.site + img_url
            yield scrapy.Request(img_url.encode('utf-8'), callback=self.parse_details)


    def parse_details(self, response):
        img_url = response.xpath('/html/body/div[1]/div[2]/section[1]/div[2]/div[2]/div/a/@href').extract()[0]
        img_tags = response.xpath('/html/body/div[1]/div[2]/section[2]/div[1]/div[3]/ul/li/a/text()').extract()

        img_item = DmozItem()
        img_item['img_url'] = img_url
        img_item['img_tags'] = img_tags
        yield img_item
