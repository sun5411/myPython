# -*- coding: utf-8 -*-

# Scrapy settings for louspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Googlebot'

SPIDER_MODULES = ['louspider.spiders']
NEWSPIDER_MODULE = 'louspider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'louspider (+http://www.yourdomain.com)'
USER_AGENT = 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

DEFAULT_REQUEST_HEADERS = {
    'Referer': 'http://www.shiyanlou.com'
}

ITEM_PIPELINES = {
    'louspider.pipelines.LouPipeline': 1
}

DOWNLOAD_DELAY = 0.5
