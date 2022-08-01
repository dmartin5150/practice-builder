import scrapy
from scrapy_selenium import SeleniumRequest
from components.Practice import Practice 




class PracticesSpider(scrapy.Spider):

    name = 'practices'
    
    def __init__(self, *args, **kwargs):
        super(PracticesSpider, self).__init__(*args, **kwargs)
        self.surgeons = kwargs.get('surgeons')
        self.start_urls = kwargs.get("urls")
            

    def parse(self, response):
        self.add_specialties(response)
        self.add_practices(response)

     

    def add_specialties(self, response):
        listed_surgeon= self.surgeons[response.url]
        specialties = response.xpath("//div[@class='prov-specialties-wrap']/span[@class='prov-specialty-name']")
        for specialty in specialties:
            specialty_name = specialty.xpath('.//text()').get()
            listed_surgeon.add_specialty(specialty_name)


    def add_practices(self,response):
        listed_surgeon= self.surgeons[response.url]
        locations = response.xpath("//div[@class='loc-1 webmd-col webmd-col-24 webmd-col-xs-24 webmd-col-sm-24 webmd-col-md-24 webmd-col-lg-15 webmd-col-xl-15']")
        for location in locations:
            practice_name = location.xpath(".//div[@class='location-practice-name webmd-row']/a/text()").get()
            practice_link = location.xpath(".//div[@class='location-practice-name webmd-row']/a/@href").get()
            practice_address = location.xpath(".//div[@class='location-address loc-coi-locad webmd-row']/text()").get()
            practice_city = location.xpath(".//div[@class='location-geo webmd-row']/span[@class='location-city loc-coi-loccty']/text()").get()
            practice_state = location.xpath(".//div[@class='location-geo webmd-row']/span[@class='location-state loc-coi-locsta']/text()").get()
            practice_zip = location.xpath(".//div[@class='location-geo webmd-row']/span[@class='location-zipcode loc-coi-loczip']/text()").get()
            practice_phone = location.xpath(".//div[@class='location-phone webmd-row']/a/text()").get()
            print(f'state: {practice_state}')
            current_practice = Practice(practice_name,practice_address,practice_city,practice_state,practice_zip,practice_phone,practice_link)
            listed_surgeon.add_practice(current_practice)
            print('adding practice')





   
