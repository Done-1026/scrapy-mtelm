# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MtelmCatItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()

class MtelmSortItem(scrapy.Item):
    sort = scrapy.Field()

class MtelmFbItem(scrapy.Item):
    bar = scrapy.Field()

class FoodItem(scrapy.Item):
    name = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    month_sales = scrapy.Field()
    
