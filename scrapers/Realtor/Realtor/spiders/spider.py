from email import header
from types import CoroutineType
import scrapy
from Realtor.url import BASE_URL
from Realtor.constants import type_search, Counties, URL,cookies
import time
import json
from Realtor.utils import getUseState, getAddress, getTotalBaths, getCode, determine_city
import random

class RealtorSpider(scrapy.Spider):
    
    ### Scraper name
    name = "Realtor"
    
    def create_URL(self, State_selected, county_selected, city_selected):
        
        urls = []
        
        
        ## Lineas temporales ya que el tipo de busqueda y el estado deben ser definidos por el usuario
        search = type_search[0]
        state = "Florida"
        county_aux = "Miami"
        city_aux = "Miami Beach"
        ########
          
        cities = determine_city(state, county_aux, city_aux)
        state_code = getCode(state)
        
        if len(cities) == 1:
            urls.append(BASE_URL.format(search = search, city = cities[0], code = state_code))
        elif len(cities) > 1:
            for city in cities:
                urls.append(BASE_URL.format(search = search, city = city, code = state_code))
        else:
            print("No hay ciudades")
            quit()
        
        # for county in aux_counties:
        #     for city in county["Cities"]:
        #         urls.append(BASE_URL.format(search = search, city = city, code = county["Code"]))
        
        
            
        return urls

        
    def start_requests(self):
        header = {
        "authority": "www.realtor.com",
        "path" : "/realestateandhomes-search/Miami-Beach_FL",
        "accept-encoding" : "gzip, deflate, br",
        "cookie": random.choice(cookies)
        } 
        
        State = "Florida"
        County = "Miami"
        city = "all"  
        urls = self.create_URL(State, County, city)
        
        print("URLS:",urls)
        
        #Pagina de lista
        # urls = ["https://www.realtor.com/realestateandhomes-search/Miami-Beach_FL"]
        # urls = ["https://www.realtor.com/apartments/Miami-Beach_FL/type-single-family-home"]
        
        #Pagina de propiedad
        # urls = ["https://www.realtor.com/realestateandhomes-detail/90-Alton-Rd-Apt-2207_Miami-Beach_FL_33139_M59625-32159?property_id=5962532159&from=ab_mixed_view_card"]
        
        # print(urls)   

        for url in urls:
            # print("I'm in ", url)
            yield scrapy.Request(url=url, callback=self.parse_buy, headers=header)
   
   
###############################################################################################           
# Parse function that extracts the links in the property catalogue from 
# properties on sale and calls the specific parse function to enter 
# each property and extract the information
    def parse_buy(self, response):
        links = response.css('a.jsx-1534613990.card-anchor::attr(href)').getall()
       
        # for link in links:  
        #     # print(URL+link)
        #     yield response.follow(URL+link, callback=self.parse_buy_prop)


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
        
            
        print("Id de Propiedad:", property_id)
        print("Id de la publicacion:", list_id)
        print("Fecha de ultima publicacion:", list_date)
        print("URL:", url)
        print("Precio:", price)
        print('Camas:', beds)
        print("Studio:", Studio)
        print('Baños:', bathroom)
        print("Baños con ducha:", full_bath)
        print("Estacionamientos:", garage)
        print('Area:', area)
        print('Area total:', area_tot)
        print('Direccion:', address)
        print("Latitud:", latitude)
        print("Longitud:", longitude)
        print("Estado:", use_state)
        print("Agente:", agent)
        print("Office", office)
        print("Año de Construccion:", year_built)
        
        ### Jumps of line to distinguish between properties
        print("\n")

        # print(list_desc)







        
###############################################################################################           
# Parse function that extracts the links in the property catalogue from 
# properties on rent and calls the specific parse function to enter 
# each property and extract the information
    def parse_rent(self, response):
        links = response.css('a.card-anchor::attr(href)').getall()
       
        for link in links:  
            # print(URL+link)
            yield response.follow(URL+link, callback=self.parse_rent_prop)
        
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
        url = Data["props"]["pageProps"]["property"]["seoContent"]["metadata"]["canonical_url"]
        
        
            
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
        
        
        
        units = Data["props"]["pageProps"]["property"]["description"]["units"]
        
        if units != None:
        ### Apartamentos con unidades
              
            list_units = Data["props"]["pageProps"]["property"]["units"]

            ### Get number of bedrooms, util area, of all units
            for unit in list_units:
                Studio = False
                
                ### Get unit name
                names = unit["description"]["name"]
                if names == None:
                    print("Unit name not available")       
                
                
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
                
                print("Nombre de la unidad:", names)
                print("Numero de dormitorios:", beds_unit)
                print("Area del departamento:", areas_unit)
                print("Baños con ducha:", full_baths_unit)
                print("Baños sin ducha:", half_baths_unit)
                print("Descripcion:", descriptions)
                print("Precio:", prices)
                print("Direccion:", address)
                print("Latitud:", latitude)
                print("Longitude:", longitude)
                
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
            price = Data["props"]["pageProps"]["property"]["list_price"]
            if price != None:
                price = str(price)
            else:
                price = "N/A"
                print("Price per month not available")
            
                
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
            
            print("Dormitorios:", beds)
            print("Baños:", bathroom)
            print("Garage:", garage)
            print("Precio:", price)
            print("Direccion:", address)
            print("Area Util:", area)
            print("Area Total:", area_tot)
            print("Longitud:", longitude)
            print("Latitude:", latitude)
            print("Agente:", agent)
            print("Oficina:", office)
            print("Description:", description)
            print("Estudio:", Studio)
            
            print("\n")
            




###############################################################################################
### Parse method for properties on rent except for apartment  
    # def parse_rent_rest(self, response):
    #     print("\n")
        
    #     # transaction = "Rent"
        
    #     Data = response.xpath('//*[@id="__NEXT_DATA__"]/text()').get()
    #     Data = json.loads(Data)
        
    #     ### Get address
    #     street_name = Data["props"]["pageProps"]["property"]["location"]["address"]["street_name"]
    #     street_number = Data["props"]["pageProps"]["property"]["location"]["address"]["street_number"]
    #     postal_code = Data["props"]["pageProps"]["property"]["location"]["address"]["postal_code"]
        
    #     address = getAddress(street_name, street_number, postal_code)
        
    #     ###Get number of bedrooms
    #     beds = Data["props"]["pageProps"]["property"]["description"]["beds"]
    #     Studio = False
        
    #     if beds != None:
    #         if beds == 0:
    #             beds = 1
    #             Studio = True
    #     else:
    #         print("Number of beds not available")
        
        
    #     ###Get number of bathrooms
    #     baths = Data["props"]["pageProps"]["property"]["description"]["baths"]
    #     if baths == None:
    #         print("Number of bathrooms not available")

    #     baths_full = Data["props"]["pageProps"]["property"]["description"]["baths_full"]
    #     if baths_full == None:
    #         print("Number of full bathrooms not available")
        
    #     baths_half = Data["props"]["pageProps"]["property"]["description"]["baths_half"]
    #     if baths_half == None:
    #         print("Number of half bathrooms not available")
        
            
    #     ###Get number of parking spaces
    #     garage = Data["props"]["pageProps"]["property"]["description"]["garage"]
    #     if garage == None:
    #         print("Number of parking spaces not available")
            
            
    #     ###Get price of rent a month
    #     price = Data["props"]["pageProps"]["property"]["list_price"]
    #     if price != None:
    #         price = str(price)
    #     else:
    #         price = "N/A"
    #         print("Price per month not available")
        
            
    #     ###Get useful area and total area
    #     area = Data["props"]["pageProps"]["property"]["description"]["sqft"]
        
    #     if area != None:
    #         area = str(area)
    #     else:
    #         area = "N/A"
    #         print("Useful area not available")
        
    #     area_tot = Data["props"]["pageProps"]["property"]["description"]["lot_sqft"]
        
    #     if area != None:
    #         area = str(area_tot)
    #     else:
    #         area = "N/A"
    #         print("Total area not available")
            
            
    #     ### Get property coordinates
    #     coordinates = Data["props"]["pageProps"]["property"]["location"]["address"]["coordinate"]
        
    #     if coordinates != None:
            
    #         latitude = Data["props"]["pageProps"]["property"]["location"]["address"]["coordinate"]["lat"]
            
    #         if latitude != None:
    #             latitude = str(latitude)
    #         else:
    #             latitude = "N/A"
    #             print("Latitude not available")
            
    #         longitude = Data["props"]["pageProps"]["property"]["location"]["address"]["coordinate"]["lon"]
            
    #         if longitude != None:
    #             longitude = str(longitude)
    #         else:
    #             longitude = "N/A"
    #             print("Longitude not available")
    #     else:
    #         coordinates = "N/A"
    #         print("Coordinates not available")
            
            
    #     ### Get real state agent and office
    #     agent = Data["props"]["pageProps"]["property"]["advertisers"][0]["name"]
        
    #     if agent == None or agent == "":
    #         agent = "N/A"
    #         print("Agent not available")
        
    #     office = Data["props"]["pageProps"]["property"]["advertisers"][0]["office"]["name"]
        
    #     if office == None or office == "":
    #         office = "N/A"
    #         print("Office not available")
        
        
    #     ### Get property description
    #     description = Data["props"]["pageProps"]["property"]["description"]["text"]
        
    #     if description == None:
    #         description = "N/A"
    #         print("Description not available")
        
    #     print("Dormitorios:", beds)
    #     print("Baños:", baths)
    #     print("Garage:", garage)
    #     print("Precio:", price)
    #     print("Direccion:", address)
    #     print("Area Util:", area)
    #     print("Area Total:", area_tot)
    #     print("Longitud:", longitude)
    #     print("Latitude:", latitude)
    #     print("Agente:", agent)
    #     print("Oficina:", office)
    #     print("Description")
        
    #     print("\n")
        
        # transaction = "Rent"