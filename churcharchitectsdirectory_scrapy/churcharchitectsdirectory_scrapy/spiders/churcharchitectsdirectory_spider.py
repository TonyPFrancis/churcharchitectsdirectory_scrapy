from scrapy import Spider, Selector, log
from scrapy.http import Request
from scrapy.log import ScrapyFileLogObserver
import requests, json, re, urllib
from time import sleep
from churcharchitectsdirectory_scrapy.items import ChurcharchitectsdirectoryScrapyItem

class ChurcharchitectsdirectorySpider(Spider):
    name = 'churcharchitectsdirectory'
    