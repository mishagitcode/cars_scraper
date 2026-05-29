# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BmwAdvertItem(scrapy.Item):
    title = scrapy.Field()
    model = scrapy.Field()
    spec_1 = scrapy.Field()
    spec_2 = scrapy.Field()
    spec_3 = scrapy.Field()
    spec_4 = scrapy.Field()
    spec_5 = scrapy.Field()
    spec_6 = scrapy.Field()
