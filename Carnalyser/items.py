# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Ads(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    year_manufactory = scrapy.Field()
    year_model = scrapy.Field()
    cylinder = scrapy.Field()
    engine = scrapy.Field()
    doors = scrapy.Field()
    fuel = scrapy.Field()
    km = scrapy.Field()
    cambio = scrapy.Field()
    desc = scrapy.Field()
    
    pass
