from extractors.ExtractorBase import ExtractorBase


class GoogleShoppingExtractor(ExtractorBase):
    def __init__(self):
        pass

    def is_valid_url(self, url: str):
        return url.startswith("https://google.com/") or url.startswith("https://www.google.com/") or url.startswith("https://shopping.google.com/")