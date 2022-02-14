from typing import Pattern
import scrapy
from scrapy import item
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from portalInmobiliario.items import PortalinmobiliarioItem
from scrapy.crawler import CrawlerProcess
import json
import re
from portalInmobiliario.constants import BASE_URL, comunas, MAX_PAGS



def createString(arr):
    Descripcion = ""
    for j in arr:
            Descripcion = Descripcion + " " + j
    
    return Descripcion

class PISpider(scrapy.Spider):
    name = "PI"
    page = 0
    
    start_urls = []

    for i in comunas:
        url = BASE_URL.format(comuna = i)
        start_urls.append(url)
        
    # start_urls = ["https://www.portalinmobiliario.com/venta/departamento/propiedades-usadas/santiago-metropolitana"]
    
    def parse(self, response):
        
        
        lista = response.xpath('//*[@id="root-app"]/div/div/section/ol').get()
        
        if lista:
            for propiedad in response.css("li.ui-search-layout__item"):
                link = propiedad.css("div div a::attr(href)").get()
                yield scrapy.Request(link, callback=self.parseProp)
                
        sig = response.css("li.andes-pagination__button.andes-pagination__button--next a::attr(href)").get()
        Act = self.page
        if sig:
            if(Act < MAX_PAGS):
                self.page = Act + 1
                yield response.follow(sig, callback=self.parse)
                

    def parseProp(self, response):
        pattern = re.compile(r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\})\s*;\s*\n')
        data = response.xpath("/html/body/script[2]/text()").re_first(pattern)
        
        if data:
            json_data = json.loads(data)
            longitud = json_data["initialState"]["components"]["content_left"][0]["map_info"]["location"]["latitude"]
            latitud = json_data["initialState"]["components"]["content_left"][0]["map_info"]["location"]["longitude"]
        else:
            longitud = "N/A"
            latitud = "N/A"
            
        Nombre = response.css("h1.ui-pdp-title::text").get()
        Precio = response.xpath('//*[@id="root-app"]/div/div[3]/div/div[1]/div[1]/div/div[2]/div/div[1]/span/span[2]/span[2]/text()').get()   
        Vendedor = response.xpath('//*[@id="seller_profile"]/div/div[2]/div/h3/text()').get()
        if(Vendedor == None):
            Vendedor = response.xpath('//*[@id="seller_profile"]/div/div/div/h3/text()').get()
            
        Codigo = response.xpath('//*[@id="seller_profile"]/ul[2]/div/div/p/text()').get()
        if Codigo == None:
            Codigo = "N/A"
        
        
        Caracteristicas = response.css("th.andes-table__header.andes-table__header--left.ui-pdp-specs__table__column.ui-pdp-specs__table__column-title::text").getall()
        Valores = response.css("td.andes-table__column.andes-table__column--left.ui-pdp-specs__table__column span.andes-table__column--value::text").getall()
        # Aux = response.xpath('//*[@id="root-app"]/div/div[3]/div/div[2]/div[2]/div[4]/div/p/text()').getall()
        
        
        # Descripcion = createString(Aux)

        
        SuperficieTotal = "N/A"
        SuperficieUtil = "N/A"
        Dormitorios = "N/A"
        Baños = "N/A"
        Orientacion = "N/A"
        Antiguedad = "N/A"
        Gastos = "N/A"
        Estacionamientos = "N/A"
        Ambientes = "N/A"
        
        Cont = 0
        for i in Caracteristicas:
            if i == "Superficie total":
                SuperficieTotal = Valores[Cont]
            if i == "Superficie útil":
                SuperficieUtil = Valores[Cont]
            if i == "Ambientes":
                Ambientes = Valores[Cont]
            if i == "Dormitorios":
                Dormitorios = Valores[Cont]
            if i == "Baños":
                Baños = Valores[Cont]
            if i == "Estacionamientos":
                Estacionamientos = Valores[Cont]
            if i == "Orientacion":
                Orientacion = Valores[Cont]
            if i == "Antigüedad":
                Antiguedad = Valores[Cont]
            if i == "Gastos comunes":
                Gastos = Valores[Cont]            
            Cont = Cont + 1
            
        
        itemPropiedad = PortalinmobiliarioItem(nombre = Nombre, precio = Precio, vendedor = Vendedor, codigo = Codigo, supTotal = SuperficieTotal, supUtil = SuperficieUtil, ambientes = Ambientes, dormitorios = Dormitorios, baños = Baños, estacionamientos = Estacionamientos, orientacion = Orientacion, antiguedad = Antiguedad, gastos = Gastos, latitud = latitud, longitud = longitud)
        
        yield itemPropiedad

            
        
        # yield{
        #     'Nombre': Nombre,
        #     'Precio': Precio,
        #     'Vendedor': Vendedor,
        #     'Codigo': Codigo,
        #     'Superficie Total': SuperficieTotal,
        #     'Superficie Util': SuperficieUtil,
        #     'Ambientes': Ambientes,
        #     'Dormitorios': Dormitorios,
        #     'Baños': Baños,
        #     'Estacionamientos': Estacionamientos,
        #     'Orientacion': Orientacion,
        #     'Antigüedad': Antiguedad,
        #     "Gastos Comunes": Gastos,
        #     "Descripcion" : Descripcion
        # }
    
