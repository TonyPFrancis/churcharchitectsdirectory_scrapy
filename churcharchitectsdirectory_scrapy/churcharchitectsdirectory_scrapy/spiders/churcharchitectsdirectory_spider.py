from scrapy import Spider, Selector, log
from scrapy.http import Request
from scrapy.log import ScrapyFileLogObserver
import requests, json, re, urllib
from time import sleep
from churcharchitectsdirectory_scrapy.items import ChurcharchitectsdirectoryScrapyItem

class ChurcharchitectsdirectorySpider(Spider):
    name = 'churcharchitectsdirectory'
    start_urls = ['http://www.churcharchitectsdirectory.com/directory.html', ]
    allowed_domains = ['churcharchitectsdirectory.com']
    TIMEZONE = ''
    BASE_URL = 'http://www.churcharchitectsdirectory.com'

    def __init__(self, name=None, **kwargs):
        ScrapyFileLogObserver(open("spider.log", 'w'), level=log.INFO).start()
        ScrapyFileLogObserver(open("spider_error.log", 'w'), level=log.ERROR).start()
        super(ChurcharchitectsdirectorySpider, self).__init__(name, **kwargs)

    def parse(self, response):
        sel = Selector(response)

        STATE_XPATH = '//blockquote/p/a/@href'

        state_urls = sel.xpath(STATE_XPATH).extract()
        if state_urls:
            for state_url in state_urls:

        else:
            return