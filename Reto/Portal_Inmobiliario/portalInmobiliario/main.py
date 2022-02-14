from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from portalInmobiliario.spiders.spider import PISpider
 
 
process = CrawlerProcess(get_project_settings())
process.crawl(PISpider)
process.start()