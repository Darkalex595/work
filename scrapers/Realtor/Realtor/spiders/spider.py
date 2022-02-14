from email import header
from types import CoroutineType
import scrapy
from Realtor.url import BASE_URL, determine_city
from Realtor.constants import type_search, Counties, URL
import time

class RealtorSpider(scrapy.Spider):
    
    name = "Realtor"
    
    header = {
        "authority": "www.realtor.com",
        "path" : "/realestateandhomes-search/Miami-Beach_FL",
        "accept-encoding" : "gzip, deflate, br",
        "cookie": 'split=n; split_tcv=170; __vst=d200eb78-90ec-41c8-8bc1-fccbb26fc7a6; G_ENABLED_IDPS=google; __gads=ID=9d05bbeaeb63dde2:T=1643920877:S=ALNI_MYWZvLDdT7kx_vg1I0WgpI9BC8d_Q; _pxvid=0a343bba-8532-11ec-bd78-6b4c74727076; g_state={"i_p":1644018114367,"i_l":2}; permutive-id=8b1ed279-99be-4407-84dc-c93474684a31; ab.storage.userId.7cc9d032-9d6d-44cf-a8f5-d276489af322={"g":"visitor_d200eb78-90ec-41c8-8bc1-fccbb26fc7a6","c":1643931753229,"l":1643931753229}; ab.storage.deviceId.7cc9d032-9d6d-44cf-a8f5-d276489af322={"g":"d8b0dd7d-8710-f0d5-b85d-171e9cfb2947","c":1643931753234,"l":1643931753234}; _ncg_id_=e7a7e408-912a-41fc-865d-5bfbfb011f79; _ncg_g_id_=eb44d254-16b1-48c3-807f-c84a833fc56c; __qca=P0-1610449954-1643931753943; ajs_anonymous_id="1128632a-9b66-4555-ae46-b9ad0d34e54e"; _gcl_au=1.1.1316557421.1643931761; _ta=us~1~89df68bc35032d48c293adce8574aa42; _ga=GA1.2.960362548.1643931753; _gid=GA1.2.1877445345.1643931762; _fbp=fb.1.1643931762245.389423919; _tac=false~google|not-available; __ssn=27da846d-00b7-46e5-97a5-8e2fac7456d6; __ssnstarttime=1644009528; SLG_G_WPT_TO=es; AMCVS_8853394255142B6A0A4C98A4@AdobeOrg=1; AMCV_8853394255142B6A0A4C98A4@AdobeOrg=-1124106680|MCIDTS|19027|MCMID|25377083391311274148721041662717506096|MCAID|NONE|MCOPTOUT-1644016731s|NONE|vVersion|5.2.0|MCAAMLH-1644614331|4|MCAAMB-1644614331|j8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI; __split=12; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; AMCVS_AMCV_8853394255142B6A0A4C98A4@AdobeOrg=1; srchID=e7ed75e6cdb3447cbc419e935933c11b; criteria=pg=1&sprefix=%2Frealestateandhomes-search&area_type=city&search_type=city&city=Miami%20Beach&state_code=FL&state_id=FL&lat=25.8105959&long=-80.1488517&county_fips=12086&county_fips_multi=12086&loc=Miami%20Beach%2C%20FL&locSlug=Miami-Beach_FL&county_needed_for_uniq=false; user_activity=return; last_ran=-1; pxcts=13e8f940-8600-11ec-ad4c-093046ebc107; srchID=27b72ca1fd014cf5b3acefea9632654d; _tas=cakdfur6zl7; _ncg_sp_ses.cc72=*; AMCV_AMCV_8853394255142B6A0A4C98A4@AdobeOrg=-1124106680|MCIDTS|19027|MCMID|47567652546420518185199460466127423759|MCOPTOUT-1644019035s|NONE|vVersion|5.2.0; __fp=89411c79771bb884ad066f8f473b70c1; last_ran_threshold=1644012034811; _ncg_sp_id.cc72=e7a7e408-912a-41fc-865d-5bfbfb011f79.1643931753.3.1644012035.1644009985.10cdde00-44e8-4ace-a85d-000d737a23fb; _pxff_bdd=2000; _pxff_cde=5,10; adcloud={"_les_v":"y,realtor.com,1644013843"}; _gat=1; _uetsid=fac5a530854a11ec8b0ad10fff72578b; _uetvid=fac607d0854a11ec83d13b37a2294c28; _px3=a09290ffd6afb11f8d36add3cfee34b94f38d7d3fa648be79bf612a0c38c67d8:cy4uPhNwDWUS1AFntjCThBf3dSl0z6XJyuBi0vw/JlZoizL+bgeAElJwUDU7Mhm1SsI5f5EI7YWY24DOxRf8Rw==:1000:BbWyKmFI5RKj+VUbQS9mRjYizHGlQeaT2tO3WrsU91wKy1wT1I5pTMfiuYjzBu/BRoeyb6nlhCXnP4HxOp9NH8gqTo+COqlHJkATREG/6/CtPxC7zmkl/q38HlH2N5jvoYDcW4c8fmOEzt8dxw2HCkyIXIiaP8yyiOy0+1IuIH7OE9NcnNTuPE6zZukzOYVhq8rcsBvvngKJ6WfxNBXpww==; QSI_HistorySession=https://www.realtor.com/realestateandhomes-search/Miami-Beach_FL~1644009544116|https://www.realtor.com/~1644011855326|https://www.realtor.com/realestateandhomes-search/Miami-Beach_FL~1644012046022; ab.storage.sessionId.7cc9d032-9d6d-44cf-a8f5-d276489af322={"g":"68b4726d-aa86-f186-02cd-4753c752e4de","e":1644013854676,"c":1644009540409,"l":1644012054676}'
    }
    
    def create_URL(self, State):
        
        urls = []
        
        
        ## Lineas temporales ya que el tipo de busqueda y el estado deben ser definidos por el usuario
        search = type_search[0]
        state = "Florida"
        ########
        
        
        
        
        aux_counties = determine_city(state)
        
        # for county in aux_counties:
        #     for city in county["Cities"]:
        #         urls.append(BASE_URL.format(search = search, city = city, code = county["Code"]))
        
        urls.append(BASE_URL.format(search = search, city = "Alachua", code = "FL"))
            
        return urls
        
    def start_requests(self):    
        
        State = "Florida"  
        # urls = self.create_URL(State)
        
        #PAgina de lista
        urls = ["https://www.realtor.com/realestateandhomes-search/Miami-Beach_FL"]
        
        #Pagina de propiedad
        # urls = ["https://www.realtor.com/realestateandhomes-detail/90-Alton-Rd-Apt-2207_Miami-Beach_FL_33139_M59625-32159?property_id=5962532159&from=ab_mixed_view_card"]
        
        print(urls)   

        for url in urls:
            # print("I'm in ", url)
            yield scrapy.Request(url=url, callback=self.parse, headers=self.header)
            

    def parse(self, response):
        links = response.css('a.jsx-1534613990.card-anchor::attr(href)').getall()
       
        for link in links:  
            # print(URL+link)
            yield response.follow(URL+link, callback=self.parse_buy)
    
    
    # Parse method for properties on sale
    def parse_buy(self, response):
        # Data = response.xpath('//*[@id="__NEXT_DATA__"]').get()
        
        price = response.css('div.rui__sc-62xokl-0.bowEcH::text').get()
        
        beds = response.css('li.rui__sc-1thjdnb-0.kxaGja span::text').get()
        
        bathroom = response.css('li.rui__jalfv4-0.Shkdj span::text').get()
        
        areaAux = response.css('li.rui__sc-147u46e-0.bcVtCB span')
        area = areaAux[0].css('span::text').get()
        
        address = response.css('h1.rui__ygf76n-0.hGDmoR.rui__sc-17fo6pt-0.iRbBbO::text').get()
        
        list_desc = response.css('li.rui-patterns__sc-2lxyoa-0.ivcDnD')
        
        attributes = []
        values = []
        Cont = 0
        
        for attr in list_desc:
            aux = attr.css('div div')
            attributes.append(aux[0].css('span::text').get())
            values.append(aux[1].css('::text').get())
            print(attributes[Cont]+":",values[Cont])
            # print(values[Cont]) 
            Cont = Cont + 1
            
        
        print("Precio:", price)
        print('Camas:', beds)
        print('Baños:', bathroom)
        print('Area:', area)
        print('Direccion:', address)
        
        # print(list_desc)
        
        
    def parse_rent(self, response):
        Data = response.xpath('//*[@id="__NEXT_DATA__"]').get()