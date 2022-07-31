import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from components.Surgeon import Surgeon
from components.Practice import Practice 
from util.utilities import get_url, get_location_url



class ProviderSpider(scrapy.Spider):

    name = 'provider'

    def __init__(self, *args, **kwargs):
        super(ProviderSpider, self).__init__(*args, **kwargs)
        self.surgeon = kwargs.get("surgeon")
        self.city = kwargs.get('city')
        self.url = get_url(self.surgeon.get_name(),self.city)


    def start_requests(self):
        yield SeleniumRequest(
            url=self.url, 
            wait_time=5,
            screenshot=True,
            callback=self.parse
        )



    def parse(self, response):

        # img = response.meta['screenshot']
        # print('response', response.url)
        # with open('screenshot.png','wb') as f:
        #     f.write(img)

        surgeons = response.xpath("//div[@class='prov-name-wrap']/a")
        for surgeon in surgeons:
            surgeon_name = surgeon.xpath('.//h2/text()').get()
            if self.surgeon.compare_name(surgeon_name):
                print(f"Matched surgeon Ascension name:{self.surgeon.get_name()} webmd name: {surgeon_name}" )
                webmd_link = get_location_url(surgeon.xpath('.//@href').get())
                self.surgeon.set_webmd_link(webmd_link)
                yield SeleniumRequest(
                    url=webmd_link, 
                    wait_time=5,
                    screenshot=True,
                    callback=self.add_clinic_info
                )
            else:
                print(f"No match Ascension name:{self.surgeon.get_name()} webmd name: {surgeon_name}" )

    def add_specialties(self, response):
        specialties = response.xpath("//div[@class='prov-specialties-wrap']/span[@class='prov-specialty-name']")
        for specialty in specialties:
            specialty_name = specialty.xpath('.//text()').get()
            self.surgeon.add_specialty(specialty_name)


    def add_practices(self,response):
        locations = response.xpath("//div[@class='loc-1 webmd-col webmd-col-24 webmd-col-xs-24 webmd-col-sm-24 webmd-col-md-24 webmd-col-lg-15 webmd-col-xl-15']")
        for location in locations:
            practice_name = location.xpath(".//div[@class='location-practice-name webmd-row']/a/text()").get()
            practice_link = location.xpath(".//div[@class='location-practice-name webmd-row']/a/@href").get()
            practice_address = location.xpath(".//div[@class='location-address webmd-row']/text()").get()
            practice_city = location.xpath(".//div[@class='location-geo webmd-row']/span[@class='location-city']/text()").get()
            practice_state = location.xpath(".//div[@class='location-geo webmd-row']/span[@class='location-state']/text()").get()
            practice_zip = location.xpath(".//div[@class='location-geo webmd-row']/span[@class='location-zipcode']/text()").get()
            practice_phone = location.xpath(".//div[@class='location-phone webmd-row']/a/text()").get()
            current_practice = Practice(practice_name,practice_address,practice_city,practice_state,practice_zip,practice_phone,practice_link)
            self.surgeon.add_practice(current_practice)

    def add_clinic_info(self,response):
        self.add_specialties(response)
        self.add_practices(response)




   
