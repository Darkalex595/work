from scrapingbee import ScrapingBeeClient

client = ScrapingBeeClient(api_key='3HKO9G7ARI9VQGU4BXA0UDBL7WA7VELIYRGIUWCJU5VGDTYT9UFBN1KC2C42NJZNS31E0RBMMKXAKQJQ')

response = client.get("https://www.portalinmobiliario.com/venta/departamento/santiago-metropolitana/8835-edificio-tocornal-nva#position=1&search_layout=stack&type=item&tracking_id=d261c5fb-76bc-48a5-9323-53b071808c6c",
                      params={
                          'extract_rules':{
                              "modal": ".ui-pdp-modal-content-autoheight.ui-pdp-modal-content-autoheight__container"
                          }
                      }
                      )

f = open("html.txt", 'w')
f.write(str(response.content))
f.close()

# print('Response HTTP Status Code: ', response.status_code)
# print('Response HTTP Response Body: ', response.content)