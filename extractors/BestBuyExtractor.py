from extractors.ExtractorBase import ExtractorBase

from bs4 import BeautifulSoup

class BestBuyExtractor(ExtractorBase):
    def __init__(self):
        super(BestBuyExtractor, self).__init__()
    def extract_data(self,url):
        ExtractorBase.extract_data(self,url) # superclass call
        content = self.driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        priceElem = next(soup.find('div', {
                'class': ['priceView-hero-price','priceView-customer-price']
        }).children)
        return float(priceElem.getText().replace("$",""))

    def is_valid_url(self, url: str):
        return url.startswith('https://www.bestbuy.com') or url.startswith('https://bestbuy.com')