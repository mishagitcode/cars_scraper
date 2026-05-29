import scrapy


class BmwAdvertItem(scrapy.Item):
    name = scrapy.Field()
    model = scrapy.Field()
    link = scrapy.Field()


class BmwSpecItem(scrapy.Item):
    link = scrapy.Field()
    mileage = scrapy.Field()
    registered = scrapy.Field()
    engine = scrapy.Field()
    range = scrapy.Field()
    exterior = scrapy.Field()
    fuel = scrapy.Field()
    transmission = scrapy.Field()
    registration = scrapy.Field()
    upholstery = scrapy.Field()
