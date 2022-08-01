from numpy import mat
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from spiders.provider2 import Provider2Spider
from spiders.practices import PracticesSpider
from scrapy.utils.project import get_project_settings
from components.Surgeon import Surgeon
from components.City import City
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from util.utilities import reformat_ascension_name, get_url
import pandas as pd
import time
import scrapy
from scrapy.crawler import CrawlerProcess



process = CrawlerProcess()



chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_path = "/Users/david.martin6@ascension.org/OneDrive - Ascension/Documents/scrapy/projects/practices/practices/chromedriver"


austin_coordinates = ('30.3024', '-97.7619')
current_city = City('Austin', 'TX', austin_coordinates)



def create_loaded_list(filename):
    loaded_list = []
    list_of_surgeons = pd.read_csv(filename)
    npi_dict = dict(zip(list_of_surgeons.Surgeon,list_of_surgeons.NPI))
    for key in npi_dict:
        surgeon = Surgeon(reformat_ascension_name(key), 'TXAUS',npi_dict[key])
        loaded_list.append(surgeon)
    return loaded_list


surgeon_loaded_list = []
surgeon_loaded_list = create_loaded_list("test1 - Sheet1.csv")
surgeon_final_list = []
print(surgeon_loaded_list)

settings = get_project_settings()
runner = CrawlerRunner(settings)



def tranfer_surgeons_to_final_list(search_results):
    for surgeon in search_results:
        surgeon_final_list.append(surgeon)

url_html_dict = {}
url_surgeon_dict = {}
start_urls = []


def get_provider_start_urls(url_html_dict):
    urls = []
    for key in url_html_dict:
        urls.append(key)
    return urls


for surgeon in surgeon_loaded_list:
    print('surgeon: ', surgeon)
    url = get_url(surgeon.get_name(),current_city)
    url_surgeon_dict[url] = surgeon
    driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    driver.close()
    url_html_dict[url] = html 
    start_urls= get_provider_start_urls(url_html_dict)
    print(start_urls)




runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(Provider2Spider,urls=start_urls,html=url_html_dict,surgeons=url_surgeon_dict, search_results=surgeon_final_list)
    # yield runner.crawl(MySpider2)
    reactor.stop()
    for surgeon in surgeon_final_list:
        print(f'Surgeon: {surgeon.name} Link: {surgeon.webmd_link}')

crawl()
reactor.run() 







# print('Finished')
# columns = ['Ascension_Name', 'Webmd_Name', 'Webmd_Link', 'Ministry', 'Specialty',
#            'NPI', 'Clinic_Name', 'Address', 'City', 'State', 'Zip', 'Phone', 'Practice_Link']
# surgeon_data = pd.DataFrame(columns=columns)
# for surgeon in surgeon_final_list:
#     practices = surgeon.get_practices()
#     for practice in practices:
#         surgeon_row = pd.DataFrame([{'Ascension_Name': surgeon.name, 'Webmd_Name': surgeon.webmd_name,
#                                      'Ministry': surgeon.ministry, 'Specialty': surgeon.get_specialties(),
#                                      'NPI': surgeon.npi, 'Webmd_Link': surgeon.webmd_link, 'Clinic_Name': practice.name,
#                                      'Clinic_Name': practice.name, 'Address': practice.address, 'City': practice.city,
#                                      'State': practice.state, 'Zip': practice.zip, 'Phone': practice.phone, 'Practice_Link': practice.website}])
#         surgeon_data = pd.concat(
#             (surgeon_data, surgeon_row), ignore_index=True, axis=0)

# surgeon_data.to_csv('data.csv')



