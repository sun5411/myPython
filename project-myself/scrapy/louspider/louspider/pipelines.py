# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

class LouPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        with open('courses.txt', 'a') as file:
            date = re.findall("\d+-\d+-\d+", item['date'])[0]
            leanred = re.findall("\d+", item['learned'])[0]
            line = u"course_name: {0}, updated_at: {1}, learned_count: {2}\n".format(
                item['name'], date, leanred)
            file.write(line.encode('utf-8'))
        return item
