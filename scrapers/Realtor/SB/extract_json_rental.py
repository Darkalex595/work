from scrapingbee import ScrapingBeeClient
import limpieza
import json
import connection

def extract(link):

    client = ScrapingBeeClient(api_key='PNTT41IH5YFQ8XVTGE6JB97H35SXIXW4KWX2D5C566PXW3FTB8Y0TIQXPZ92TC8164PMZRZHE81WHXOH')
    print("Extrayendo en: " + link)

    response = client.get(link,
                                params={
                                    #   'json_response': 'True',
                                    'extract_rules':{
                                        "scripts": {
                                            "selector": "#__NEXT_DATA__",
                                            "output" : "html"
                                        }
                                    }
                                }
                                )

    print(response.status_code)



    response_code = str(response.status_code)

    if(response_code[0] != "4" and response_code[0] != "5"):
            # print(response.content)
            info = json.loads(response.content)
            info_json = info["scripts"]
            info_json = limpieza.eliminate_firstScript(info_json)
            info_json = limpieza.eliminate_lastScript(info_json)

            info_json = json.loads(info_json)
        


            ### Get property ID
            property_id = info_json["props"]["pageProps"]["property"]["property_id"]
            if property_id == None:
                print("Property ID not available")
            # print(property_id)
        
        
            
            ### Get the publication ID
            list_id = info_json["props"]["pageProps"]["property"]["listing_id"]
            if list_id == None:
                print("Listing ID is not available")
            
            
            
            ### Get last update
            last_update = info_json["props"]["pageProps"]["property"]["last_update_date"]
            if last_update == None:
                print("Last update unavailable")
            
            
            
            ### Get URL
            url = info_json["props"]["pageProps"]["jsonld"]["content"]["url"]
            
                
            ### Get address
            address = info_json["props"]["pageProps"]["property"]["location"]["address"]["line"]
            if address == None:
                s_number = info_json["props"]["pageProps"]["property"]["location"]["address"]["street_number"]
                s_direction = info_json["props"]["pageProps"]["property"]["location"]["address"]["street_direction"]
                s_name = info_json["props"]["pageProps"]["property"]["location"]["address"]["street_name"]
                s_suffix = info_json["props"]["pageProps"]["property"]["location"]["address"]["street_suffix"]
                s_post_direction = info_json["props"]["pageProps"]["property"]["location"]["address"]["street_post_direction"]
                postal_code = info_json["props"]["pageProps"]["property"]["location"]["address"]["postal_code"]
                
                address = limpieza.getAddress(s_number, s_direction, s_name, s_suffix, s_post_direction, postal_code)

            
            
            ### Get property coordinates
            longitude = None
            latitude = None
            coordinates = info_json["props"]["pageProps"]["property"]["location"]["address"]["coordinate"]    
            if coordinates != None:
                latitude = info_json["props"]["pageProps"]["property"]["location"]["address"]["coordinate"]["lat"]             
                if latitude == None:
                    print("Latitude not available")
                    
                longitude = info_json["props"]["pageProps"]["property"]["location"]["address"]["coordinate"]["lon"]    
                if longitude == None:
                    print("Longitude not available")
            else:
                print("Coordinates not available")
                    
            
            
            ### Get year built
            year_built = info_json["props"]["pageProps"]["property"]["description"]["year_built"]
            if year_built == None:
                print("Year of construction not available") 
            
            
            
            ### Get number of stories of the property
            stories = info_json["props"]["pageProps"]["property"]["description"]["stories"]
            if stories == None:
                stories = 1       
                
                
                
            ### Get real state agent and office
            agent = info_json["props"]["pageProps"]["property"]["advertisers"][0]["name"]
                
            if agent == None or agent == "":
                agent = "N/A"
                print("Agent not available")
                
            office = info_json["props"]["pageProps"]["property"]["advertisers"][0]["office"]["name"]
                
            if office == None or office == "":
                office = "N/A"
                print("Office not available")
            
            
            units = info_json["props"]["pageProps"]["property"]["description"]["units"]
            
            if units != None:
            ### Apartamentos con unidades
                
                list_units = info_json["props"]["pageProps"]["property"]["units"]

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
                            
                        baths = limpieza.getTotalBaths(full_baths_unit, half_baths_unit)
                        
                        
                        ### Get units description
                        descriptions = unit["description"]["text"]
                        if descriptions == None:
                            print("Description not available")
                            
                        
                        ### Get prices of units
                        prices = unit["list_price"]
                        

                    
        ########################################################
        ### Apartamentos sin unidades o demas tipo de propiedades            
            else:
                ### Get unit
                unit = info_json["props"]["pageProps"]["property"]["location"]["address"]["unit"]
                if unit == None:
                    print("Unit not available")
                
                
                
                ###Get number of bedrooms
                beds = info_json["props"]["pageProps"]["property"]["description"]["beds"]
                Studio = False
                
                if beds != None:
                    if beds == "Studio":
                        beds = 1
                        Studio = True
                else:
                    print("Number of beds not available")
                
                
                ###Get number of bathrooms
                bathroom = info_json["props"]["pageProps"]["property"]["description"]["baths"]
                if bathroom == None:
                    print("Number of bathrooms not included")
            
                full_bath = info_json["props"]["pageProps"]["property"]["description"]["baths_full"]
                if full_bath == None:
                    print("Number of full bathrooms not included")
                
                    
                ###Get number of parking spaces
                garage = info_json["props"]["pageProps"]["property"]["description"]["garage"]
                if garage == None:
                    print("Number of parking spaces not available")
                
                    
                ###Get price of rent a month
                price = None
                price = info_json["props"]["pageProps"]["property"]["list_price"]
                if price != None:
                    price = str(price)
                else:
                    price = "N/A"
                    print("Price per month not available")
                
                    
                ###Get useful area and total area
                area = info_json["props"]["pageProps"]["property"]["description"]["sqft"]
                if area == None:
                    print("Useful area not available")
                
                area_tot = info_json["props"]["pageProps"]["property"]["description"]["lot_sqft"]
                if area == None:
                    print("Total area not available")
                
                
                
                ### Get property description
                description = info_json["props"]["pageProps"]["property"]["description"]["text"]
                
                if description == None:
                    description = "N/A"
                    print("Description not available")
                
                
            connection.insert_into_db(property_id=property_id, list_id=list_id, stories=stories, beds=beds, studio=Studio, area=area, area_tot=area_tot, garage=garage, description=description, agent=agent, office=office, address=address, bathroom=bathroom, full_baths=full_bath, latitude=latitude, longitude=longitude, price=price, unit=unit, year_built=year_built)
         
        

    # f = open("html2.txt", 'w')
    # f.write(json_inf)
    # f.close()
