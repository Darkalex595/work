from email import header
from types import CoroutineType
import scrapy
from Realtor.url import BASE_URL
from Realtor.constants import type_search, URL,cookies, COUNTRY_ID, PROXIES, PROXY_PASSWORD, PROXY_USER
import json
from Realtor.utils import getUseState, getAddress, getTotalBaths, getCode, determine_city, getTypeSearch, getBuildType, transformLink
import random
import sys
from Realtor.publications_item import PublicationItem
import random
import base64

class RealtorSpider(scrapy.Spider):
    
    name = "links"
    
    
###############################################################################################
start_urls = ["https://www.nizestore.com/categoria-producto/nuevos-productos/"]




###############################################################################################
def parse(self, response):
    funkos = response.css('product-small.box').getall()
    print(funkos)