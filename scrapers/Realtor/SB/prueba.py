from scrapingbee import ScrapingBeeClient
import limpieza
import json

client = ScrapingBeeClient(api_key='KP5PQA2LWRFA2ZZE4K0SQIKLXJ6LMA83HEV0D1TIAS62231V09IW19480BGJFL3X6DO2651CYLII70RJ')


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
                              }
                          }
                      }
                      )

print(response.content)
print(response.status_code)

response_code = str(response.status_code)

if(response_code[0] == "2"):
    print("Hola")
else:
    print("Adios")