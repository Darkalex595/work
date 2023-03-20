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
    
    ### Scraper name
    name = "Realtor"
    #################
    
    properties = []
    referers = []
    actual_link = ""
    
#############################################################################################   
### Function that creates URL depending of the input of the user
    def create_URL(self):
        
        ### Array where created URLs will be stored
        urls = []
        
        ## Variables for testing purposes
        # search_aux = "rental"
        # state = "Florida"
        # county_aux = "Miami"
        # city_aux = "Miami-Beach"
        # prop_type_aux = "apartment"
        # self.type = "apartment"
        # self.search = "rental"
        ###########################
        
        ### Input of the user to specify what the spider will search
        search_aux = self.search
        state = self.state
        county_aux = self.county
        city_aux = self.city
        prop_type_aux = self.type
        ########
        
        
        search_2 =  getTypeSearch(search_aux) 
        cities = determine_city(state, county_aux, city_aux)
        state_code = getCode(state)
        self.prop_type = getBuildType(prop_type_aux)
        
        if len(cities) == 1:
            urls.append(BASE_URL.format(search = search_2, city = cities[0], code = state_code, type = self.prop_type))
        elif len(cities) > 1:
            for city in cities:
                urls.append(BASE_URL.format(search = search_2, city = city, code = state_code, type=self.prop_type))
        else:
            sys.exit("City not available")
                   
        return urls

#############################################################################################     
### Function that starts the requests based on the list of URLs created
        
    def start_requests(self):
        
        # proxy_user_pass = PROXY_USER + ":" + PROXY_PASSWORD
        # encoded_user_pass = base64.b64encode(proxy_user_pass.encode())
        # self.proxy_authorization = 'Basic ' + encoded_user_pass.decode()
        
        self.header = {
        "authority": "www.realtor.com",
        "path" : "/realestateandhomes-search/Miami-Beach_FL",
        "scheme": "https",
        "accept-encoding": "gzip, deflate, br",
        "accept-language":"es-ES,es;q=0.9",
        "referer": "https://www.realtor.com/",
        "cookie": random.choice(cookies),
        
        # 'Proxy-Authorization': self.proxy_authorization
        } 
        
        
        urls = self.create_URL()
        
        
        print("URLS:",urls)
        
        if self.search == "rental":
            for url in urls:
                self.header["path"] = url
                # print("I'm in ", url)
                self.actual_link = url
                url ="http://api.scraperapi.com?api_key=ba844affc206c6e87fc7b475670e8235&url=" + url
                yield scrapy.Request(url=url, callback=self.parse_rent, headers=self.header)
                
                
                
                
        
        elif self.search == "buy":
            for url in urls:
                self.header["path"] = url
                # print("I'm in ", url)
                self.actual_link = url
                url ="http://api.scraperapi.com?api_key=ba844affc206c6e87fc7b475670e8235&url=" + url
                yield scrapy.Request(url=url, callback=self.parse_buy, headers=self.header)

                
                
        else:
            print("Type of search not available")
   


###############################################################################################           
# Parse function that extracts the links in the property catalogue from 
# properties on sale and calls the specific parse function to enter 
# each property and extract the information
    def parse_buy(self, response):
        links = response.css('a.jsx-1534613990.card-anchor::attr(href)').getall()
       
        self.referers.append(self.actual_link)
       
        for link in links:  
            # print("Link:", URL+link)
            # self.header["cookie"] = random.choice(cookies)
            # yield scrapy.Request(url= URL+link, callback=self.parse_buy_prop, headers=self.header)
            self.properties.append(URL+link)
        
        button_array = response.css('a.item.btn::attr(href)').getall()
        
            
        tam_array = len(button_array)
        next_link = button_array[tam_array-1]
        
        # print("Tamaño del array:", tam_array)
        
        if next_link != "":
            next_link = transformLink(next_link, self.prop_type)
            self.header["cookie"] = random.choice(cookies)
            self.header["referer"] = self.actual_link
            self.actual_link = URL+next_link
            yield scrapy.Request(URL+next_link, callback=self.parse_buy, headers=self.header)
        else:
            print("End of catalogue")
            
        
            # Cont = 0
            # ref = 0
                
            # for props in self.properties:
            #     self.header["cookie"] = random.choice(cookies)
            #     if (Cont == 44):
            #         Cont = 0
            #         ref = ref + 1
                            
            #     self.header["referer"] = self.referers[ref]
                        
            #     yield scrapy.Request(url= props, callback=self.parse_buy_prop, headers=self.header)
                        
            #     Cont = Cont + 1
                

###############################################################################################
### Parse method for properties on sale
    def parse_buy_prop(self, response):
        
        ### Jumps of line to distinguish between properties
        print("\n")
        
        # transaction = "Buy"
        
        ### Get JSON with the information about the property for sale as a string and converts it to JSON
        data_aux = response.xpath('//*[@id="__NEXT_DATA__"]/text()').get()
        data = json.loads(data_aux)
        
         
        ### Get property ID
        property_id = data["props"]["pageProps"]["property"]["property_id"]
        if property_id == None: 
            print("Property ID not available")
             
        
        
        ### Get the publication ID
        list_id = data["props"]["pageProps"]["property"]["listing_id"]
        if list_id == None:
            print("Listing ID is not available")
        
        
        
        ### Get listing date
        list_date_aux = data["props"]["pageProps"]["property"]["property_history"]
        if list_date_aux != None:
            list_date = list_date_aux[0]["date"]
            
            if list_date == None:
                print("Last listing date not available")
            
        else:
            print("History of the property not available")
        
        
         
        ### Get URL
        url = data["props"]["pageProps"]["seoContent"]["zoho"]["meta_data"]["canonical_url"]
        
        
        
        ### Get latitude and longitude
        longitude = None
        latitude = None
        Coordinates = data["props"]["pageProps"]["property"]["location"]["address"]["coordinate"]
        
        if Coordinates != None:
            latitude = Coordinates["lat"]
            if latitude == None:
                print("Latitude not available")
                
            longitude = Coordinates["lon"]
            if longitude == None:
                print("Longitude not available")
        else:
            print("Coordinates are not available")
        
        
        
        ### Gets an array of details about the property
        details = data["props"]["pageProps"]["property"]["details"]

  
        
        ### Gets use state (New/Resale) and year it was built
        use_state = getUseState(details)
        
        year_built = data["props"]["pageProps"]["property"]["description"]["year_built"]
        if year_built == None:
            print("Year of construction not available")
        
        
        
        ### Gets price using css and if not found it uses the json information
        price = data["props"]["pageProps"]["property"]["list_price"]
        if price == None:
            print("Total price not available")
        
        
        
        ### Get number of stories of the property
        stories = data["props"]["pageProps"]["property"]["description"]["stories"]
        if stories == None:
            stories = 1
        
        
        
        ### Gets number of bedrooms or if it is a studio
        Studio = False
        beds = data["props"]["pageProps"]["property"]["description"]["beds"]
                
        if beds != None:
            if beds <= 0:
                beds = 1
                Studio = True
        else:
            print("Number of bedrooms not included")


                
        ### Gets number of bathrooms
        bathroom = data["props"]["pageProps"]["property"]["description"]["baths"]
        if bathroom == None:
            print("Number of bathrooms not included")
        
        full_bath = data["props"]["pageProps"]["property"]["description"]["baths_full"]
        if full_bath == None:
            print("Number of full bathrooms not included")

        
        
        ### Gets useful area
        # areaAux = response.css('li.rui__sc-147u46e-0.bcVtCB span')
        # area = areaAux[0].css('span::text').get()
        area = data["props"]["pageProps"]["property"]["description"]["sqft"]     
        if area == None:
            print("Area not found")
        
        
        
        ### Gets total area
        area_tot = data["props"]["pageProps"]["property"]["description"]["lot_sqft"]
        if area_tot == None:
            print("Total area not available")
       
       
        
        ### Gets address
        address = data["props"]["pageProps"]["property"]["location"]["address"]["line"]
        if address == None:
            s_number = data["props"]["pageProps"]["property"]["location"]["address"]["street_number"]
            s_direction = data["props"]["pageProps"]["property"]["location"]["address"]["street_direction"]
            s_name = data["props"]["pageProps"]["property"]["location"]["address"]["street_name"]
            s_suffix = data["props"]["pageProps"]["property"]["location"]["address"]["street_suffix"]
            s_post_direction = data["props"]["pageProps"]["property"]["location"]["address"]["street_post_direction"]
            postal_code = data["props"]["pageProps"]["property"]["location"]["address"]["postal_code"]
            
            address = getAddress(s_number, s_direction, s_name, s_suffix, s_post_direction, postal_code)
        
        
        
        ### Nombre de la unidad
        unit = data["props"]["pageProps"]["property"]["location"]["address"]["unit"]
        if unit == None:
            print("Unit name not available")
        
        
        
        ### Get number of cars which the garage allows or if it doesn't has a garage
        garage = data["props"]["pageProps"]["property"]["description"]["garage"]         
        if garage == None:
            print("No garage")
            
 
 
        ### Get description about the property
        description = data["props"]["pageProps"]["property"]["description"]["text"]
        if description == None:
            description = "N/A"
            print("No description added")
        
        
            
        ### Get agent and office of real state
        rs_info = data["props"]["pageProps"]["property"]["consumer_advertisers"]
        for info in rs_info:
            if info["type"] == "Agent":
                agent = info["name"]
                agent_id = info["agent_id"]
                agent_phone = info["phone"]
                
            elif info["type"] == "Office":
                office = info["name"]
                office_id = info["broker_id"]
                office_phone = info["phone"]
                
                
        if agent == None:
            agent = "N/A"
            print("Real State agent not found")
        
        if office == None:
            office = "N/A"
            print("Real State office not found")        
        
            
        # print("Id de Propiedad:", property_id)
        # print("Id de la publicacion:", list_id)
        # print("Fecha de ultima publicacion:", list_date)
        # print("URL:", url)
        # print("Precio:", price)
        # print('Camas:', beds)
        # print("Studio:", Studio)
        # print('Baños:', bathroom)
        # print("Baños con ducha:", full_bath)
        # print("Estacionamientos:", garage)
        # print('Area:', area)
        # print('Area total:', area_tot)
        # print('Direccion:', address)
        # print("Latitud:", latitude)
        # print("Longitud:", longitude)
        # print("Estado:", use_state)
        # print("Agente:", agent)
        # print("Office", office)
        # print("Año de Construccion:", year_built)
        
        
        item = PublicationItem(prov_id= None, id_publication_scraper= None, id_publication_provider= None, publication_code= list_id, project_code= property_id, unit_code= None, unit_name= unit, country_id= COUNTRY_ID, id_admin_zone= None, name= None, address= address, description= description, publication_link= url, property_type= self.type, use_state= use_state, transaction_type= self.search, bedrooms= beds, bathrooms= bathroom, floors= stories, garage= garage, warehouse= None, furnished= None, util_area= area, terrace_area= None, total_area= area_tot, warehouse_price= None, garage_price= None, total_price= price, currency_type= "USD", publication_date= None, email= None, phone= agent_phone, seller_id= agent_id, seller= agent, real_state_name= office, construction_company= None, delivery_range= None, delivery_year= None, delivery_month= None, latitude= latitude, longitude= longitude, add_date= list_date, updated_date= None, studio= Studio, full_baths= full_bath, source_total_price= None, state_list= None, build_year= year_built, build_year_detail=None)
        
        yield item
        
        ### Jumps of line to distinguish between properties
        # print("\n")

        # print(list_desc)







        
###############################################################################################           
# Parse function that extracts the links in the property catalogue from 
# properties on rent and calls the specific parse function to enter 
# each property and extract the information

    def parse_rent(self, response):
        
        
        links = response.css('a.card-anchor::attr(href)').getall()
        self.header["referer"] = self.actual_link
       
        for link in links:  
            print(URL+link)
            self.header["cookie"] = random.choice(cookies)
            # yield scrapy.Request(url=URL+link, callback=self.parse_rent_prop, headers= self.header)
            self.properties.append(URL+link)
            
        button_array = response.css('a.item.btn::attr(href)').getall()
        
        
        # tam_array = len(button_array)
        # next_link = button_array[tam_array-1]
        
        # if next_link != "":
        #     next_link = transformLink(next_link, self.prop_type)
        #     self.header["cookie"] = random.choice(cookies)
        #     self.actual_link =  URL+next_link
        #     # mod_url = "http://api.scraperapi.com?api_key=ba844affc206c6e87fc7b475670e8235&url="+URL+next_link
        #     yield scrapy.Request(URL+next_link, callback=self.parse_rent, headers= self.header)
        # else:
        #     print("End of catalogue")
             
            
            
            # print("\n")
            # print("Empieza el scraping de propiedades")
            # print("\n")
            # Cont = 0
            # ref = 0
                
            # for props in self.properties:
            #     self.header["cookie"] = random.choice(cookies)
            #     if (Cont == 44):
            #         Cont = 0
            #         ref = ref + 1
                            
            #     # self.header["referer"] = self.referers[ref]
                        
            #     yield scrapy.Request(url=props, callback=self.parse_rent_prop, headers= self.header)
                        
            #     Cont = Cont + 1
        
###############################################################################################
### Parse method for properties on rent for apartments 
    def parse_rent_prop(self, response):
        print("\n")
        
        Data = response.xpath('//*[@id="__NEXT_DATA__"]/text()').get()
        Data = json.loads(Data)
        
        ### Get property ID
        property_id = Data["props"]["pageProps"]["property"]["property_id"]
        if property_id == None:
            print("Property ID not available")
        # print(property_id)
        
        
        
        ### Get the publication ID
        list_id = Data["props"]["pageProps"]["property"]["listing_id"]
        if list_id == None:
            print("Listing ID is not available")
        
        
        
        ### Get last update
        last_update = Data["props"]["pageProps"]["property"]["last_update_date"]
        if last_update == None:
            print("Last update unavailable")
        
        
        
        ### Get URL
        url = Data["props"]["pageProps"]["jsonld"]["content"]["url"]
        
        
        url = URL + url
        
        
            
        ### Get address
        address = Data["props"]["pageProps"]["property"]["location"]["address"]["line"]
        if address == None:
            s_number = Data["props"]["pageProps"]["property"]["location"]["address"]["street_number"]
            s_direction = Data["props"]["pageProps"]["property"]["location"]["address"]["street_direction"]
            s_name = Data["props"]["pageProps"]["property"]["location"]["address"]["street_name"]
            s_suffix = Data["props"]["pageProps"]["property"]["location"]["address"]["street_suffix"]
            s_post_direction = Data["props"]["pageProps"]["property"]["location"]["address"]["street_post_direction"]
            postal_code = Data["props"]["pageProps"]["property"]["location"]["address"]["postal_code"]
            
            address = getAddress(s_number, s_direction, s_name, s_suffix, s_post_direction, postal_code)

        
        
        ### Get property coordinates
        longitude = None
        latitude = None
        coordinates = Data["props"]["pageProps"]["property"]["location"]["address"]["coordinate"]    
        if coordinates != None:
            latitude = Data["props"]["pageProps"]["property"]["location"]["address"]["coordinate"]["lat"]             
            if latitude == None:
                print("Latitude not available")
                
            longitude = Data["props"]["pageProps"]["property"]["location"]["address"]["coordinate"]["lon"]    
            if longitude == None:
                print("Longitude not available")
        else:
            print("Coordinates not available")
                
           
           
        ### Get year built
        year_built = Data["props"]["pageProps"]["property"]["description"]["year_built"]
        if year_built == None:
            print("Year of construction not available") 
        
        
        
        ### Get number of stories of the property
        stories = Data["props"]["pageProps"]["property"]["description"]["stories"]
        if stories == None:
            stories = 1       
            
            
            
        ### Get real state agent and office
        agent = Data["props"]["pageProps"]["property"]["advertisers"][0]["name"]
            
        if agent == None or agent == "":
            agent = "N/A"
            print("Agent not available")
            
        office = Data["props"]["pageProps"]["property"]["advertisers"][0]["office"]["name"]
            
        if office == None or office == "":
            office = "N/A"
            print("Office not available")
        
        
        ### Ultima actualizacion
        update = Data["props"]["pageProps"]["property"]["last_update_date"]
        if update == None:
            print("Last update date not available")
        
        
        units = Data["props"]["pageProps"]["property"]["description"]["units"]
        
        if units != None:
        ### Apartamentos con unidades
              
            list_units = Data["props"]["pageProps"]["property"]["units"]

            ### Get number of bedrooms, util area, of all units
            if list_units != None:
                for unit in list_units:
                    Studio = False
                    
                    ### Get unit name
                    names = unit["description"]["name"]
                    if names == None:
                        print("Unit name not available")       
                    
                    
                    ### Get unit id
                    unit_id = unit["plan_id"]
                    if unit_id == None:
                        print("Unit id not available")
                    
                    ### Get number of bedrooms
                    beds_unit = unit["description"]["beds"]
                    if beds_unit == None:
                        print("Number of bedrooms not available")
                    else:
                        if beds_unit <= 0:
                            beds_unit = 1
                            Studio = True          
                    
                    
                    ### Get area of the unit
                    areas_unit = unit["description"]["sqft"]
                    if areas_unit == None:
                        print("Area of unit not available")
                    
                    
                    ### Get bathrooms
                    full_baths_unit = unit["description"]["baths"]
                    if full_baths_unit == None:
                        print("Full bathrooms not available")
                    
                    half_baths_unit = unit["description"]["baths_half"]
                    if half_baths_unit == None:
                        print("Half bathrooms not available")
                        
                    baths = getTotalBaths(full_baths_unit, half_baths_unit)
                    
                    
                    ### Get units description
                    descriptions = unit["description"]["text"]
                    if descriptions == None:
                        print("Description not available")
                        
                    
                    ### Get prices of units
                    prices = unit["list_price"]
                    
                    # print("Nombre de la unidad:", names)
                    # print("Numero de dormitorios:", beds_unit)
                    # print("Area del departamento:", areas_unit)
                    # print("Baños con ducha:", full_baths_unit)
                    # print("Baños sin ducha:", half_baths_unit)
                    # print("Descripcion:", descriptions)
                    # print("Precio:", prices)
                    # print("Direccion:", address)
                    # print("Latitud:", latitude)
                    # print("Longitude:", longitude)
                    item = PublicationItem(prov_id= None, id_publication_scraper= None, id_publication_provider= None, publication_code= list_id, project_code= property_id, unit_code= unit_id, unit_name= names, country_id= COUNTRY_ID, id_admin_zone= None, name= None, address= address, description= descriptions, publication_link= url, property_type= self.type, use_state= None, transaction_type= self.search, bedrooms= beds_unit, bathrooms= baths, floors= stories, garage= None, warehouse= None, furnished= None, util_area= areas_unit, terrace_area= None, total_area= None, warehouse_price= None, garage_price= None, total_price= prices, currency_type= "USD", publication_date= None, email= None, phone= None, seller_id= None, seller= agent, real_state_name= office, construction_company= None, delivery_range= None, delivery_year= None, delivery_month= None, latitude= latitude, longitude= longitude, add_date= None, updated_date= update, studio= Studio, full_baths= full_baths_unit, source_total_price= None, state_list= None, build_year= year_built, build_year_detail=None)
            
                    yield item
                else:
                    print("List of units not available")
                
    ########################################################
    ### Apartamentos sin unidades o demas tipo de propiedades            
        else:
            ### Get unit
            unit = Data["props"]["pageProps"]["property"]["location"]["address"]["unit"]
            if unit == None:
                print("Unit not available")
            
            
            
            ###Get number of bedrooms
            beds = Data["props"]["pageProps"]["property"]["description"]["beds"]
            Studio = False
            
            if beds != None:
                if beds == "Studio":
                    beds = 1
                    Studio = True
            else:
                print("Number of beds not available")
            
            
            ###Get number of bathrooms
            bathroom = Data["props"]["pageProps"]["property"]["description"]["baths"]
            if bathroom == None:
                print("Number of bathrooms not included")
        
            full_bath = Data["props"]["pageProps"]["property"]["description"]["baths_full"]
            if full_bath == None:
                print("Number of full bathrooms not included")
            
                
            ###Get number of parking spaces
            garage = Data["props"]["pageProps"]["property"]["description"]["garage"]
            if garage == None:
                print("Number of parking spaces not available")
            
                
            ###Get price of rent a month
            price = None
            # price = Data["props"]["pageProps"]["property"]["list_price"]
            # if price != None:
            #     price = str(price)
            # else:
            #     price = "N/A"
            #     print("Price per month not available")
            
                
            ###Get useful area and total area
            area = Data["props"]["pageProps"]["property"]["description"]["sqft"]
            if area == None:
                print("Useful area not available")
            
            area_tot = Data["props"]["pageProps"]["property"]["description"]["lot_sqft"]
            if area == None:
                print("Total area not available")
            
            
            ### Get property description
            description = Data["props"]["pageProps"]["property"]["description"]["text"]
            
            if description == None:
                description = "N/A"
                print("Description not available")
            
            # print("Dormitorios:", beds)
            # print("Baños:", bathroom)
            # print("Garage:", garage)
            # print("Precio:", price)
            # print("Direccion:", address)
            # print("Area Util:", area)
            # print("Area Total:", area_tot)
            # print("Longitud:", longitude)
            # print("Latitude:", latitude)
            # print("Agente:", agent)
            # print("Oficina:", office)
            # print("Description:", description)
            # print("Estudio:", Studio)
            
            # print("\n")
            
            item = PublicationItem(prov_id= None, id_publication_scraper= None, id_publication_provider= None, publication_code= list_id, project_code= property_id, unit_code= None, unit_name= unit, country_id= COUNTRY_ID, id_admin_zone= None, name= None, address= address, description= description, publication_link= url, property_type= self.type, use_state= None, transaction_type= self.search, bedrooms= beds, bathrooms= bathroom, floors= stories, garage= garage, warehouse= None, furnished= None, util_area= area, terrace_area= None, total_area= area_tot, warehouse_price= None, garage_price= None, total_price= price, currency_type= "USD", publication_date= None, email= None, phone= None, seller_id= None, seller= agent, real_state_name= office, construction_company= None, delivery_range= None, delivery_year= None, delivery_month= None, latitude= latitude, longitude= longitude, add_date= None, updated_date= update, studio= Studio, full_baths= full_bath, source_total_price= None, state_list= None, build_year= year_built, build_year_detail=None)
        
            yield item
            
            