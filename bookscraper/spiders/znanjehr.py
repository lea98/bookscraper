import scrapy
from datetime import datetime

NEXT_PAGE_NUM = 0


class ZnanjeSpider(scrapy.Spider):
    name = 'znanjehr'
    start_urls = ["https://znanje.hr/kategorija-proizvoda/knjizevnost/500010?pageNumber=0"]

    # ima jedna bez naslova, stavi uvjete nas sve
    def parse(self, response):
        for product in response.xpath("//div[contains(@class,'product-card')]"):
            try:
                yield {
                    'title': product.xpath(".//h3[contains(@class,'product-title')]//span/text()").get(),
                    'author': product.xpath(".//p[contains(@class,'product-author')]//a/text()").get().split(', '),
                    'price': self.get_currency(product),
                    'link': product.xpath(".//a[contains(@class,'product-thumb')]").attrib['href'][1:],
                    'page': 2,
                    'date_added': datetime.utcnow()
                }
            except:
                yield {
                    None
                }

        # next_page = response.xpath("//ul[@class='pages']//li[last()]/@*").get()  #None if has next
        # if not next_page:
        #     self.increment_page_num()
        #     yield response.follow(f"https://znanje.hr/kategorija-proizvoda/knjizevnost/500010?pageNumber={NEXT_PAGE_NUM}", callback=self.parse)

    @staticmethod
    def get_currency(product):
        amount = product.xpath(".//meta[@itemprop='price']").attrib['content']
        currency = product.xpath(".//meta[@itemprop='priceCurrency']").attrib['content']

        if currency == "HRK":
            currency = "kn"
        return amount + " " + currency

    @staticmethod
    def increment_page_num():
        global NEXT_PAGE_NUM
        NEXT_PAGE_NUM = NEXT_PAGE_NUM + 1
