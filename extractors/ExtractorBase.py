from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import os
class ExtractorBase:
    globalDriver = None

    def __init__(self):
        if ExtractorBase.globalDriver is not None:
            self.driver = ExtractorBase.globalDriver
            return
        if os.getenv('PHANTOMJS_LOCATION') is None:
            options = webdriver.ChromeOptions()
            # options.add_argument("start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            self.driver = webdriver.Chrome(os.getenv('CHROMEDRIVER_LOCATION','/home/raymond/chromedriver'), options = options)
            try:
                from selenium_stealth import stealth
                stealth(self.driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Google Inc. (NVIDIA Corporation)",
                    renderer="ANGLE (NVIDIA Corporation, NVIDIA GeForce GTX 1650/PCIe/SSE2, OpenGL 4.5.0 NVIDIA 470.74)",
                    fix_hairline=True
                )
            except:
                print("Selenium Stealth not found, this may increase your changes of being detected as a bot")
                
        else:
            self.driver = webdriver.PhantomJS(executable_path=os.getenv('PHANTOMJS_LOCATION'))
        self.driver.set_window_size(1920, 960)
        # self.driver.set_page_load_timeout(60)
        ExtractorBase.globalDriver = self.driver
    def extract_data(self, url):
        # return the relevant data for a url
        self.driver.get(url)
        '''
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
        '''

    def is_valid_url(self, url):
        return False
