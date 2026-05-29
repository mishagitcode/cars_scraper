import scrapy


class UsedcarsbmwukspiderSpider(scrapy.Spider):
    name = "UsedCarsBmwUkSpider"
    allowed_domains = ["usedcars.bmw.co.uk"]
    start_urls = ["https://usedcars.bmw.co.uk/"]

    def parse(self, response):
        pass
