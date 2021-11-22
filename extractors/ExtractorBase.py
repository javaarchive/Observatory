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
        #more sites

    def is_valid_url(self, url):
        return False