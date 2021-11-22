from bs4 import BeautifulSoup
from .ExtractorBase import ExtractorBase


class MultiExtractor(ExtractorBase):
    def __init__(self):
        super(MultiExtractor, self).__init__()
    def extract_data(self,url):
        ExtractorBase.extract_data(self,url) # superclass call
        content = self.driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        if "amazon" in url:                
            #for amazon
            # pw = soup.find('span', 'a-price-whole')
            # pf = soup.find('span', 'a-price-fraction')
            # weirdly this works but
            priceElem = next(soup.find('span', {
                'class': ['a-price','a-text-price','apexPriceToPay']
            }).children)
            #returns price
            print(priceElem.getText())
            return priceElem.getText()[1:]#pw.get_text() + pf.get_text()

        elif "target" in url:
            #for Target
            pw = soup.find("div",{
                "data-test": "product-price"
            })
            #returns price only
            print(pw,pw.getText())
            return pw.getText()[1:]
        elif "google" in url:
            #for google shopping
            # div class for airpod, mac,  brands -> aULzUe IuHnof
            result = soup.findAll('span', 'a8Pemb OFFNJ') #gets all spans that hold prices
            pw = soup.findAll('div', attrs={'class':'aULzUe IuHnof'}) #gets all the divs that hold brands- the name for this div class varies i think
            #may need to make it a hard-coded var based on search term

            ret = {pw[i].get_text(): result[i].get_text() for i in range(len(pw))}  #returns a dict of the two lists because idk how else

            return ret
    def is_valid_url(self, url):
        return "target" in url or "amazon" in url or "google" in url