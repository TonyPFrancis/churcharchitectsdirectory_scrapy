# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class ChurcharchitectsdirectoryScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    address = Field()
    city = Field()
    state = Field()
    zip = Field()
    phone = Field()
    website = Field()
