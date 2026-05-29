import scrapy
from scrapy_playwright.page import PageMethod
from cars_scraper.items import BmwAdvertItem, BmwSpecItem

BASE_URL = "https://usedcars.bmw.co.uk"


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
                        PageMethod("wait_for_selector",
                                   ".uvl-c-advert-overview__title a[href*='quoteref']"),
                    ],
                },
                callback=self.parse_listing,
            )

    def parse_listing(self, response):
        for advert in response.css(".uvl-c-advert-overview"):
            title = advert.css(".uvl-c-advert-overview__title a::text").get("").strip()
            model = advert.css(".uvl-c-advert-overview__model::text").get("").strip()
            href = advert.css(".uvl-c-advert-overview__title a::attr(href)").get("")
            link = response.urljoin(href)

            yield BmwAdvertItem(title=title, model=model, link=link)

            yield scrapy.Request(
                link,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector",
                                   ".uvl-c-specification-overview__value"),
                    ],
                    "link": link,
                },
                callback=self.parse_spec,
            )

    def parse_spec(self, response):
        values = response.css(".uvl-c-specification-overview__value::text").getall()
        values = [v.strip() for v in values]

        item = BmwSpecItem(link=response.meta["link"])
        for i in range(1, 9):
            item[f"spec_{i}"] = values[i - 1] if i - 1 < len(values) else ""

        yield item
