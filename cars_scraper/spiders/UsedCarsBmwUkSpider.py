import scrapy
from cars_scraper.items import BmwAdvertItem


class UsedCarsBmwUkSpider(scrapy.Spider):
    name = "UsedCarsBmwUkSpider"
    allowed_domains = ["usedcars.bmw.co.uk"]

    start_urls = [
        f"https://usedcars.bmw.co.uk/result/?payment_type=cash&size=23&source=home&page={page}"
        for page in range(1, 6)
    ]

    def parse(self, response):
        for advert in response.css(".uvl-c-advert-overview"):
            item = BmwAdvertItem()
            item["title"] = advert.css(".uvl-c-advert-overview__title::text").get("").strip()
            item["model"] = advert.css(".uvl-c-advert-overview__model::text").get("").strip()

            specs = advert.css(".uvl-c-advert-overview__specs span::text").getall()
            for i in range(1, 7):
                item[f"spec_{i}"] = specs[i - 1].strip() if i - 1 < len(specs) else ""

            yield item
