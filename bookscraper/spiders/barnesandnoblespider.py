import scrapy
from datetime import datetime
class BarnesSpider(scrapy.Spider):
    name = 'barnesandnoble'
    start_urls = ["https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=3&page=1"]

    def parse(self, response):
        for index, product in enumerate(response.xpath("//div[@class='row topX-row']"),start=1):
            try:
                yield {
                'title': product.xpath(".//h3[@class='product-info-title']//a/text()").get(),
                'author': [s.strip() for s in product.xpath(f"(//div[@class='product-info-view'])[{index}]//div[contains(@class,'product-shelf-author contributors')]/descendant::a//text()").extract()],
                'price': product.xpath(".//a[@class=' current link']/text()").get().split(';jsessionid')[0],
                'link': self.form_link('https://www.barnesandnoble.com'+product.xpath(".//h3[@class='product-info-title']//a").attrib['href']),
                'page': 1,
                'date_added': datetime.utcnow()
                    }
            except:
                yield {
                    None
                }

        # FOR LOCAL TESTING, DON'T FILL PROD DB WITH MUCH DATA
        # next_page = response.xpath("//a[@class='next-button' and not(@aria-disabled)]")
        # if next_page:
        #     next_page = response.xpath("//a[@class='next-button' and not(@aria-disabled)]").attrib['href']
        #     yield response.follow(next_page, callback=self.parse)


    @staticmethod
    def form_link(link):
        if ';jsessionid' in link:
            return (link.split(';jsessionid')[0] + '?ean' + link.split('?ean')[1]).split('https://www.barnesandnoble.com/')[1]
        else:
            return link.split('https://www.barnesandnoble.com/')[1]


