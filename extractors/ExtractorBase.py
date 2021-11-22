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
            pw = soup.find('span', 'a-price-whole')
            pf = soup.find('span', 'a-price-fraction')
            return pw.get_text() + pf.get_text()
        elif url.find('target') != -1:
            pw = soup.find('div', 'web-migration-tof__PriceFontSize-sc-14z8sos-16 dqRAOH')
            return pw.get_text()
        else:
            
        #more sites
        
        pass

    def is_valid_url(self, url):
        return False