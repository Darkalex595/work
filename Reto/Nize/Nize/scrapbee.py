from scrapingbee import ScrapingBeeClient

client = ScrapingBeeClient(api_key='3HKO9G7ARI9VQGU4BXA0UDBL7WA7VELIYRGIUWCJU5VGDTYT9UFBN1KC2C42NJZNS31E0RBMMKXAKQJQ')

response = client.get("https://www.realtor.com/realestateandhomes-search/Miami-Beach_FL",
                      params={cd
                          'extract_rules': {"item": {
                                        "selector": "li.jsx-1881802087",
                                        "type": "list"
                                             }
                                            }
                          })

print('Response HTTP Status Code: ', response.status_code)
print('Response HTTP Response Body: ', response.content)