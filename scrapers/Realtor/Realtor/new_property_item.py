import scrapy


class RealtorNewPropertyItem(scrapy.Item):
    
    price = scrapy.Field()
    beds = scrapy.Field()
    bathrooms = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    
    pass