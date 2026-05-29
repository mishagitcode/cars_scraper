import scrapy
from scrapy_playwright.page import PageMethod
from cars_scraper.items import BmwAdvertItem


class UsedCarsBmwUkSpider(scrapy.Spider):
    name = "UsedCarsBmwUkSpider"
    allowed_domains = ["usedcars.bmw.co.uk"]

    async def start(self):
        for page in range(1, 6):
            yield scrapy.Request(
                f"https://usedcars.bmw.co.uk/result/?payment_type=cash&size=23&source=home&page={page}",
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", ".uvl-c-advert-overview"),
                    ],
                },
            )

    def parse(self, response):
        for advert in response.css(".uvl-c-advert-overview"):
            item = BmwAdvertItem()
            item["title"] = advert.css(".uvl-c-advert-overview__title::text").get("").strip()
            item["model"] = advert.css(".uvl-c-advert-overview__model::text").get("").strip()

            specs = advert.css(".uvl-c-advert-overview__specs span::text").getall()
            for i in range(1, 7):
                item[f"spec_{i}"] = specs[i - 1].strip() if i - 1 < len(specs) else ""

            yield item
