from scrapingbee import ScrapingBeeClient
import limpieza
import json
from const import BASE_URL
from extract_json import extract
import time

client = ScrapingBeeClient(api_key='PNTT41IH5YFQ8XVTGE6JB97H35SXIXW4KWX2D5C566PXW3FTB8Y0TIQXPZ92TC8164PMZRZHE81WHXOH')

print("Estas en: https://www.realtor.com/realestateandhomes-search/Miami-Beach_FL")

response = client.get("https://www.realtor.com/realestateandhomes-search/Miami-Beach_FL",
                      params={
                          'extract_rules':{
                              "button_list": {
                                  "selector": ".item.btn",
                                  "type": "list"
                              },
                              "href_list":{
                                  "selector": ".item.btn",
                                  "type": "list",
                                  "output" : "@href"
                              },
                              "links":{
                                    "selector": ".jsx-1534613990",
                                    "type": "list",
                                    "output": "@href"
                                }
                          }
                      }
                      )

# string_inf = str(response.content)

print(str(response.status_code))



all_links = []

info = limpieza.eliminate_b(str(response.content))
info = limpieza.eliminate_lastChar(info)
info_json = json.loads(info)

button_list = info_json["button_list"]
href_list = info_json["href_list"]
link_list = info_json["links"]

all_links = all_links + link_list

# for link in link_list:
#     extract(BASE_URL+link)

# extract(BASE_URL+link_list[0])

# print(link_list)

tam = len(button_list)
print(button_list)

if(button_list[tam-1] == "Next"):
    next_exist = True
else:
    next_exist = False

print(info_json["button_list"])
print(response.status_code)

#################################################################################################################################################

if(next_exist):
    while(next_exist):
        next_link = href_list[tam-1]
        print("Estas en: " + BASE_URL + next_link)
        
        
        response = client.get(BASE_URL+next_link,
                        params={
                            'extract_rules':{
                                "button_list": {
                                    "selector": ".item.btn",
                                    "type": "list"
                                },
                                "href_list":{
                                    "selector": ".item.btn",
                                    "type": "list",
                                    "output" : "@href"
                                },
                                "links":{
                                    "selector": ".jsx-1534613990",
                                    "type": "list",
                                    "output": "@href"
                                }
                            }
                        }
                        )
        
        if(str(response.status_code) != "500"):
        
            info = limpieza.eliminate_b(str(response.content))
            info = limpieza.eliminate_lastChar(info)
            info_json = json.loads(info)

            button_list = info_json["button_list"]
            href_list = info_json["href_list"]
            link_list = info_json["links"]
            
            all_links = all_links + link_list
            
            
            
            # for link in link_list:
            #     extract(link)
            
            # print(link_list)
            
            tam = len(button_list)
            
            if(tam > 0):
            
                # print(info_json["button_list"])
                print(response.status_code)

                if(button_list[tam-1] == "Next" and href_list[tam-1] != ""):
                    next_exist = True
                else:
                    print("End of Catalogue")
                    next_exist = False
            else:
                print("Fin")
                break
        else:
            print("Error 500. Reintentando en " + BASE_URL + next_link)
            

    if(len(all_links) > 0):
        print("Links Requested")
        for link in all_links:
            extract(BASE_URL+link)
            time.sleep(5)
    else:
        print("No links available")
   
else:
    print("No hay siguiente")