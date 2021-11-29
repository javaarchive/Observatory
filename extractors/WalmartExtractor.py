from extractors.ExtractorBase import ExtractorBase

from bs4 import BeautifulSoup

class WalmartExtractor(ExtractorBase):
    def __init__(self):
        super(WalmartExtractor, self).__init__()
    def extract_data(self,url):
        ExtractorBase.extract_data(self,url) # superclass call
        content = self.driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        priceElem = soup.find('div', {
                'itemprop':  "price"
        })
        return float(priceElem.getText().replace("$",""))

    def is_valid_url(self, url: str):
        return url.startswith('https://www.walmart.com') or url.startswith('https://walmart.com')