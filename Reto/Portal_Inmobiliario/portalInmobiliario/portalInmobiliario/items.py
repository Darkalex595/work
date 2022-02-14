# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PortalinmobiliarioItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nombre = scrapy.Field()
    precio = scrapy.Field()
    vendedor = scrapy.Field()
    codigo = scrapy.Field()
    supTotal = scrapy.Field()
    supUtil = scrapy.Field()
    ambientes = scrapy.Field()
    dormitorios = scrapy.Field()
    baños = scrapy.Field()
    estacionamientos = scrapy.Field()
    orientacion = scrapy.Field()
    antiguedad = scrapy.Field()
    gastos = scrapy.Field()
    latitud = scrapy.Field()
    longitud = scrapy.Field()
    # descripcion = scrapy.Field()
    pass
