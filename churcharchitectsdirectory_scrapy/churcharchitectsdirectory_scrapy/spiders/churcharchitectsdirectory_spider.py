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

        state_urls = filter(None, sel.xpath(STATE_XPATH).extract())
        if state_urls:
            for state_url in state_urls:
                state_url = self.BASE_URL+'/'+state_url
                yield Request(url= state_url, dont_filter=True, callback=self.parse_state)
        else:
            return

    def parse_state(self, response):
        sel = Selector(response)

        FIRM_XPATH = '//td[@rowspan="32"]/blockquote/p'

        firm_items = sel.xpath(FIRM_XPATH)
        if firm_items:
            FIRM_TEXT_XPATH = './/text()'
            for firm in firm_items:
                firm_text = firm.xpath(FIRM_TEXT_XPATH).extract()
                firm_text = [text.strip() for text in firm_text if text.strip()] if firm_text else []

        else:
            return
