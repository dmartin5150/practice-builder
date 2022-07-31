from scrapy.crawler import CrawlerProcess
from spiders.provider  import ProviderSpider # this is our friend in subfolder **spiders**
from scrapy.utils.project import get_project_settings
from components.Surgeon import Surgeon
from components.City import City


austin_coordinates = ('36.1658','-86.7844')
current_city =  City('Nashville', 'TN', austin_coordinates)
current_surgeon = Surgeon('Gregory Raab, MD','TNNAS')
# provider_url = 'https://doctor.webmd.com/results?q=Gregory%20Raab&pagenumber=18&d=40&sortby=bestmatch&medicare=false&medicaid=false&newpatient=false&isvirtualvisit=false&minrating=0&pt=36.1658,-86.7844&city=Nashville&state=TN'


process = CrawlerProcess(get_project_settings())
process.crawl(ProviderSpider, surgeon=current_surgeon, city=current_city)
process.start() # the script will block here until the crawling is finished
practices = current_surgeon.get_practices()
for practice in practices:
    print(practice)

