import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class MercadoLibreSpider(scrapy.Spider):
    name = "videojuegos"
    start_urls = [
        "https://listado.mercadolibre.com.sv/consolas-video-juegos/#c_id=/home/categories/element&c_category_id=MSV1144&c_uid=137ad005-f675-4089-8865-888065f148b2" 
    ]

    def parse(self, response):
        lista = response.css("ol.ui-search-layout.ui-search-layout--stack")
        
        
        if lista != None:
            for articulos in response.css("li.ui-search-layout__item"):
                precio = articulos.css("div div div.ui-search-result__content-wrapper div.ui-search-result__content-columns div.ui-search-result__content-column.ui-search-result__content-column--left div div div span.price-tag.ui-search-price__part span.price-tag-amount span.price-tag-fraction::text").get()
                titulo = articulos.css("div div div.ui-search-result__content-wrapper div.ui-search-item__group.ui-search-item__group--title a h2::text").get()
                yield{
                    "Titulo": titulo,
                    "Precio": precio
                }
                
        sig_pag = response.css("li.andes-pagination__button.andes-pagination__button--next a::attr(href)").get()
        if sig_pag:
            yield response.follow(sig_pag, callback = self.parse)