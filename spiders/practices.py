import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from components.Surgeon import Surgeon
from components.Practice import Practice 
from util.utilities import get_url, get_location_url




class PracticesSpider(scrapy.Spider):

    name = 'practices'
    
    def __init__(self, *args, **kwargs):
        super(PracticesSpider, self).__init__(*args, **kwargs)
        self.surgeon = kwargs.get('surgeon')


    def start_requests(self):
            url = self.surgeon.get_webmd_link()
            if url != '':
                yield SeleniumRequest(
                    url=url, 
                    wait_time=5,
                    screenshot=True,
                    callback=self.parse
                )
            

    def parse(self, response):
        self.add_specialties(response)
        self.add_practices(response)

     

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
            print('adding practice')





   
