from selenium import webdriver
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(executable_path="/Users/david.martin6@ascension.org/OneDrive - Ascension/Documents/scrapy/projects/practices/practices/Selenium_basics/chromedriver", options=chrome_options)
# driver.get("https://doctor.webmd.com/results?q=Dr.%20Adair%20Frierson%20Deberry-Carlisle%20&pagenumber=1&pt=30.48,-87.32&d=40&zc=32526&city=Pensacola&state=FL")
driver.get("https://duckduckgo.com")

search_input = driver.find_element_by_xpath("//input[contains(@class,'js-search-input search__input--adv')]")
search_input.send_keys('My User Agent')
search_button = driver.find_element_by_id("search_button_homepage")
# search_button.click()
search_input.send_keys(Keys.ENTER)

print(driver.page_source)
driver.close()