from .ExtractorBase import ExtractorBase

class PyppeteerExtractorBase(ExtractorBase):
    def __init__(self, *args, **kwargs):
        # do not super init here
        pass

    def extract(self, *args, **kwargs):
        raise NotImplementedError