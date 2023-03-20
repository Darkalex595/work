import scrapy
from scrapingant_client import ScrapingAntClient

class NizeScrappy(scrapy.Spider):
    name = "Nize"
    
    start_urls = [
        # "https://www.nizestore.com"
        # "https://thecomicstore.com.sv"
    ]

    def parse(self, response):
        funko = response.css("ul").getall()
        print(funko)
        # print("Hola")