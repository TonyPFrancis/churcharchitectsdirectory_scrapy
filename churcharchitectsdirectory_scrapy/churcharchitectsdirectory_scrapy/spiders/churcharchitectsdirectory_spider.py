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