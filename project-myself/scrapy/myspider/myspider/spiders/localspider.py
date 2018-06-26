#coding=utf-8
import scrapy

from myspider.items import CourseItem
from scrapy.selector import Selector

class MySpider(scrapy.Spider):
    name = "myspider"
    #define the allowed domain
    allowed_domains = ["shiyanlou.com"]
    start_urls = ['https://www.shiyanlou.com/courses/?course_type=all&tag=all&free=yes']

    def parse(self,response):
        items = []
        hxs = Selector(response)
        courses = hxs.select('//div[@class="col-md-4 course"]')
        for course in courses:
            item = CourseItem()
            item['name'] = course.xpath('a/div[3]/span[1]/text()').extract()[0].strip()
            item['learned'] = course.xpath('a/div[4]/span[1]/text()').extract()[0].strip()
            item['date'] = course.xpath('a/div[4]/span[2]/text()').extract()[0].strip()
            items.append(item)
        return items
