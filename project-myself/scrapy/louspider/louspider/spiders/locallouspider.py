# -*- coding: utf-8 -*-
import scrapy
from louspider.items import CourseItem
from scrapy.selector import Selector

class LouSpider(scrapy.Spider):
    name = "mylouspider"
    # 定义允许的域名
    allowed_domains = ["shiyanlou.com"]
    # 定义进行爬取的url列表
    start_urls = ['https://www.shiyanlou.com/courses/?course_type=all&tag=all&free=yes']

    # 解析并提取Item对象
    def parse(self, response):
        items = []
        hxs = Selector(response)
        #courses = hxs.select('//ul/li')
        courses = hxs.select('//div[@class="col-md-4 course"]')
        for course in courses:
            item = CourseItem()
            item['name'] = course.xpath('a/div[3]/span[1]/text()').extract()[0].strip()
            item['learned'] = course.xpath('a/div[4]/span[1]/text()').extract()[0].strip()
            item['date'] = course.xpath('a/div[4]/span[2]/text()').extract()[0].strip()
            items.append(item)
        return items
