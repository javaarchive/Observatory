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
        
        if url.find("amazon") != -1:                
            pw = soup.find('span', 'a-price-whole')
            pf = soup.find('span', 'a-price-fraction')
            ret = {"amazon" : pw.get_text() + pf.get_text()}
            return ret
                   
        elif url.find("target") != -1:
            pw = soup.find('div', 'web-migration-tof__PriceFontSize-sc-14z8sos-16 dqRAOH')
            ret = {"target" : pw.get_text()}
            return ret
        
        else: #for google shopping
            result = soup.findAll('span', 'a8Pemb OFFNJ') #get all prices
            pw = soup.findAll('div', attrs={'class':'aULzUe IuHnof'}) #get all brand names- this div class name may vary.
            #this aULzUe IuHnof works for 'airpods', 'macbook', 'pot cooker'
            
            ret = {pw[i].get_text() : result[i].get_text() for i in range(len(pw))}
            return ret
        #more sites
        
        pass

    def is_valid_url(self, url):
        return False
