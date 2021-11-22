from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import os
class ExtractorBase:
    def __init__(self):
        self.driver = webdriver.Chrome(os.getenv('CHROMEDRIVER_LOCATION','/home/raymond/chromedriver'))

    def extract_data(self, url):
        # return the relevant data for a url
        self.driver.get(url)
        content = self.driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        if url.find('amazon') != -1:                
            #for amazon
            pw = soup.find('span', 'a-price-whole')
            pf = soup.find('span', 'a-price-fraction')
            #returns price
            return pw.get_text() + pf.get_text()

        elif url.find('target') != -1:
            #for Target
            pw = soup.find('div', 'web-migration-tof__PriceFontSize-sc-14z8sos-16 dqRAOH')
            #returns price only
            return pw.get_text()
        else:
            #for google shopping
            # div class for airpod, mac,  brands -> aULzUe IuHnof
            result = soup.findAll('span', 'a8Pemb OFFNJ') #gets all spans that hold prices
            pw = soup.findAll('div', attrs={'class':'aULzUe IuHnof'}) #gets all the divs that hold brands- the name for this div class varies i think
            #may need to make it a hard-coded var based on search term

            ret = {pw[i].get_text(): result[i].get_text() for i in range(len(pw))}  #returns a dict of the two lists because idk how else

            return ret
        #more sites

    def is_valid_url(self, url):
        return False