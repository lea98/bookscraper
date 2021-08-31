from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from bookscraper.spiders.barnesandnoblespider import BarnesSpider
from bookscraper.spiders.ljevak import LjevakSpider
from bookscraper.spiders.mozaik import MozaikSpider
from bookscraper.spiders.znanjehr import ZnanjeSpider

print(get_project_settings())
process = CrawlerProcess(get_project_settings())

process.crawl(BarnesSpider)
process.crawl(LjevakSpider)
process.crawl(ZnanjeSpider)
process.crawl(MozaikSpider)

process.start()
