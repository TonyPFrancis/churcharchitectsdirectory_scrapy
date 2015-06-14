from scrapy import Spider, Selector, log
from scrapy.http import Request
from scrapy.log import ScrapyFileLogObserver
import requests, json, re, urllib
from time import sleep
from churcharchitectsdirectory_scrapy.items import ChurcharchitectsdirectoryScrapyItem
from math import ceil

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
        response_url = response.url

        FIRM_XPATH = '//td[@rowspan="32"]/blockquote/p'

        firm_items = sel.xpath(FIRM_XPATH)
        if firm_items:
            FIRM_TEXT_XPATH = './/text()'
            for firm in firm_items:
                firm_text = firm.xpath(FIRM_TEXT_XPATH).extract()
                firm_text = [text.strip() for text in firm_text if text.strip()] if firm_text else []
                if firm_text:
                    items = self.parse_items(firm_text, response_url)
                    if items:
                        for item in items:
                            WEBSITE_XPATH = 'a[contains(text(),"%s")]/@href'%(item['name'])
                            website = firm.xpath(WEBSITE_XPATH).extract()
                            website = website[0].strip() if website else ''
                            item['website'] = website
                            try:
                                self.check_item(item)
                                yield item
                            except Exception as e:
                                with open('dropped.text', 'a+') as ur:
                                    print "*** DROPPED ITEM - %s"%(item['name'])
                                    ur.write(item['name']+' - '+response_url+'\n')
        else:
            return

    def parse_items(self, firm_text, response_url):
        items = []
        if len(firm_text)%4 == 0:
            firm_text_items = [firm_text[4*(x+0):4*(x+1)] for x in range(int(ceil(len(firm_text)/4.0)))]
            for firm_text_item in firm_text_items:
                name = firm_text_item[0].strip()
                address = firm_text_item[1].strip()
                city = ((firm_text_item[2].strip()).split(',')[0]).strip()
                state = (((firm_text_item[2].strip()).split(',')[1]).strip().split(' ')[0]).strip()
                zip = (((firm_text_item[2].strip()).split(',')[1]).strip().split(' ')[1]).strip()
                phone = firm_text_item[3].strip()
                item = ChurcharchitectsdirectoryScrapyItem(name = name,
                                                           address = address,
                                                           city = city,
                                                           state = state,
                                                           zip = zip,
                                                           phone = phone)
                items.append(item)
        else:
            with open('unrecognized.text', 'a+') as ur:
                print "*** UNRECOGNIZED ITEMS - %s"%(firm_text[0])
                ur.write(firm_text[0]+' - '+response_url+'\n')
        return items

    def check_item(self, item):
        if not item['name']:
            raise AssertionError('No name')
        if not item['address']:
            raise AssertionError('No address')
        if not item['city']:
            raise AssertionError('No city')
        if not item['state']:
            raise AssertionError('No state')
        if not item['zip']:
            raise AssertionError('No zip')
        if not item['phone']:
            raise AssertionError('No phone')
        if not item['website']:
            raise AssertionError('No website')