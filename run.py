from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor, defer
from spiders.provider  import ProviderSpider
from spiders.practices import PracticesSpider
from scrapy.utils.project import get_project_settings
from components.Surgeon import Surgeon
from components.City import City


austin_coordinates = ('36.1658','-86.7844')
current_city =  City('Nashville', 'TN', austin_coordinates)
surgeon1 = Surgeon('Gregory Raab, MD','TNNAS')
surgeon2 = Surgeon('William Kurtz, MD', 'TNNAS')
surgeon3 = Surgeon('Test', 'TNNAS')
surgeon_list = []
surgeon_list.append(surgeon1)
surgeon_list.append(surgeon2)
surgeon_list.append(surgeon3)




process = CrawlerProcess(get_project_settings())
settings = get_project_settings()
runner = CrawlerRunner(settings)

@defer.inlineCallbacks
def crawl():
    surgeon_search_results = []
    for surgeon in surgeon_list:
        yield runner.crawl(ProviderSpider, surgeon=surgeon, city=current_city)
        yield runner.crawl(PracticesSpider, surgeon=surgeon)
        surgeon_search_results.append(surgeon)
    reactor.stop()
    print('reactor stop')
    for surgeon in surgeon_search_results:
        print(f'Name: {surgeon.get_name()} Link: {surgeon.get_webmd_link()}')
        practices = surgeon.get_practices()
        for practice in practices:
            print(practice)

crawl()
reactor.run()
print('Finished')

# surgeon_search_results = []
# for surgeon in surgeon_list:
#     yield process.crawl(ProviderSpider, surgeon_search_results = surgeon_search_results, surgeon=surgeon, city=current_city)
#     process.start() # the script will block here until the crawling is finished












