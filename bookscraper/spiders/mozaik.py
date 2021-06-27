import scrapy
from datetime import datetime

NEXT_PAGE_NUM_MOZAIK=1
STOP_PAGE = ""

class MozaikSpider(scrapy.Spider):
    name = 'mozaik'
    start_urls = ["https://mozaik-knjiga.hr/kategorija/knjige/knjizevnost/"]

    def parse(self, response):
        self.get_page_to_top(response)

        for index, product in enumerate(response.xpath("//div[@class='books-container']/div[contains(@class,'book')]"),start=1):
            try:

                yield {
                'title': product.xpath(".//div[@class='title']//a").attrib['title'],
                'author': self.get_authors(product,index),
                'price': self.get_currency(product),
                'link': product.xpath(".//div[@class='title']//a").attrib['href'].split('https://mozaik-knjiga.hr/')[1],
                'page': 3,
                'date_added': datetime.utcnow()
                    }
            except:
                yield {
                    None
                }

        self.increment_page_num_mozaik()
        # if NEXT_PAGE_NUM_MOZAIK <= STOP_PAGE:
        #     yield response.follow(f"https://mozaik-knjiga.hr/kategorija/knjige/knjizevnost/page/{NEXT_PAGE_NUM_MOZAIK}/", callback=self.parse)

    @staticmethod
    def get_authors(product,index):
        authors = [s.strip() for s in product.xpath(
            f"(//div[@class='books-container']/div[contains(@class,'book')])[{index}]//div[@class='author']//a//text()").extract()]
        additional_checker = []
        for i in authors:
            if '; ' in i:
                additional_checker.append(i.split('; ')[0])
                additional_checker.append(i.split('; ')[1])
            else:
                additional_checker.append(i)
        return additional_checker # some are separated with semicolon

    @staticmethod
    def get_currency(product):
        two_prices = product.xpath(".//p[@class='price']//ins/span")
        if two_prices:
            return product.xpath(".//p[@class='price']//ins/span//text()").get().replace(u'\xa0',
                                                                                         u' ') + product.xpath(
                ".//p[@class='price']//ins/span/span//text()").get()
        else:
            return product.xpath(".//p[@class='price']/span//text()").get().replace(u'\xa0', u' ') + product.xpath(
                ".//p[@class='price']/span/span/text()").get()

    @staticmethod
    def increment_page_num_mozaik():
        global NEXT_PAGE_NUM_MOZAIK
        NEXT_PAGE_NUM_MOZAIK = NEXT_PAGE_NUM_MOZAIK+1

    @staticmethod
    def get_page_to_top(res):
        global STOP_PAGE
        if STOP_PAGE:
            return
        STOP_PAGE = float(res.xpath("//a[@aria-label='Last Page']").attrib['href'].split('/page/')[1].split('/')[0])