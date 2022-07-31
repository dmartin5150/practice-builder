import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from components.Surgeon import Surgeon
from components.Practice import Practice 
from util.utilities import get_url, get_location_url




class ProviderSpider(scrapy.Spider):

    name = 'provider'
    found_surgeons = []
    def __init__(self, *args, **kwargs):
        super(ProviderSpider, self).__init__(*args, **kwargs)
        self.surgeon = kwargs.get("surgeon")
        self.city = kwargs.get("city")
        self.url = get_url(self.surgeon.get_name(),self.city)


    def start_requests(self):
        yield SeleniumRequest(
            url=self.url, 
            wait_time=5,
            screenshot=True,
            callback=self.get_webmd_link
        )


    def get_webmd_link(self, response):

        # img = response.meta['screenshot']
        # print('response', response.url)
        # with open('screenshot.png','wb') as f:
        #     f.write(img)

        surgeons_from_initial_search = response.xpath("//div[@class='prov-name-wrap']/a")
        found = False
        for surgeon in surgeons_from_initial_search:
            surgeon_name = surgeon.xpath('.//h2/text()').get()
            if self.surgeon.compare_name(surgeon_name):
                found=True
                print(f"Matched surgeon Ascension name:{self.surgeon.get_name()} webmd name: {surgeon_name}" )
                webmd_link = get_location_url(surgeon.xpath('.//@href').get())
                self.surgeon.set_webmd_link(webmd_link)
                self.surgeon = Surgeon(self.surgeon.get_name(), self.surgeon.get_ministry())
            else:
                print(f"No match Ascension name:{self.surgeon.get_name()} webmd name: {surgeon_name}" )
        if not found:
            self.surgeon.set_webmd_link=''

            



   
