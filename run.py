from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from spiders.provider import ProviderSpider
from spiders.practices import PracticesSpider
from scrapy.utils.project import get_project_settings
from components.Surgeon import Surgeon
from components.City import City
from util.utilities import reformat_ascnesion_name
import pandas as pd


austin_coordinates = ('36.1658', '-86.7844')
current_city = City('Nashville', 'TN', austin_coordinates)
surgeon1 = Surgeon('Gregory Raab, MD', 'TNNAS')
surgeon2 = Surgeon('William Kurtz, MD', 'TNNAS')
surgeon3 = Surgeon('Test', 'TNNAS')
surgeon_list = []
surgeon_list.append(surgeon1)
surgeon_list.append(surgeon2)
surgeon_list.append(surgeon3)


settings = get_project_settings()
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    surgeon_search_results = []
    for surgeon in surgeon_list:
        yield runner.crawl(ProviderSpider, surgeon=surgeon, city=current_city)
        print('FINISHED PROVIDER')
        yield runner.crawl(PracticesSpider, surgeon=surgeon)
        print('FINISHED PRACTICE')
        surgeon_search_results.append(surgeon)
    reactor.stop()
    print('reactor stop')

name = "O'BRIEN, BRIDGET ANNE"
reformat = reformat_ascnesion_name(name)
print('reformat', reformat)


# crawl()
# print('starting reactor')
# reactor.run()


# print('Finished')
# columns = ['Ascension_Name', 'Webmd_Name', 'Webmd_Link', 'Ministry', 'Specialty',
#            'NPI', 'Clinic_Name', 'Address', 'City', 'State', 'Zip', 'Phone', 'Practice_Link']
# surgeon_data = pd.DataFrame(columns=columns)
# for surgeon in surgeon_list:
#     practices = surgeon.get_practices()
#     for practice in practices:
#         surgeon_row = pd.DataFrame([{'Ascension_Name': surgeon.name, 'Webmd_Name': surgeon.webmd_name,
#                                      'Ministry': surgeon.ministry, 'Specialty': surgeon.get_specialties(),
#                                      'NPI': surgeon.npi, 'Webmd_Link': surgeon.webmd_link, 'Clinic_Name': practice.name,
#                                      'Clinic_Name': practice.name, 'Address': practice.address, 'City': practice.city,
#                                      'State': practice.state, 'Zip': practice.zip, 'Phone': practice.phone, 'Practice_Link': practice.website}])
#         print(surgeon_row)
#         surgeon_data = pd.concat(
#             (surgeon_data, surgeon_row), ignore_index=True, axis=0)

# surgeon_data.to_csv('data.csv')


# surgeon_search_results = []
# for surgeon in surgeon_list:
#     yield process.crawl(ProviderSpider, surgeon_search_results = surgeon_search_results, surgeon=surgeon, city=current_city)
#     process.start() # the script will block here until the crawling is finished
