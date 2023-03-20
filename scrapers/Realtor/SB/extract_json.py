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


            # print(response.content)

    print(response.status_code)
            # print(response.content)
            # info = limpieza.eliminate_b(str(response.content))
            # info = limpieza.eliminate_lastChar(info)
            # info = limpieza.eliminate_backslash(info)
            # info = limpieza.eliminate_firstScript(info)
            # info = limpieza.eliminate_lastScript(info)
            # info = limpieza.eliminate_outer(info)
            # info = limpieza.eliminate_lastChar(info)
            # info = limpieza.eliminate_lastChar(info)


    response_code = str(response.status_code)

    if(response_code[0] != "4" and response_code[0] != "5"):
            # print(response.content)
            info = json.loads(response.content)
            info_json = info["scripts"]
            info_json = limpieza.eliminate_firstScript(info_json)
            info_json = limpieza.eliminate_lastScript(info_json)

            info_json = json.loads(info_json)
        


            ### Get property ID
            property_id = info_json["props"]["pageProps"]["initialProps"]["property"]["property_id"]
            if property_id == None: 
                    print("Property ID not available")
            else:
                    print("Property ID: "+property_id)

            ### Get the publication ID
            list_id = info_json["props"]["pageProps"]["initialProps"]["property"]["listing_id"]
            if list_id == None:
                    print("Listing ID is not available")
            else:
                    print("List ID: "+list_id)
                    
                    
            ### Get listing date
            list_date_aux = info_json["props"]["pageProps"]["initialProps"]["property"]["property_history"]
            if list_date_aux != None:
                list_date = list_date_aux[0]["date"]
                
                if list_date == None:
                    print("Last listing date not available")
                
            else:
                list_date = None
                print("History of the property not available")
                    
                    
            ### Get property stories        
            stories = info_json["props"]["pageProps"]["initialProps"]["property"]["description"]["stories"]
            if stories == None:
                    stories = 1
                    print("Stories by default: "+str(stories))
            else:
                    print("Stories: "+str(stories))
                    
            
            ### Gets number of bedrooms or if it is a studio
            Studio = False
            beds = info_json["props"]["pageProps"]["initialProps"]["property"]["description"]["beds"]
                                
            if beds != None:
                    if beds <= 0:
                        beds = 1
                        Studio = True
                        print("It is a studio")
                    else:
                        print("Beds: "+str(beds))
            else:
                    print("Number of bedrooms not included")
                    
            ### Gets useful area
            area = info_json["props"]["pageProps"]["initialProps"]["property"]["description"]["sqft"]     
            if area == None:
                    print("Useful area not found")
            else:
                    print("Useful area: "+str(area))
                        
                                    
            ### Gets total area
            area_tot = info_json["props"]["pageProps"]["initialProps"]["property"]["description"]["lot_sqft"]
            if area_tot == None:
                    print("Total area not available")
            else:
                    print("Total area: "+str(area_tot))
                    
            
            ### Get number of cars which the garage allows or if it doesn't has a garage
            garage = info_json["props"]["pageProps"]["initialProps"]["property"]["description"]["garage"]         
            if garage == None:
                    print("No garage")
            else:
                    print("Garage spaces: "+str(garage))

            
            ### Get description about the property
            description = info_json["props"]["pageProps"]["initialProps"]["property"]["description"]["text"]
            if description == None:
                    description = "N/A"
                    print("No description added")
            else:
                    print("Description: "+description)
                    
            
            ### Get agent and office of real state
            rs_info = info_json["props"]["pageProps"]["initialProps"]["property"]["consumer_advertisers"]
            for info in rs_info:
                    if info["type"] == "Agent":
                        agent = info["name"]
                        agent_id = info["agent_id"]
                        agent_phone = info["phone"]
                        
                        if agent == None:
                            agent = "N/A"
                            print("Real State agent not found")
                        else:
                            print("Agent: "+agent)
                                
                    elif info["type"] == "Office":
                        office = info["name"]
                        office_id = info["broker_id"]
                        office_phone = info["phone"]
                        
                        if office == None:
                            office = "N/A"
                            print("Real State office not found")   
                        else:
                            print("Office: "+office)
                            
            
            ### Gets address
            address = info_json["props"]["pageProps"]["initialProps"]["property"]["location"]["address"]["line"]
            if address == None:
                    s_number = info_json["props"]["pageProps"]["initialProps"]["property"]["location"]["address"]["street_number"]
                    s_direction = info_json["props"]["pageProps"]["initialProps"]["property"]["location"]["address"]["street_direction"]
                    s_name = info_json["props"]["pageProps"]["initialProps"]["property"]["location"]["address"]["street_name"]
                    s_suffix = info_json["props"]["pageProps"]["initialProps"]["property"]["location"]["address"]["street_suffix"]
                    s_post_direction = info_json["props"]["pageProps"]["initialProps"]["property"]["location"]["address"]["street_post_direction"]
                    postal_code = info_json["props"]["pageProps"]["initialProps"]["property"]["location"]["address"]["postal_code"]
                            
                    address = limpieza.getAddress(s_number, s_direction, s_name, s_suffix, s_post_direction, postal_code)
                    print(address)
            else:
                    print("Address: "+address)
                    
                    
                    
            ### Gets number of bathrooms
            bathroom = info_json["props"]["pageProps"]["initialProps"]["property"]["description"]["baths"]
            if bathroom == None:
                print("Number of bathrooms not included")
            else:
                print("Bathrooms: "+ str(bathroom))
            
            full_bath = info_json["props"]["pageProps"]["initialProps"]["property"]["description"]["baths_full"]
            if full_bath == None:
                print("Number of full bathrooms not included")
            else:
                print("Full baths: "+ str(full_bath))
                
                
            ### Get latitude and longitude
            longitude = None
            latitude = None
            Coordinates = info_json["props"]["pageProps"]["initialProps"]["property"]["location"]["address"]["coordinate"]
            
            if Coordinates != None:
                latitude = Coordinates["lat"]
                if latitude == None:
                    print("Latitude not available")
                else:
                    print("Latitude: " + str(latitude))
                    
                longitude = Coordinates["lon"]
                if longitude == None:
                    print("Longitude not available")
                else:
                    print("Longitude: " + str(longitude))
            else:
                print("Coordinates are not available")
                
            
            ### Gets price using css and if not found it uses the json information
            price = info_json["props"]["pageProps"]["initialProps"]["property"]["list_price"]
            if price == None:
                print("Total price not available")
            else:
                print("Total price: " + str(price))
                
                
            ### Nombre de la unidad
            unit = info_json["props"]["pageProps"]["initialProps"]["property"]["location"]["address"]["unit"]
            if unit == None:
                print("Unit name not available")
            else:
                print("Unit name: " + unit)
                
                
            ### Get year the property was built
            year_built = info_json["props"]["pageProps"]["initialProps"]["property"]["description"]["year_built"]
            if year_built == None:
                print("Year of construction not available")
            else:
                print("Year built: " + str(year_built))
                
                
            connection.insert_into_db(property_id=property_id, list_id=list_id, list_date=list_date, stories=stories, beds=beds, studio=Studio, area=area, area_tot=area_tot, garage=garage, description=description, agent=agent, office=office, address=address, bathroom=bathroom, full_baths=full_bath, latitude=latitude, longitude=longitude, price=price, unit=unit, year_built=year_built)
         
        

    # f = open("html2.txt", 'w')
    # f.write(json_inf)
    # f.close()
