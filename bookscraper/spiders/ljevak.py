import scrapy
from datetime import datetime


class LjevakSpider(scrapy.Spider):
    name = "ljevak"
    start_urls = ["https://www.ljevak.hr/18-knjizevnost"]  # novo

    def parse(self, response):

        for product in response.xpath("//div[@class='item-inner']"):
            try:
                yield {
                    "title": product.xpath(
                        ".//a[contains(@class,'info_product_wl')]"
                    ).attrib["data-name-product"],
                    "author": self.get_author(product),
                    "price": product.xpath(
                        ".//div[@class='product-description']//span[@class='price']/text()"
                    )
                    .get()
                    .replace(u"\xa0", u" ")
                    .replace("HRK", "kn"),
                    "link": product.xpath(".//span[@class='cover_image']//a")
                    .attrib["href"]
                    .split("https://www.ljevak.hr/")[1],
                    "page": 4,
                    "date_added": datetime.utcnow(),
                }
            except:
                yield {
                    "title": "",
                    "author": "",
                    "price": "",
                    "link": "",
                    "page": "",
                    "date_added": "",
                }

        # FOR LOCAL TESTING, DON'T FILL PROD DB WITH MUCH DATA
        next_page = response.xpath("//a[@class='next ']")
        if next_page:
            next_page = response.xpath("//a[@class='next ']").attrib["href"]
            yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def get_author(product):
        author = product.xpath(
            ".//div[@class='product-description']//div[@class='author']//span//a"
        )
        if author:
            return author.attrib["title"].split(", ")
        else:
            return None
