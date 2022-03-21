import scrapy


class PublicationItem(scrapy.Item):
    
    prov_id = scrapy.Field()
    id_publication_scraper = scrapy.Field()
    id_publication_provider = scrapy.Field()
    publication_code = scrapy.Field()
    project_code = scrapy.Field()
    unit_code = scrapy.Field()
    unit_name = scrapy.Field()
    country_id = scrapy.Field()
    id_admin_zone = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    description = scrapy.Field()
    publication_link = scrapy.Field()
    property_type = scrapy.Field()
    use_state = scrapy.Field()
    transaction_type = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    floors = scrapy.Field()
    garage = scrapy.Field()
    warehouse = scrapy.Field()
    furnished = scrapy.Field()
    util_area = scrapy.Field()
    terrace_area = scrapy.Field()
    total_area = scrapy.Field()
    warehouse_price = scrapy.Field()
    garage_price = scrapy.Field()
    total_price = scrapy.Field()
    currency_type = scrapy.Field()
    publication_date = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    seller_id = scrapy.Field()
    seller = scrapy.Field()
    real_state_name = scrapy.Field()
    construction_company = scrapy.Field()
    delivery_range = scrapy.Field()
    delivery_year = scrapy.Field()
    delivery_month = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    add_date = scrapy.Field()
    updated_date = scrapy.Field()
    studio = scrapy.Field()
    full_baths = scrapy.Field()
    source_total_price = scrapy.Field()
    state_list = scrapy.Field()
    build_year = scrapy.Field()
    build_year_detail = scrapy.Field()
    
    
    
    
    
    
    pass