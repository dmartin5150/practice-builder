import scrapy
from scrapy.selector import Selector
from components.Surgeon import Surgeon
from util.utilities import  get_location_url



class Provider2Spider(scrapy.Spider):

    name = 'provider2'
    found_surgeons = []
    def __init__(self, *args, **kwargs):
        super(Provider2Spider, self).__init__(*args, **kwargs)
        self.search_results = kwargs.get("search_results")
        self.html= kwargs.get('html')
        self.start_urls = kwargs.get("urls")
        self.surgeons = kwargs.get('surgeons')



    def parse(self, response):
        print('url', response.url)
        resp = Selector(text=self.html[response.url])
        listed_surgeon = self.surgeons[response.url]
        print('Listed Surgeon', listed_surgeon)
        surgeons_from_initial_search = resp.xpath("//div[@class='prov-name-wrap']/a")
        found = False
        for surgeon in surgeons_from_initial_search:
            surgeon_name = surgeon.xpath('.//h2/text()').get()
            print("SURGEON NAME", surgeon_name)
            if listed_surgeon.compare_name(surgeon_name):
                found=True
                print(f"Matched surgeon Ascension name:{listed_surgeon.get_name()} webmd name: {surgeon_name}" )
                webmd_link = get_location_url(surgeon.xpath('.//@href').get())
                listed_surgeon.set_webmd_link(webmd_link)
                listed_surgeon.set_webmd_name(surgeon_name)
                self.search_results.append(listed_surgeon)
                listed_surgeon = Surgeon(listed_surgeon.get_name(), listed_surgeon.get_ministry())
            else:
                print(f"No match Ascension name:{listed_surgeon.get_name()} webmd name: {surgeon_name}" )
        if not found:
            listed_surgeon.set_webmd_link=''
            listed_surgeon.set_webmd_name ='Not found'
            self.search_results.append(listed_surgeon)
        yield {
            'surgeon': listed_surgeon.name
        }

            



   
