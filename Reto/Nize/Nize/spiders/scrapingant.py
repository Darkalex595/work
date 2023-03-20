from scrapingant_client import ScrapingAntClient

client = ScrapingAntClient(token='09104f86c7634063a015b3a9a6553f18')
# Scrape the example.com site.
result = client.general_request('https://thecomicstore.com.sv')
funko = result.css("ul").getall()
print(funko)