import scrapy


class BmwAdvertItem(scrapy.Item):
    title = scrapy.Field()
    model = scrapy.Field()
    link = scrapy.Field()


class BmwSpecItem(scrapy.Item):
    link = scrapy.Field()
    spec_1 = scrapy.Field()
    spec_2 = scrapy.Field()
    spec_3 = scrapy.Field()
    spec_4 = scrapy.Field()
    spec_5 = scrapy.Field()
    spec_6 = scrapy.Field()
    spec_7 = scrapy.Field()
    spec_8 = scrapy.Field()
